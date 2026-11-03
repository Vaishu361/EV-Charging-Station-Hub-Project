
import sys
from db_connection import initialize_db
import panels

def main():
    print(" Syncing with PlugPoint EV Local Grid Engine...")
    initialize_db()  
    
    while True:
        print("\n==============================================")
        print("      WELCOME TO PLUGPOINT EV NETWORK     ")
        print("==============================================")
        print("1. Log In as Grid Operator (Admin Panel)")
        print("2. Enter as EV Driver     (User Panel)")
        print("3. Terminate Connection   (Exit)")
        
        portal_choice = input("\nChoose portal pathway (1-3): ").strip()
        
        if portal_choice == '1':
            panels.admin_panel()
        elif portal_choice == '2':
            panels.user_panel()
        elif portal_choice == '3':
            print("\nShutting down power link grids safely. Goodbye! ")
            sys.exit()
        else:
            print(" Invalid Input Route Option.")

if __name__ == "__main__":
    main()
