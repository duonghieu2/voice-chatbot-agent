import os
import sys
import unicodedata
from fastapi.testclient import TestClient
from app.main import app
from app.database.mock_db import db

# Define TestClient
client = TestClient(app)

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "tests", "audio_samples")

def strip_accents(text: str) -> str:
    """
    Transliterates Vietnamese text to ASCII to avoid console encoding crashes on Windows.
    """
    if not text:
        return ""
    # Normalize unicode to separate characters from their diacritics
    normalized = unicodedata.normalize('NFKD', text)
    # Filter out diacritical marks
    ascii_text = "".join([c for c in normalized if not unicodedata.combining(c)])
    # Hand-map specific Vietnamese letters
    ascii_text = ascii_text.replace('đ', 'd').replace('Đ', 'D')
    return ascii_text.encode('ascii', errors='replace').decode('ascii')

def run_static_integration_test():
    print("=" * 80)
    print("STARTING STATIC INTEGRATION FLOW TEST (WEEK 2)")
    print("=" * 80)
    
    # Reset DB to ensure fresh state
    db.reset_db()
    
    # 5 test scenarios representing key business intents
    scenarios = [
        {
            "name": "Scenario 1: Driver Late (Check Ride Status)",
            "file": "P001_driver_late.mp3"
        },
        {
            "name": "Scenario 2: Cancellation Fee (Verify Billing/Fees)",
            "file": "P004_payment_error.mp3"
        },
        {
            "name": "Scenario 3: Agent Escalation (Create Ticket & Escalated State)",
            "file": "P008_escalate.mp3"
        },
        {
            "name": "Scenario 4: Missing Food Item (Check Order Status)",
            "file": "P012_missing_item.mp3"
        },
        {
            "name": "Scenario 5: Refund Request (Trigger Refund Policy & Core Tool)",
            "file": "P016_refund_request.mp3"
        }
    ]
    
    success_count = 0
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n[{i}/5] RUNNING: {scenario['name']}")
        file_name = scenario["file"]
        audio_path = os.path.join(AUDIO_DIR, file_name)
        
        if not os.path.exists(audio_path):
            print(f"[-] Error: Audio file {file_name} not found at {audio_path}!")
            continue
            
        print(f"[-] Uploading audio sample: {file_name} ...")
        
        try:
            with open(audio_path, "rb") as f:
                # Construct HTTP upload tuple (filename, file_object, content_type)
                response = client.post(
                    "/api/v1/chatbot/voice",
                    files={"file": (file_name, f, "audio/mpeg")}
                )
                
            if response.status_code == 200:
                data = response.json()
                pipeline = data.get("pipeline_results", {})
                
                print(f"  [+] Response Status: {data.get('status')}")
                print(f"  [+] ASR Transcript  : {strip_accents(pipeline.get('asr_transcript'))}")
                print(f"  [+] Intent Detected : {pipeline.get('intent')}")
                print(f"  [+] Tool Called     : {pipeline.get('tool_called')}")
                print(f"  [+] Tool Arguments  : {strip_accents(str(pipeline.get('tool_args')))}")
                print(f"  [+] Tool Result     : {strip_accents(str(pipeline.get('tool_result')))}")
                print(f"  [+] Agent Response  : {strip_accents(pipeline.get('agent_response'))}")
                
                # Basic sanity validations
                assert data.get("status") == "success", "Response status is not success"
                assert pipeline.get("asr_transcript"), "ASR Transcript is empty"
                assert pipeline.get("intent"), "Intent is empty"
                assert pipeline.get("agent_response"), "Agent response is empty"
                
                print(f"  [+] STATUS: PASSED")
                success_count += 1
            else:
                print(f"  [-] HTTP Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"  [-] Exception occurred: {str(e)}")
            
        print("-" * 80)
        
    print(f"\nINTEGRATION TEST SUMMARY: {success_count}/{len(scenarios)} PASSED")
    print("=" * 80)
    
    if success_count == len(scenarios):
        print("ALL TESTS PASSED SUCCESSFULLY!")
        return 0
    else:
        print("SOME TESTS FAILED.")
        return 1

if __name__ == "__main__":
    sys.exit(run_static_integration_test())
