import os
import json
import ollama
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def process_batch():
    # Load the tasks
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)

    for text in tasks:
        print(f"Processing: {text[:50]}...")
        
        prompt = f"""Extract Name, Location, and Date. 
        Return ONLY valid JSON with keys: 'name', 'location', 'date', 'confidence'.
        Text: {text}"""
        
        response = ollama.chat(model='qwen2.5-coder:7b', messages=[{'role': 'user', 'content': prompt}])
        content = response['message']['content'].replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(content)
            supabase.table("annotation_results").insert({
                "raw_text": text,
                "extracted_data": data
            }).execute()
            print(f"✅ Saved.")
        except Exception as e:
            print(f"❌ Failed to process: {e}")

if __name__ == "__main__":
    process_batch()