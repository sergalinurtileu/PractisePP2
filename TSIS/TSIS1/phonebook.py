import json
from connect import connect
from config import load_config

def execute_query(query, params=None, fetch=False, is_procedure=False):
    """
    Generic helper function to manage database connections, cursor execution, 
    and transaction commits.
    
    :param query: SQL string to execute
    :param params: Tuple of parameters for the SQL query
    :param fetch: Boolean, if True returns results from the database
    :param is_procedure: Boolean, indicates if a stored procedure is being called
    """
    config = load_config()
    try:
        # Establish connection using context managers for safe resource handling
        with connect(config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                # Commit changes for INSERT/UPDATE/DELETE/CALL operations
                conn.commit()
    except Exception as e:
        print(f"Database Error: {e}")
        return None

# --- TASK 3.2: Advanced Console Search & Filter ---

def search_all_fields():
    """Searches for contacts matching a term in names, emails, or phone numbers."""
    q = input("Enter search term (name, email, or phone): ")
    # Calls the stored DB function search_contacts
    rows = execute_query("SELECT * FROM search_contacts(%s)", (q,), fetch=True)
    
    if rows is None or len(rows) == 0:
        print("\nNo results found.")
        return

    # Formatted console output for better readability
    print(f"\n{'Name':<15} | {'Email':<25} | {'Group':<12} | {'Phones'}")
    print("-" * 95)
    for r in rows:
        name = r[0] or ""
        email = r[1] or ""
        group = r[2] or "No Group"
        phones = r[3] or ""
        print(f"{name:<15} | {email:<25} | {group:<12} | {phones}")

def filter_by_group():
    """Displays contacts belonging to a specific group."""
    print("\n--- Available Groups ---")
    groups_list = execute_query("SELECT name FROM groups", fetch=True)
    if groups_list:
        for g in groups_list: print(f"- {g[0]}")
    
    group_name = input("\nEnter group name to filter: ")
    query = """
        SELECT c.first_name, c.email, g.name 
        FROM contacts c 
        JOIN groups g ON c.group_id = g.id 
        WHERE g.name ILIKE %s
    """
    rows = execute_query(query, (group_name,), fetch=True)
    
    if rows:
        print(f"\nContacts in group '{group_name}':")
        print(f"{'Name':<15} | {'Email':<25} | {'Group'}")
        print("-" * 60)
        for r in rows:
            print(f"{r[0]:<15} | {r[1]:<25} | {r[2]}")
    else:
        print(f"\nNo contacts found in group '{group_name}'.")

def sort_contacts():
    """Allows sorting contacts dynamically by name, birthday, or creation date."""
    print("\nSort by: 1. Name | 2. Birthday | 3. Date Added")
    choice = input("Choice: ")
    order_map = {"1": "first_name", "2": "birthday", "3": "created_at"}
    col = order_map.get(choice, "first_name")
    
    rows = execute_query(f"SELECT first_name, email, birthday FROM contacts ORDER BY {col}", fetch=True)
    print(f"\n{'Name':<15} | {'Email':<25} | {'Birthday'}")
    print("-" * 60)
    for r in rows:
        bday = r[2] if r[2] else "N/A"
        print(f"{r[0]:<15} | {r[1]:<25} | {bday}")

def interactive_pagination(limit=5):
    """Navigates through contacts page-by-page using database-level offset."""
    offset = 0
    while True:
        rows = execute_query("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset), fetch=True)
        if not rows:
            print("\n--- End of list ---")
            break
            
        print(f"\n--- Page (Showing {len(rows)} results) ---")
        for r in rows:
            bday = r[2] if r[2] else "N/A"
            print(f"Name: {r[0]:<15} | Email: {r[1]:<25} | Birthday: {bday}")
        
        if len(rows) < limit:
            print("\n--- End of list ---")
            break

        user_input = input("\n[Enter] Next Page | [q] Back to Menu: ").lower()
        if user_input == 'q': break
        offset += limit

# --- PROCEDURES (TASK 3.1 & 3.2) ---

def move_contact_to_group():
    """Updates contact's group by calling the 'move_to_group' stored procedure."""
    contact = input("Enter contact name: ")
    group = input("Enter target group name: ")
    execute_query("CALL move_to_group(%s, %s)", (contact, group))
    print(f"Procedure executed: {contact} moved to {group}.")

def add_new_phone():
    """Adds a phone number to an existing contact via the 'add_phone' stored procedure."""
    contact = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    p_type = input("Enter type (mobile/home/work): ")
    execute_query("CALL add_phone(%s, %s, %s)", (contact, phone, p_type))
    print(f"Procedure executed: Added {p_type} phone to {contact}.")

# --- TASK 3.3: Import / Export ---

def export_json():
    """Exports all contacts, groups, and phone numbers into a structured JSON file."""
    query = """
        SELECT c.first_name, c.email, c.birthday, g.name, 
               json_agg(json_build_object('phone', p.phone, 'type', p.type)) 
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name;
    """
    rows = execute_query(query, fetch=True)
    data = [{"name": r[0], "email": r[1], "birthday": str(r[2]), "group": r[3], "phones": r[4]} for r in rows]
    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)
    print("\nSuccess: Exported to contacts.json")

def import_json():
    """Imports contacts from JSON and handles duplicates by prompting the user."""
    try:
        with open("contacts.json", "r") as f:
            data = json.load(f)
        config = load_config()
        with connect(config) as conn:
            with conn.cursor() as cur:
                for item in data:
                    # Check for existing record to prevent duplicates
                    cur.execute("SELECT id FROM contacts WHERE first_name = %s", (item['name'],))
                    if cur.fetchone():
                        if input(f"Overwrite {item['name']}? (y/n): ").lower() != 'y': continue
                        cur.execute("DELETE FROM contacts WHERE first_name = %s", (item['name'],))
                    
                    # Insert primary contact data
                    cur.execute("INSERT INTO contacts (first_name, email, birthday) VALUES (%s, %s, %s) RETURNING id",
                                (item['name'], item['email'], item['birthday']))
                    c_id = cur.fetchone()[0]
                    
                    # Insert associated phone numbers
                    if item['phones']:
                        for p in item['phones']:
                            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", 
                                        (c_id, p['phone'], p['type']))
            conn.commit()
        print("Import successful.")
    except Exception as e: print(f"Error: {e}")

# --- MAIN MENU ---

def menu():
    """Main application loop and navigation menu."""
    while True:
        print("\n" + "="*35)
        print("   TSIS 1: FINAL PHONEBOOK   ")
        print("="*35)
        print("1. Search (All fields)")
        print("2. Filter by Group")
        print("3. Sort Contacts")
        print("4. Paginated View")
        print("5. Export to JSON")
        print("6. Import from JSON")
        print("7. Move to Group (PROCEDURE)")
        print("8. Add Phone (PROCEDURE)")
        print("0. Exit")
        
        choice = input("\nSelect action: ")
        if choice == "1": search_all_fields()
        elif choice == "2": filter_by_group()
        elif choice == "3": sort_contacts()
        elif choice == "4": interactive_pagination()
        elif choice == "5": export_json()
        elif choice == "6": import_json()
        elif choice == "7": move_contact_to_group()
        elif choice == "8": add_new_phone()
        elif choice == "0": 
            print("Exiting application. Goodbye!")
            break
        else: print("Invalid choice. Please select 0-8.")

if __name__ == "__main__":
    menu()