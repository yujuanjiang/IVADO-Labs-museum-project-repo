import pandas as pd
import sqlite3

def fetch_and_store_museum_data(url: str, db_path: str = "museums.db"):
    # Step 1: Fetch the first table from Wikipedia
    df = pd.read_html(url)[0]

    # Step 2: Rename columns for consistency
    df.columns = ['name', 'visitors', 'city', 'country']

    # Step 3: Clean and convert 'visitors' column
    df['visitors'] = (
        df['visitors']
        .astype(str)
        .str.replace(r"[^\d]", "", regex=True)  # Remove commas or text
        .astype(int)
    )

    # Step 4: Store in SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql("museums", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Saved {len(df)} records to {db_path}")

# Example usage:
if __name__ == "__main__":
    wikipedia_url = "https://en.wikipedia.org/wiki/List_of_most_visited_museums"
    fetch_and_store_museum_data(wikipedia_url)

