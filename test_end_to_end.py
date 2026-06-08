import os
import sys
import json
import time

# Reconfigure stdout/stderr for Unicode support on Windows command line
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the FastAPI app and components
from app.main import app
from app.database.mock_db import db

client = TestClient(app)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "tests", "audio_samples")

def run_end_to_end_test():
    print("=" * 85)
    print("      STARTING LIVE END-TO-END VOICE PIPELINE TEST (GEMINI 3.1 FLASH-LITE)")
    print("=" * 85)
    
    # 1. Check if Gemini API key is configured
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[-] Error: GEMINI_API_KEY not found in environment or .env file!")
        print("    Please configure it before running live tests.")
        return 1
    
    print(f"[+] Loaded GEMINI_API_KEY (ends in ...{api_key[-5:]})")
    print(f"[+] Using LLM Model: {os.getenv('LLM_MODEL_NAME', 'gemini-2.5-flash')}")
    
    # 2. Reset database to ensure fresh state
    print("[+] Resetting mock database to seed values...")
    db.reset_db()
    
    scenarios = [
        {
            "id": "P001",
            "name": "Scenario 1: Tài xế đến trễ (Check Ride Status)",
            "file": "P001_driver_late.mp3",
            "expected_intent": "check_ride_status"
        },
        {
            "id": "P004",
            "name": "Scenario 2: Phí hủy chuyến xe (Check Cancellation Fee)",
            "file": "P004_payment_error.mp3",
            "expected_intent": "check_ride_cancellation_fee"
        },
        {
            "id": "P008",
            "name": "Scenario 3: Khiếu nại thái độ tài xế (Escalate to Support Ticket)",
            "file": "P008_escalate.mp3",
            "expected_intent": "escalate_to_support"
        },
        {
            "id": "P012",
            "name": "Scenario 4: Giao thiếu món ăn (Check Order Status)",
            "file": "P012_missing_item.mp3",
            "expected_intent": "check_food_order_status"
        },
        {
            "id": "P016",
            "name": "Scenario 5: Yêu cầu hoàn tiền món ăn thiếu (Request Refund)",
            "file": "P016_refund_request.mp3",
            "expected_intent": "request_refund"
        }
    ]
    
    passed_count = 0
    
    for i, scenario in enumerate(scenarios, 1):
        print("\n" + "-" * 85)
        print(f"[{i}/{len(scenarios)}] RUNNING: {scenario['name']}")
        file_name = scenario["file"]
        audio_path = os.path.join(AUDIO_DIR, file_name)
        
        if not os.path.exists(audio_path):
            print(f"  [-] Error: Audio file '{file_name}' not found at: {audio_path}")
            continue
            
        print(f"  [-] File path: {audio_path}")
        print(f"  [-] Sending POST request to /api/v1/chatbot/voice ...")
        
        start_time = time.time()
        try:
            with open(audio_path, "rb") as f:
                response = client.post(
                    "/api/v1/chatbot/voice",
                    files={"file": (file_name, f, "audio/mpeg")}
                )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                pipeline = data.get("pipeline_results", {})
                
                print(f"  [+] Response Status : {data.get('status')}")
                print(f"  [+] ASR Transcript  : \"{pipeline.get('asr_transcript')}\"")
                print(f"  [+] Detected Intent : {pipeline.get('intent')}")
                print(f"  [+] Tool Called     : {pipeline.get('tool_called')}")
                print(f"  [+] Tool Arguments  : {json.dumps(pipeline.get('tool_args'), ensure_ascii=False)}")
                print(f"  [+] Tool Result     : {json.dumps(pipeline.get('tool_result'), ensure_ascii=False)}")
                print(f"  [+] Agent Response  : \"{pipeline.get('agent_response')}\"")
                print(f"  [+] Total Latency   : {elapsed:.2f} seconds")
                
                # Assert basic flow sanity
                assert data.get("status") == "success", "Failed API status"
                assert pipeline.get("intent") == scenario["expected_intent"], f"Intent mismatch. Expected: {scenario['expected_intent']}, Got: {pipeline.get('intent')}"
                assert pipeline.get("agent_response"), "Agent response is empty"
                
                print("  [+] Result          : PASSED")
                passed_count += 1
            else:
                print(f"  [-] Failed with status code {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"  [-] Exception occurred: {str(e)}")
            
    print("\n" + "=" * 85)
    print(f"LIVE END-TO-END PIPELINE SUMMARY: {passed_count}/{len(scenarios)} SCENARIOS PASSED")
    print("=" * 85)
    
    # Reset db at the end
    db.reset_db()
    
    return 0 if passed_count == len(scenarios) else 1

if __name__ == "__main__":
    sys.exit(run_end_to_end_test())
