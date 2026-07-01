import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def test_insert():
    print("Attempting to insert dummy data...")
    try:
        data = {
            "raw_text": "Jamie lives in Ashland.",
            "entity_type": "LOCATION",
            "extracted_value": "Ashland",
            "confidence_score": 0.95
        }
        response = supabase.table("extracted_entities").insert(data).execute()
        print("✅ Success! Data inserted.")
    except Exception as e:
        print("❌ Insertion failed. Error details:")
        print(e)

if __name__ == "__main__":
    test_insert()