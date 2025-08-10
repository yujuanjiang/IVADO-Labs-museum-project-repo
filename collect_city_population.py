import sqlite3
import requests
import time

GEONAMES_USERNAME = "yjjianggeonamedb"  # Register free at https://www.geonames.org/login

def update_city_populations(db_path="museums.db", delay_seconds=1):
    """
    Fetch population for each city in museum.db using GeoNames API and update the table in batch.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Add 'Population' column if it doesn't exist
    cur.execute("PRAGMA table_info(museums)")
    columns = [col[1].lower() for col in cur.fetchall()]
    if "population" not in columns:
        cur.execute("ALTER TABLE museums ADD COLUMN Population INTEGER;")
        conn.commit()

    # Get unique cities from DB
    cur.execute("SELECT DISTINCT City FROM museums WHERE City IS NOT NULL;")
    cities = [row[0] for row in cur.fetchall()]

    for city in cities:
        # Query GeoNames API
        url = f"http://api.geonames.org/searchJSON"
        params = {
            "q": city,
            "maxRows": 1,
            "username": GEONAMES_USERNAME,
            "orderby": "population"
        }
        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            pop = None
            if data.get("geonames"):
                pop = data["geonames"][0].get("population")

            if pop:
                cur.execute("UPDATE museums SET Population = ? WHERE City = ?;", (pop, city))
                print(f"Updated {city} population: {pop}")
                conn.commit()
            else:
                print(f"No population found for city: {city}")

        except Exception as e:
            print(f"Error fetching population for {city}: {e}")

        time.sleep(delay_seconds)  # Avoid hitting API limits

    conn.close()


if __name__ == "__main__":
    update_city_populations()

