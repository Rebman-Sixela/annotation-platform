import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def show_dashboard():
    # Fetch all records
    response = supabase.table("annotation_results").select("*").execute()
    
    if not response.data:
        print("No tasks found in the database.")
        return

    # Convert to a DataFrame for easy viewing
    df = pd.DataFrame(response.data)
    
    # Select and rename columns for a cleaner display
    # We use .get() to avoid errors if a column is missing
    display_df = df[['raw_text', 'status']]
    display_df.columns = ['Task Content', 'Status']
    
    print("\n--- ANNOTATION DASHBOARD ---")
    print(display_df.to_string(index=False))
    print("\n")

if __name__ == "__main__":
    show_dashboard()