from db_connection import get_connection
def print_table(rows):
    """Helper to display rows in a clean,human-readable terminal matrix."""
    if not rows:
        print("\nNo charging station found matchingthose parameters.")
        return
    print("\n"+"="*80)
    print(f"{'STATION ID':<12} | {'LOCATION':<25} | {'CHARGER TYPE':<18} | {'RATE(₹/kwh)':<12} | {'STATUS':<12}")
    print("="*80)
    for r in rows:
        print(f"{r[0]:<12} | {r[1]:<25} | {r[2]:<18} | {r[3]:<12.2f} | {r[4]:<12}")
        print("="*80+"\n")


# ==========================================
# ADMIN PANEL: NETWORK OPERATOR
# ==========================================
def admin_panel():
    while True:
        print("\n---EV NETWORK OPERATOR TERMINAL (ADMIN) ---")
        print("1. Add New Charging Station (Create)")
        print("2. View All Grid Station (Read)")
        print("3. Update Station Status/Rates (Update)")
        print("4. Remove Station from Network (Delete)")
        print("5. Back to Main Menu")
        
        choice = input("\nSelect action (1-5): ").strip()
        conn = get_connection()
        if not conn: 
            print(" Database offline."); continue
        cursor = conn.cursor()

        if choice == '1': # CREATE
            print("\n--- Add New Grid Node ---")
            try:
                sid = int(input("Enter Station ID: "))
                loc = input("Enter Location Area Name: ").strip()
                ctype = input("Charger Type (AC Type 2 / DC Fast): ").strip()
                rate = float(input("Enter Price per kWh (₹): "))
                cursor.execute("INSERT INTO station (id, location, charger_type, price_per_kwh) VALUES (%s, %s, %s, %s)", (sid, loc, ctype, rate))
                conn.commit()
                print(" Station successfully registered online!")
            except Exception as e:
                print(f" Refused: Duplicate ID or invalid format entered. ({e})")

        elif choice == '2': # READ
            cursor.execute("SELECT * FROM station")
            print_table(cursor.fetchall())

        elif choice == '3': # UPDATE
            try:
                sid = int(input("Enter Station ID to update: "))
                cursor.execute("SELECT * FROM station WHERE id = %s", (sid,))
                station = cursor.fetchone()
                if station:
                    print(f"Current details: {station}")
                    new_rate = input(f"New Rate [Current: {station[3]}]: ").strip()
                    rate = float(new_rate) if new_rate else station[3]
                    new_status = input(f"New Status (Available/Occupied/Maintenance) [Current: {station[4]}]: ").strip() or station[4]
                    
                    cursor.execute("UPDATE station SET price_per_kwh=%s, status=%s WHERE id=%s", (rate, new_status, sid))
                    conn.commit()
                    print(" Station configurations updated successfully!")
                else:
                    print("Station ID not found.")
            except ValueError:
                print(" Invalid numeric format typed.")

        elif choice == '4': # DELETE
            try:
                sid = int(input("Enter Station ID to decommission: "))
                cursor.execute("DELETE FROM station WHERE id = %s", (sid,))
                conn.commit()
                print(" Station removed from network mapping.")
            except ValueError:
                print(" Invalid entry.")

        elif choice == '5':
            cursor.close()
            conn.close()
            break
            
        cursor.close()
        conn.close()

# ==========================================
# USER PANEL: EV DRIVER PORTAL
# ==========================================
def user_panel():
    while True:
        print("\n--- PLUGPOINT DRIVER APP (USER) ---")
        print("1. Find Available Chargers Near Me")
        print("2. Filter Stations by Charger Type")
        print("3. Sort Stations by Price (Cheapest First)")
        print("4. Back to Main Menu")
        
        choice = input("\nSelect action (1-4): ").strip()
        conn = get_connection()
        if not conn: 
            print(" Database offline."); continue
        cursor = conn.cursor()

        if choice == '1': # READ ACTIVE
            cursor.execute("SELECT * FROM station WHERE status = 'Available'")
            print_table(cursor.fetchall())

        elif choice == '2': # FILTER
            print("\nAvailable Types: AC Type 2, DC Fast Charger")
            target = input("Enter charger type to filter: ").strip()
            cursor.execute("SELECT * FROM station WHERE LOWER(charger_type) LIKE LOWER(%s)", (f"%{target}%",))
            print_table(cursor.fetchall())

        elif choice == '3': # SORT
            cursor.execute("SELECT * FROM station ORDER BY price_per_kwh ASC")
            print_table(cursor.fetchall())

        elif choice == '4':
            cursor.close()
            conn.close()
            break
            
        cursor.close()
        conn.close()