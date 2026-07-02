import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def verify_task():
    # Get one 'pending' task
    response = supabase.table("annotation_results").select("*").eq("status", "pending").limit(1).execute()
    
    if not response.data:
        print("No pending tasks to verify!")
        return

    task = response.data[0]
    print(f"\n--- TASK --- \n{task['raw_text']}")
    print(f"\n--- AI EXTRACTION --- \n{json.dumps(task['extracted_data'], indent=2)}")
    
    choice = input("\n[A]pprove, [E]dit, or [R]eject? ").lower()
    
    if choice == 'a':
        supabase.table("annotation_results").update({"status": "approved"}).eq("id", task['id']).execute()
        print("✅ Task Approved!")
    elif choice == 'e':
        new_data = input("Enter corrected JSON: ")
        supabase.table("annotation_results").update({"status": "corrected", "extracted_data": json.loads(new_data)}).eq("id", task['id']).execute()
        print("📝 Task Updated!")
    elif choice == 'r':
        supabase.table("annotation_results").update({"status": "rejected"}).eq("id", task['id']).execute()
        print("❌ Task Rejected!")

if __name__ == "__main__":
    verify_task()