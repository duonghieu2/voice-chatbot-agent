import json
import os
import asyncio
import edge_tts

async def generate_speech(text: str, voice: str, output_path: str):
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print(f"Saved: {os.path.basename(output_path)}")
    except Exception as e:
        print(f"Error generating {os.path.basename(output_path)}: {e}")

async def main():
    prompts_path = r"c:\Users\Administrator\Developer\Intern_VSF\voice-chatbot-agent-demo\app\database\prompts.json"
    output_dir = r"c:\Users\Administrator\Developer\Intern_VSF\voice-chatbot-agent-demo\tests\audio_samples"
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(prompts_path):
        print(f"Error: Prompts file not found at {prompts_path}")
        return
        
    with open(prompts_path, "r", encoding="utf-8") as f:
        prompts = json.load(f)
        
    # Giọng đọc chuẩn tiếng Việt của Microsoft Edge TTS
    female_voice = "vi-VN-HoaiMyNeural"
    male_voice = "vi-VN-NamMinhNeural"
    
    tasks = []
    print(f"Starting synthesis of {len(prompts)} audio files using Multilingual voices...")
    
    for i, p in enumerate(prompts):
        pid = p["id"]
        category = p["category"]
        text = p["text"]
        
        # Đan xen giọng đọc Nam và Nữ
        voice = female_voice if i % 2 == 0 else male_voice
        
        filename = f"{pid}_{category}.mp3"
        output_path = os.path.join(output_dir, filename)
        
        tasks.append(generate_speech(text, voice, output_path))
        
    await asyncio.gather(*tasks)
    print("Finished generating all test audio samples!")

if __name__ == "__main__":
    asyncio.run(main())
