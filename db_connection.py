import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "@rootvk12jun",
}
DB_NAME = "ev_hub_db"                       

def initialize_db():
    """Create the database and tables dynamically on startup."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS station(
                id INT PRIMARY KEY,
                location VARCHAR(150) NOT NULL,
                charger_type VARCHAR(50) NOT NULL,
                price_per_kwh DECIMAL(5,2) NOT NULL,
                status VARCHAR(50) DEFAULT 'Available'
            )  
        """)
  
  
        cursor.execute("SELECT COUNT(*) FROM station")
        if cursor.fetchone()[0] == 0:
            initial_station = [
                (1, "Baner Highway Hub", "DC Fast Charger", 18.50, "Available"),
                (2, "Shivajinagar Mall parking", "AC Type 2", 12.00, "Occupied"),
                (3, "FC Road Plaza", "DC Fast Charger", 19.00, "Available"),
                (4, "Hinjewadi Phase 1", "AC Type 2", 11.50, "Under Maintenance"),
                (5, "Kothrud Metro Station", "DC Fast Charger", 17.80, "Available")
            ]
       
            cursor.executemany(
                "INSERT INTO station (id, location, charger_type, price_per_kwh, status) VALUES (%s, %s, %s, %s, %s)",
                initial_station  
            )
            
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialization completed.")
    except Error as e:
        print(f"Database Setup Error: {e}")

def get_connection():
    """Helper function to get an active database link.""" 
    try:
       
        return mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
    except Error as e:
        print(f"Connection Error: {e}")
        return None   


if __name__ == "__main__":      
    print("Initializing...")   
    initialize_db()
    conn = get_connection()
    if conn:
        print("Success! Connection established.") 
        conn.close()