import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import logging
from datetime import datetime
from hashlib import sha256
import time
import os

logging.basicConfig(
    filename=f'sports_archive_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

conn = mysql.connector.connect(
    host="<database-host>",
    user="<database-user>",
    password="<database-password>",
    database="<database-name>"
)

table_columns = {
    "suppliers": ["Supplier_ID", "Supplier_Name", "Contact_Info"],
    
    "sports_sportinfo": ["Sport_ID", "Sport_Name", "Weight", "Age", "Supplier_ID"],
    
    "equipment": ["Equipment_ID", "Equipment_Name", "Weight", "Dimensions", 
                 "Sport_ID", "Supplier_Name"],
    
    "players": ["Player_ID", "Age", "Gender", "First_Name", "Middle_Name", 
                "Last_Name", "Sponsor_Name", "Sport_ID"],
    
    "organizers": ["Organizer_Name", "Description", "Supplier_Name", 
                  "Chairman_FN", "Chairman_MN", "Chairman_LN"],
    
    "organizers_competitions": ["Organizer_Name", "Competition_Name"],
    
    "competitions": ["Competition_Name", "Location", "Duration"],
    
    "sponsors": ["Sponsor_Name", "Sport_ID"],
    
    "sponsors_budget": ["Sponsor_Name", "Budget"],
    
    "sponsors_competition": ["Sponsor_Name", "Competition_Name"],
    
    "sponsors_player": ["Sponsor_Name", "Player_ID"],
    
    "broadcasters": ["Broadcaster_Name", "Location", "Competition_Name", 
                    "Platform", "Languages"],
    
    "records": ["Player_ID", "Sport_ID", "Competition_Name", "Tally", "Duration"],
    
    "sports_sportdetails": ["Sport_Name", "Number_of_Players"]
}

def setup_database():
    try:
        cursor = conn.cursor()
        
        # Drop users table if it exists
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(64) NOT NULL,
                role VARCHAR(20) NOT NULL
            )
        """)
        
        # Create default admin user (password: admin123)
        admin_password = sha256('admin123'.encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES ('admin', %s, 'admin')
        """, (admin_password,))
        
        # Create test user (password: test123)
        test_password = sha256('test123'.encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES ('test', %s, 'viewer')
        """, (test_password,))
        
        conn.commit()
        
        # Verify users were created
        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        print("Users created successfully:")
        for user in users:
            print(f"Username: {user[0]}, Role: {user[1]}")
        
        cursor.close()
        
    except mysql.connector.Error as err:
        logging.error(f"Database setup error: {err}")
        messagebox.showerror("Error", f"Failed to setup database: {err}")

# Call setup_database after establishing connection
setup_database()

def login_page():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x400")  # Made taller for additional info
    
    
    
    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def login_as_viewer():
        login_window.destroy()
        main_app(role="viewer")

    def authenticate():
        username = username_entry.get()
        password = sha256(password_entry.get().encode()).hexdigest()
        
        try:
            cursor = conn.cursor()
            # For debugging - print the attempted login details
            print(f"Login attempt - Username: {username}, Password Hash: {password}")
            
            query = "SELECT role FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()

            if result:
                role = result[0]
                login_window.destroy()
                main_app(role=role)
            else:
                # For debugging - check what's in the database for this username
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                stored_pass = cursor.fetchone()
                cursor.close()
                
                if stored_pass:
                    print(f"Stored password hash for {username}: {stored_pass[0]}")
                else:
                    print(f"No user found with username: {username}")
                    
                messagebox.showerror("Error", "Invalid username or password.")
        except mysql.connector.Error as err:
            logging.error(f"Login error: {err}")
            messagebox.showerror("Error", "Database error during login")

    tk.Button(login_window, text="Login as Viewer", command=login_as_viewer).pack(pady=10)
    tk.Button(login_window, text="Login", command=authenticate).pack(pady=10)

    login_window.mainloop()

def main_app(role):
    # Create root window first
    root = tk.Tk()
    root.title("Advanced Sports Archive Database Viewer")
    root.geometry("1200x600")
    
    # Then set up session management
    last_activity = time.time()
    SESSION_TIMEOUT = 30 * 60  # 30 minutes
    
    def check_session():
        nonlocal last_activity
        if time.time() - last_activity > SESSION_TIMEOUT:
            root.destroy()
            messagebox.showinfo("Session Expired", "Your session has expired. Please login again.")
            login_page()
        else:
            root.after(60000, check_session)  # Check every minute
    
    def update_activity(event):
        nonlocal last_activity
        last_activity = time.time()
    
    # Bind events after root is created
    root.bind_all('<Key>', update_activity)
    root.bind_all('<Button-1>', update_activity)
    root.after(60000, check_session)
    
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    def create_table_tab(tab_name, query):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=tab_name)

        # Add search frame
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side="left", padx=5)
        
        # Add column filter
        tk.Label(search_frame, text="Filter by:").pack(side="left", padx=5)
        # Map display name to actual table name for Sports
        actual_table_name = "sports_sportinfo" if tab_name.lower() == "sports" else tab_name.lower()
        filter_column = ttk.Combobox(search_frame, values=table_columns[actual_table_name])
        filter_column.pack(side="left", padx=5)
        
        def search_records():
            search_text = search_entry.get().lower()
            filter_col = filter_column.get()
            
            for item in tree.get_children():
                values = tree.item(item)['values']
                if filter_col:
                    col_idx = table_columns[actual_table_name].index(filter_col)
                    if str(values[col_idx]).lower().find(search_text) != -1:
                        tree.reattach(item, '', 'end')
                    else:
                        tree.detach(item)
                else:
                    if any(str(value).lower().find(search_text) != -1 for value in values):
                        tree.reattach(item, '', 'end')
                    else:
                        tree.detach(item)
        
        def clear_search():
            # Clear search entry and filter
            search_entry.delete(0, tk.END)
            filter_column.set('')
            
            # Show all items that might have been hidden
            for item in tree.get_children(''):
                tree.item(item, tags=())
                tree.detach(item)
            
            try:
                cursor = conn.cursor()
                # Use the actual table name for the query
                actual_table_name = "sports_sportinfo" if tab_name.lower() == "sports" else tab_name.lower()
                cursor.execute(f"SELECT * FROM {actual_table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    tree.insert("", "end", values=row)
                cursor.close()
            except mysql.connector.Error as err:
                logging.error(f"Database error: {err}")
                messagebox.showerror("Error", f"Failed to refresh table: {err}")
            
            # Set focus back to search entry
            search_entry.focus()
        
        # Button frame for search controls
        button_frame = ttk.Frame(search_frame)
        button_frame.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Search", command=search_records).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Clear", command=clear_search).pack(side="left", padx=2)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(expand=True, fill="both")

        tree = ttk.Treeview(tree_frame)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar.pack(side="right", fill="y")
        tree.pack(expand=True, fill="both")

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        tree["columns"] = columns
        tree["show"] = "headings"
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", stretch=True)

        for row in rows:
            tree.insert("", "end", values=row)

        cursor.close()
        
        # Add CRUD controls
        create_crud_controls(frame, tab_name, tree)

    def create_crud_controls(frame, table_name, tree):
        if role != "admin":  # Only show CRUD controls for admin users
            return
        
        crud_frame = ttk.Frame(frame)
        crud_frame.pack(fill="x", padx=5, pady=5)
        
        # Add the missing get_foreign_key_values function
        def get_foreign_key_values(table_name, column):
            try:
                cursor = conn.cursor()
                
                # Map common foreign key patterns to their tables and columns
                fk_mappings = {
                    'Sport_ID': ('sports_sportinfo', 'Sport_ID'),
                    'Supplier_ID': ('suppliers', 'Supplier_ID'),
                    'Supplier_Name': ('suppliers', 'Supplier_Name'),
                    'Player_ID': ('players', 'Player_ID'),
                    'Competition_Name': ('competitions', 'Competition_Name'),
                    'Sponsor_Name': ('sponsors', 'Sponsor_Name'),
                    'Organizer_Name': ('organizers', 'Organizer_Name'),
                    'Broadcaster_Name': ('broadcasters', 'Broadcaster_Name')
                }
                
                if column in fk_mappings:
                    ref_table, ref_column = fk_mappings[column]
                    cursor.execute(f"SELECT DISTINCT {ref_column} FROM {ref_table}")
                    values = [str(row[0]) for row in cursor.fetchall()]
                    cursor.close()
                    return values
                return None
                
            except mysql.connector.Error as err:
                logging.error(f"Error fetching foreign key values: {err}")
                return None
        
        # Delete functionality
        def delete_record():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a record to delete")
                return
            
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
                try:
                    cursor = conn.cursor()
                    cursor.execute("START TRANSACTION")
                    current_values = tree.item(selected_item[0])['values']
                    
                    if table_name.lower() == "competitions":
                        # Delete related records first
                        cursor.execute("DELETE FROM organizers_competitions WHERE Competition_Name = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM sponsors_competition WHERE Competition_Name = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM broadcasters WHERE Competition_Name = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM records WHERE Competition_Name = %s", 
                                     (current_values[0],))
                        # Delete main record
                        cursor.execute("DELETE FROM competitions WHERE Competition_Name = %s", 
                                     (current_values[0],))
                        
                    elif table_name.lower() == "players":
                        # Delete related records first
                        cursor.execute("DELETE FROM sponsors_player WHERE Player_ID = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM records WHERE Player_ID = %s", 
                                     (current_values[0],))
                        # Delete main record
                        cursor.execute("DELETE FROM players WHERE Player_ID = %s", 
                                     (current_values[0],))
                        
                    elif table_name.lower() == "sports_sportinfo":
                        # Delete related records first
                        cursor.execute("DELETE FROM equipment WHERE Sport_ID = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM players WHERE Sport_ID = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM records WHERE Sport_ID = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM sports_sportdetails WHERE Sport_Name = %s", 
                                     (current_values[1],))  # Sport_Name is second column
                        # Delete main record
                        cursor.execute("DELETE FROM sports_sportinfo WHERE Sport_ID = %s", 
                                     (current_values[0],))
                        
                    elif table_name.lower() == "sponsors":
                        # Delete related records first
                        cursor.execute("DELETE FROM sponsors_budget WHERE Sponsor_Name = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM sponsors_competition WHERE Sponsor_Name = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM sponsors_player WHERE Sponsor_Name = %s", 
                                     (current_values[0],))
                        # Delete main record
                        cursor.execute("DELETE FROM sponsors WHERE Sponsor_Name = %s", 
                                     (current_values[0],))
                        
                    elif table_name.lower() == "organizers":
                        # Delete related records first
                        cursor.execute("DELETE FROM organizers_competitions WHERE Organizer_Name = %s", 
                                     (current_values[0],))
                        # Delete main record
                        cursor.execute("DELETE FROM organizers WHERE Organizer_Name = %s", 
                                     (current_values[0],))
                        
                    elif table_name.lower() == "broadcasters":
                        # Delete main record
                        cursor.execute("DELETE FROM broadcasters WHERE Broadcaster_Name = %s", 
                                     (current_values[0],))
                        
                    elif table_name.lower() == "suppliers":
                        # Delete related records first
                        cursor.execute("DELETE FROM equipment WHERE Supplier_Name = %s", 
                                     (current_values[0],))
                        cursor.execute("DELETE FROM organizers WHERE Supplier_Name = %s", 
                                     (current_values[0],))
                        # Delete main record
                        cursor.execute("DELETE FROM suppliers WHERE Supplier_Name = %s", 
                                     (current_values[0],))
                        
                    conn.commit()
                    refresh_table(tree, table_name)
                    messagebox.showinfo("Success", "Record deleted successfully!")
                    
                except mysql.connector.Error as err:
                    conn.rollback()
                    logging.error(f"Database error: {err}")
                    messagebox.showerror("Error", f"Failed to delete record: {err}")
                finally:
                    cursor.close()
        
        # Update functionality
        def show_update_dialog():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a record to update")
                return
            
            update_window = tk.Toplevel()
            update_window.title(f"Update {table_name}")
            
            # Get current values
            current_values = tree.item(selected_item[0])['values']
            
            # Create entry fields with current values
            entries = {}
            row = 0
            
            # Use the columns from the current table view
            fields = table_columns[table_name.lower()]
            
            # Create entry fields
            for field in fields:
                tk.Label(update_window, text=field).grid(row=row, column=0, padx=5, pady=5)
                
                # Check if field is a foreign key
                fk_values = get_foreign_key_values(table_name, field)
                
                if fk_values:
                    # Create combobox for foreign key fields
                    entry = ttk.Combobox(update_window, values=fk_values)
                    if current_values[row] is not None:
                        entry.set(current_values[row])
                else:
                    # Create regular entry for non-foreign key fields
                    entry = tk.Entry(update_window)
                    if current_values[row] is not None:
                        entry.insert(0, current_values[row])
                
                entry.grid(row=row, column=1, padx=5, pady=5)
                entries[field] = entry
                row += 1
            
            def update_record():
                try:
                    cursor = conn.cursor()
                    cursor.execute("START TRANSACTION")
                    
                    values = {field: entry.get() for field, entry in entries.items()}
                    
                    # Build UPDATE query dynamically based on table columns
                    set_clause = ", ".join([f"{field} = %s" for field in fields[1:]])  # Skip first field (usually PK)
                    where_clause = f"{fields[0]} = %s"  # First field is usually the PK
                    
                    query = f"UPDATE {table_name.lower()} SET {set_clause} WHERE {where_clause}"
                    
                    # Create parameters list: all values except PK + PK value at the end
                    params = [values[field] for field in fields[1:]] + [values[fields[0]]]
                    
                    # Execute the main update
                    cursor.execute(query, params)
                    
                    # Handle related tables based on the table being updated
                    if table_name.lower() == "competitions":
                        # Update related tables if they exist
                        if 'Organizer_Name' in values and values['Organizer_Name']:
                            cursor.execute("""
                                INSERT INTO organizers_competitions (Organizer_Name, Competition_Name)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE Organizer_Name = VALUES(Organizer_Name)
                            """, (values['Organizer_Name'], values['Competition_Name']))
                        
                    elif table_name.lower() == "players":
                        # Update sponsors_player if Sponsor_Name exists
                        if 'Sponsor_Name' in values and values['Sponsor_Name']:
                            cursor.execute("""
                                INSERT INTO sponsors_player (Sponsor_Name, Player_ID)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE Sponsor_Name = VALUES(Sponsor_Name)
                            """, (values['Sponsor_Name'], values['Player_ID']))
                    
                    elif table_name.lower() == "sports_sportinfo":
                        # Update sports_sportdetails if Number_of_Players exists
                        if 'Number_of_Players' in values:
                            cursor.execute("""
                                INSERT INTO sports_sportdetails (Sport_Name, Number_of_Players)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE Number_of_Players = VALUES(Number_of_Players)
                            """, (values['Sport_Name'], values['Number_of_Players']))
                    
                    elif table_name.lower() == "sponsors":
                        # Update sponsors_budget if Budget exists
                        if 'Budget' in values:
                            cursor.execute("""
                                INSERT INTO sponsors_budget (Sponsor_Name, Budget)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE Budget = VALUES(Budget)
                            """, (values['Sponsor_Name'], values['Budget']))
                    
                    conn.commit()
                    refresh_table(tree, table_name)
                    update_window.destroy()
                    messagebox.showinfo("Success", "Record updated successfully!")
                    
                except mysql.connector.Error as err:
                    conn.rollback()
                    logging.error(f"Database error: {err}")
                    messagebox.showerror("Error", f"Failed to update record: {err}")
                finally:
                    cursor.close()
            
            tk.Button(update_window, text="Update", command=update_record).grid(
                row=row, column=0, columnspan=2, pady=10)
        
        # Add CRUD buttons
        ttk.Button(crud_frame, text="Update", command=show_update_dialog).pack(side="left", padx=5)
        ttk.Button(crud_frame, text="Delete", command=delete_record).pack(side="left", padx=5)

        def export_to_csv():
            import csv
            from tkinter import filedialog
            
            file_path = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[("CSV files", "*.csv")]
            )
            
            if file_path:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    # Write headers
                    writer.writerow(table_columns[table_name.lower()])
                    # Write data
                    for item in tree.get_children():
                        writer.writerow(tree.item(item)['values'])
                messagebox.showinfo("Success", "Data exported successfully!")
        
        ttk.Button(crud_frame, text="Export CSV", command=export_to_csv).pack(side="left", padx=5)

        def import_from_csv():
            import csv
            from tkinter import filedialog
            
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv")]
            )
            
            if file_path:
                try:
                    with open(file_path, 'r') as file:
                        csv_reader = csv.reader(file)
                        headers = next(csv_reader)  # Skip header row
                        
                        cursor = conn.cursor()
                        for row in csv_reader:
                            columns = ", ".join(table_columns[table_name.lower()])
                            placeholders = ", ".join(["%s"] * len(row))
                            query = f"INSERT INTO {table_name.lower()} ({columns}) VALUES ({placeholders})"
                            cursor.execute(query, row)
                        
                        conn.commit()
                        cursor.close()
                        refresh_table(tree, table_name)
                        messagebox.showinfo("Success", "Data imported successfully!")
                except Exception as e:
                    logging.error(f"Import error: {e}")
                    messagebox.showerror("Error", f"Failed to import data: {e}")
        
        ttk.Button(crud_frame, text="Import CSV", command=import_from_csv).pack(side="left", padx=5)

    def refresh_table(tree, table_name):
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Reload data
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name.lower()}")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        cursor.close()

    for table_name, table_query in {
        "Broadcasters": "SELECT * FROM broadcasters;",
        "Competitions": "SELECT * FROM competitions;",
        "Equipment": "SELECT * FROM equipment;",
        "Organizers": "SELECT * FROM organizers;",
        "Players": "SELECT * FROM players;",
        "Records": "SELECT * FROM records;",
        "Sponsors": "SELECT * FROM sponsors;",
        "Sports": "SELECT * FROM sports_sportinfo;",
        "Suppliers": "SELECT * FROM suppliers;"
    }.items():
        create_table_tab(table_name, table_query)

    def advanced_search_tab():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Advanced Search")

        # Frame for table selection
        tables_frame = ttk.LabelFrame(frame, text="Select Tables")
        tables_frame.pack(fill="x", padx=5, pady=5)

        selected_tables = []
        table_entries = []

        def add_table_selection():
            table_frame = ttk.Frame(tables_frame)
            table_frame.pack(fill="x", padx=5, pady=2)
            
            table_var = tk.StringVar()
            table_combo = ttk.Combobox(table_frame, values=list(table_columns.keys()), 
                                     textvariable=table_var)
            table_combo.pack(side="left", padx=2)
            
            def remove_table():
                table_frame.destroy()
                if table_var.get() in selected_tables:
                    selected_tables.remove(table_var.get())
                update_available_columns()
            
            def on_table_select(event):
                if table_var.get() not in selected_tables:
                    selected_tables.append(table_var.get())
                update_available_columns()
            
            ttk.Button(table_frame, text="-", width=3, 
                      command=remove_table).pack(side="left", padx=2)
            
            table_combo.bind("<<ComboboxSelected>>", on_table_select)
            table_entries.append((table_frame, table_var))

        ttk.Button(tables_frame, text="+", width=3, 
                  command=add_table_selection).pack(pady=5)

        # Frame for column selection
        columns_frame = ttk.LabelFrame(frame, text="Select Output Columns")
        columns_frame.pack(fill="x", padx=5, pady=5)

        # Split into two frames: available and selected columns
        available_cols_frame = ttk.Frame(columns_frame)
        available_cols_frame.pack(side="left", fill="both", expand=True)
        selected_cols_frame = ttk.Frame(columns_frame)
        selected_cols_frame.pack(side="right", fill="both", expand=True)

        # Available columns list
        tk.Label(available_cols_frame, text="Available Columns:").pack()
        available_columns_listbox = tk.Listbox(available_cols_frame, height=6)
        available_columns_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Selected columns list
        tk.Label(selected_cols_frame, text="Selected Columns:").pack()
        selected_columns_listbox = tk.Listbox(selected_cols_frame, height=6)
        selected_columns_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Buttons frame
        buttons_frame = ttk.Frame(columns_frame)
        buttons_frame.pack(fill="x", pady=5)

        def add_selected_column():
            selection = available_columns_listbox.curselection()
            if selection:
                idx = selection[0]
                column = available_columns_listbox.get(idx)
                if column not in selected_columns_listbox.get(0, tk.END):
                    selected_columns_listbox.insert(tk.END, column)

        def remove_selected_column():
            selection = selected_columns_listbox.curselection()
            if selection:
                selected_columns_listbox.delete(selection)

        # Add and Remove buttons
        ttk.Button(buttons_frame, text="+", width=3, 
                  command=add_selected_column).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="-", width=3, 
                  command=remove_selected_column).pack(side="left", padx=5)

        def update_available_columns():
            available_columns_listbox.delete(0, tk.END)
            available_columns = []
            for table in selected_tables:
                for col in table_columns[table]:
                    available_columns.append(f"{table}.{col}")
            for col in available_columns:
                available_columns_listbox.insert(tk.END, col)

        # Frame for constraints
        constraints_frame = ttk.LabelFrame(frame, text="Add Constraints")
        constraints_frame.pack(fill="x", padx=5, pady=5)

        constraint_widgets = []

        def add_constraint():
            constraint_frame = ttk.Frame(constraints_frame)
            constraint_frame.pack(fill="x", padx=5, pady=2)
            
            # Get all available columns from selected tables
            all_columns = []
            for table in selected_tables:
                for col in table_columns[table]:
                    all_columns.append(f"{table}.{col}")
            
            # Column selection
            column_var = tk.StringVar()
            column_combo = ttk.Combobox(constraint_frame, values=all_columns, 
                                      textvariable=column_var)
            column_combo.pack(side="left", padx=2)
            
            # Operator selection
            op_var = tk.StringVar()
            op_combo = ttk.Combobox(constraint_frame, 
                                   values=["=", ">", "<", ">=", "<=", "!=", "LIKE"],
                                   textvariable=op_var, width=5)
            op_combo.pack(side="left", padx=2)
            
            # Value entry
            value_var = tk.StringVar()
            value_entry = ttk.Entry(constraint_frame, textvariable=value_var)
            value_entry.pack(side="left", padx=2)
            
            def remove_constraint():
                constraint_frame.destroy()
                constraint_widgets.remove((column_var, op_var, value_var))
            
            ttk.Button(constraint_frame, text="-", width=3, 
                      command=remove_constraint).pack(side="left", padx=2)
            
            constraint_widgets.append((column_var, op_var, value_var))

        ttk.Button(constraints_frame, text="+", width=3, 
                  command=add_constraint).pack(pady=5)

        def execute_query():
            try:
                # Get selected output columns from the selected_columns_listbox
                output_columns = list(selected_columns_listbox.get(0, tk.END))
                if not output_columns:
                    messagebox.showerror("Error", "Please select at least one output column")
                    return

                # Build the query with DISTINCT to remove duplicates
                select_clause = "DISTINCT " + ", ".join(output_columns)
                from_clause = ", ".join(selected_tables)
                
                # Build WHERE clause from constraints
                where_conditions = []
                for col_var, op_var, val_var in constraint_widgets:
                    if col_var.get() and op_var.get() and val_var.get():
                        if op_var.get() == "LIKE":
                            where_conditions.append(
                                f"{col_var.get()} LIKE '%{val_var.get()}%'")
                        else:
                            where_conditions.append(
                                f"{col_var.get()} {op_var.get()} '{val_var.get()}'")

                # Build JOIN conditions
                join_conditions = []
                for i, table1 in enumerate(selected_tables):
                    for table2 in selected_tables[i+1:]:
                        # Define custom join conditions based on table relationships
                        if (table1.lower(), table2.lower()) in [
                            ("broadcasters", "competitions"),
                            ("competitions", "broadcasters")
                        ]:
                            join_conditions.append(
                                f"{table1}.Competition_Name = {table2}.Competition_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("equipment", "sports_sportinfo"),
                            ("sports_sportinfo", "equipment")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sport_ID = {table2}.Sport_ID"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("equipment", "suppliers"),
                            ("suppliers", "equipment")
                        ]:
                            join_conditions.append(
                                f"{table1}.Supplier_Name = {table2}.Supplier_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("organizers", "suppliers"),
                            ("suppliers", "organizers")
                        ]:
                            join_conditions.append(
                                f"{table1}.Supplier_Name = {table2}.Supplier_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("organizers_competitions", "organizers"),
                            ("organizers", "organizers_competitions")
                        ]:
                            join_conditions.append(
                                f"{table1}.Organizer_Name = {table2}.Organizer_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("organizers_competitions", "competitions"),
                            ("competitions", "organizers_competitions")
                        ]:
                            join_conditions.append(
                                f"{table1}.Competition_Name = {table2}.Competition_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("players", "sports_sportinfo"),
                            ("sports_sportinfo", "players")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sport_ID = {table2}.Sport_ID"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("records", "players"),
                            ("players", "records")
                        ]:
                            join_conditions.append(
                                f"{table1}.Player_ID = {table2}.Player_ID"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("records", "sports_sportinfo"),
                            ("sports_sportinfo", "records")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sport_ID = {table2}.Sport_ID"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("records", "competitions"),
                            ("competitions", "records")
                        ]:
                            join_conditions.append(
                                f"{table1}.Competition_Name = {table2}.Competition_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("sponsors", "sports_sportinfo"),
                            ("sports_sportinfo", "sponsors")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sport_ID = {table2}.Sport_ID"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("sponsors_budget", "sponsors"),
                            ("sponsors", "sponsors_budget")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sponsor_Name = {table2}.Sponsor_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("sponsors_competition", "sponsors"),
                            ("sponsors", "sponsors_competition")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sponsor_Name = {table2}.Sponsor_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("sponsors_competition", "competitions"),
                            ("competitions", "sponsors_competition")
                        ]:
                            join_conditions.append(
                                f"{table1}.Competition_Name = {table2}.Competition_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("sponsors_player", "sponsors"),
                            ("sponsors", "sponsors_player")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sponsor_Name = {table2}.Sponsor_Name"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("sponsors_player", "players"),
                            ("players", "sponsors_player")
                        ]:
                            join_conditions.append(
                                f"{table1}.Player_ID = {table2}.Player_ID"
                            )
                        elif (table1.lower(), table2.lower()) in [
                            ("sports_sportdetails", "sports_sportinfo"),
                            ("sports_sportinfo", "sports_sportdetails")
                        ]:
                            join_conditions.append(
                                f"{table1}.Sport_Name = {table2}.Sport_Name"
                            )

                # Combine all conditions
                all_conditions = join_conditions + where_conditions
                where_clause = " AND ".join(all_conditions) if all_conditions else "1=1"

                query = f"""
                    SELECT {select_clause}
                    FROM {from_clause}
                    WHERE {where_clause}
                """

                # Execute query
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()

                # Display results
                result_window = tk.Toplevel()
                result_window.title("Search Results")
                
                # Clean up column names for display (remove table names)
                display_columns = [col.split('.')[-1] for col in output_columns]
                
                # Create Treeview
                tree = ttk.Treeview(result_window)
                tree["columns"] = display_columns
                tree["show"] = "headings"
                
                # Set column headings with cleaned names
                for col in display_columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=100)
                
                # Add scrollbars
                vsb = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
                hsb = ttk.Scrollbar(result_window, orient="horizontal", command=tree.xview)
                tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
                
                # Grid layout
                tree.grid(row=0, column=0, sticky="nsew")
                vsb.grid(row=0, column=1, sticky="ns")
                hsb.grid(row=1, column=0, sticky="ew")
                
                # Configure grid weights
                result_window.grid_rowconfigure(0, weight=1)
                result_window.grid_columnconfigure(0, weight=1)
                
                # Insert data
                for row in results:
                    tree.insert("", "end", values=row)
                
                # Add export button
                def export_results():
                    file_path = filedialog.asksaveasfilename(
                        defaultextension='.csv',
                        filetypes=[("CSV files", "*.csv")]
                    )
                    if file_path:
                        with open(file_path, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(display_columns)  # Use cleaned column names
                            for row in results:
                                writer.writerow(row)
                        messagebox.showinfo("Success", "Results exported successfully!")
                
                ttk.Button(result_window, text="Export to CSV", 
                          command=export_results).grid(row=2, column=0, pady=5)

            except mysql.connector.Error as err:
                logging.error(f"Query error: {err}")
                messagebox.showerror("Error", f"Query failed: {err}")

        # Execute button
        ttk.Button(frame, text="Execute Query", 
                  command=execute_query).pack(pady=10)

        # Add initial table selection
        add_table_selection()

    def create_visualization_tab():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Analytics")
        
        # Controls frame
        controls_frame = ttk.Frame(frame)
        controls_frame.pack(fill="x", padx=5, pady=5)
        
        # Table and Column selection
        tk.Label(controls_frame, text="Select Table:").pack(side="left", padx=5)
        table_menu = ttk.Combobox(controls_frame, values=[
            "broadcasters", "competitions", "equipment", "organizers",
            "players", "records", "sponsors", "sports_sportinfo", "suppliers"
        ])
        table_menu.pack(side="left", padx=5)
        
        tk.Label(controls_frame, text="Select Column:").pack(side="left", padx=5)
        column_menu = ttk.Combobox(controls_frame)
        
        # Chart type selection
        tk.Label(controls_frame, text="Chart Type:").pack(side="left", padx=5)
        chart_type = ttk.Combobox(controls_frame, values=[
            "Bar Chart", "Pie Chart", "Line Chart", "Histogram"
        ])
        chart_type.set("Bar Chart")
        chart_type.pack(side="left", padx=5)
        
        def plot_data():
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import numpy as np
            
            selected_table = table_menu.get()
            selected_column = column_menu.get()
            selected_chart = chart_type.get()
            
            if not (selected_table and selected_column):
                messagebox.showwarning("Warning", "Please select both table and column")
                return
            
            try:
                cursor = conn.cursor()
                cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
                columns = [column[0] for column in cursor.fetchall()]
                
                if selected_column not in columns:
                    messagebox.showerror("Error", f"Column '{selected_column}' not found in table '{selected_table}'")
                    return
                
                # Get data based on column type
                cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                             f"WHERE TABLE_NAME = '{selected_table}' AND COLUMN_NAME = '{selected_column}'")
                data_type = cursor.fetchone()[0]
                
                if data_type in ('int', 'decimal', 'float', 'double'):
                    # Numeric data
                    cursor.execute(f"SELECT {selected_column} FROM {selected_table} WHERE {selected_column} IS NOT NULL")
                    numeric_data = [row[0] for row in cursor.fetchall()]
                    
                    # Clear previous plot
                    for widget in plot_frame.winfo_children():
                        widget.destroy()
                    
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                    
                    # Statistical summary
                    stats_frame = ttk.LabelFrame(plot_frame, text="Statistical Summary")
                    stats_frame.pack(fill="x", padx=5, pady=5)
                    
                    mean_val = np.mean(numeric_data)
                    median_val = np.median(numeric_data)
                    std_val = np.std(numeric_data)
                    min_val = np.min(numeric_data)
                    max_val = np.max(numeric_data)
                    
                    stats_text = f"Mean: {mean_val:.2f}\n"
                    stats_text += f"Median: {median_val:.2f}\n"
                    stats_text += f"Std Dev: {std_val:.2f}\n"
                    stats_text += f"Min: {min_val:.2f}\n"
                    stats_text += f"Max: {max_val:.2f}"
                    
                    tk.Label(stats_frame, text=stats_text).pack(pady=5)
                    
                    # Histogram
                    ax1.hist(numeric_data, bins='auto', alpha=0.7)
                    ax1.set_title(f"Distribution of {selected_column}")
                    ax1.set_xlabel(selected_column)
                    ax1.set_ylabel("Frequency")
                    
                    # Box plot
                    ax2.boxplot(numeric_data)
                    ax2.set_title(f"Box Plot of {selected_column}")
                    
                else:
                    # Categorical data
                    cursor.execute(f"""
                        SELECT {selected_column}, COUNT(*) as count 
                        FROM {selected_table} 
                        WHERE {selected_column} IS NOT NULL
                        GROUP BY {selected_column}
                        ORDER BY count DESC
                        LIMIT 10
                    """)
                    data = cursor.fetchall()
                    
                    # Clear previous plot
                    for widget in plot_frame.winfo_children():
                        widget.destroy()
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    labels = [str(row[0]) if row[0] is not None else 'None' for row in data]
                    values = [row[1] for row in data]
                    
                    if selected_chart == "Bar Chart":
                        bars = ax.bar(labels, values)
                        ax.set_title(f"Top 10 {selected_column} Distribution")
                        ax.tick_params(axis='x', rotation=45)
                        
                        # Add value labels
                        for bar in bars:
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width()/2., height,
                                    f'{int(height)}',
                                    ha='center', va='bottom')
                    
                    elif selected_chart == "Pie Chart":
                        ax.pie(values, labels=labels, autopct='%1.1f%%')
                        ax.set_title(f"{selected_column} Distribution")
                    
                    elif selected_chart == "Line Chart":
                        ax.plot(labels, values, marker='o')
                        ax.set_title(f"Trend of {selected_column}")
                        ax.tick_params(axis='x', rotation=45)
                    
                plt.tight_layout()
                
                # Create canvas
                canvas_frame = ttk.Frame(plot_frame)
                canvas_frame.pack(fill="both", expand=True)
                
                canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
                # Add export button
                def export_plot():
                    file_path = filedialog.asksaveasfilename(
                        defaultextension='.png',
                        filetypes=[("PNG files", ".png"), ("All files", ".*")]
                    )
                    if file_path:
                        fig.savefig(file_path, dpi=300, bbox_inches='tight')
                        messagebox.showinfo("Success", "Plot exported successfully!")
                
                ttk.Button(plot_frame, text="Export Plot", command=export_plot).pack(pady=5)
                
            except mysql.connector.Error as err:
                logging.error(f"Database error in visualization: {err}")
                messagebox.showerror("Error", f"Failed to generate visualization: {err}")
            except Exception as e:
                logging.error(f"Visualization error: {e}")
                messagebox.showerror("Error", f"Failed to create visualization: {e}")
        
        def update_columns(event):
            try:
                selected_table = table_menu.get()
                if selected_table:
                    cursor = conn.cursor()
                    cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
                    columns = [column[0] for column in cursor.fetchall()]
                    column_menu['values'] = columns
                    cursor.close()
            except mysql.connector.Error as err:
                logging.error(f"Failed to fetch columns: {err}")
                messagebox.showerror("Error", f"Failed to fetch columns: {err}")
        
        table_menu.bind("<<ComboboxSelected>>", update_columns)
        column_menu.pack(side="left", padx=5)
        
        ttk.Button(controls_frame, text="Generate Plot", command=plot_data).pack(side="left", padx=5)
        
        # Plot frame
        plot_frame = ttk.Frame(frame)
        plot_frame.pack(fill="both", expand=True)

    def create_theme_toggle(root):
        def toggle_theme():
            style = ttk.Style()
            if style.theme_use() == 'default':
                style.theme_use('clam')
                root.configure(bg='#2d2d2d')
                style.configure("Treeview", background="#2d2d2d", 
                              fieldbackground="#2d2d2d", foreground="white")
            else:
                style.theme_use('default')
                root.configure(bg='#f0f0f0')
                style.configure("Treeview", background="white", 
                              fieldbackground="white", foreground="black")
        
        theme_button = ttk.Button(root, text="Toggle Theme", command=toggle_theme)
        theme_button.pack(pady=5)

    def create_backup_button(root):
        def backup_database():
            from datetime import datetime
            import os
            
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{backup_dir}/sportsarchive_backup_{timestamp}.sql"
            
            try:
                os.system(f"mysqldump -u root -pUdit@2002 sportsarchive > {backup_file}")
                messagebox.showinfo("Success", f"Backup created successfully at {backup_file}")
            except Exception as e:
                logging.error(f"Backup error: {e}")
                messagebox.showerror("Error", f"Failed to create backup: {e}")
        
        if role == "admin":
            ttk.Button(root, text="Backup Database", command=backup_database).pack(pady=5)

    def create_sql_query_tab():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Custom Query")
        
        query_text = tk.Text(frame, height=10)
        query_text.pack(fill="x", padx=5, pady=5)
        
        def execute_custom_query():
            query = query_text.get("1.0", tk.END).strip()
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                
                if query.lower().startswith("select"):
                    results = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    display_results(results, columns)
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Query executed successfully!")
                    
                cursor.close()
            except Exception as e:
                logging.error(f"Query error: {e}")
                messagebox.showerror("Error", f"Query failed: {e}")
        
        ttk.Button(frame, text="Execute Query", command=execute_custom_query).pack(pady=5)

    def create_insert_tab():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Insert Data")
        
        # Add this function inside create_insert_tab
        def get_reference_values(column):
            try:
                cursor = conn.cursor()
                
                # Map common foreign key patterns to their tables and columns
                fk_mappings = {
                    'Sport_ID': ('sports_sportinfo', 'Sport_ID'),
                    'Sport_Name': ('sports_sportinfo', 'Sport_Name'),
                    'Supplier_ID': ('suppliers', 'Supplier_ID'),
                    'Supplier_Name': ('suppliers', 'Supplier_Name'),
                    'Player_ID': ('players', 'Player_ID'),
                    'Competition_Name': ('competitions', 'Competition_Name'),
                    'Sponsor_Name': ('sponsors', 'Sponsor_Name'),
                    'Organizer_Name': ('organizers', 'Organizer_Name'),
                    'Broadcaster_Name': ('broadcasters', 'Broadcaster_Name')
                }
                
                if column in fk_mappings:
                    ref_table, ref_column = fk_mappings[column]
                    cursor.execute(f"SELECT DISTINCT {ref_column} FROM {ref_table}")
                    values = [str(row[0]) for row in cursor.fetchall()]
                    cursor.close()
                    return values
                return None
                
            except mysql.connector.Error as err:
                logging.error(f"Error fetching reference values: {err}")
                return None
        
        # Top frame for table selection
        selection_frame = ttk.Frame(frame)
        selection_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(selection_frame, text="Select Table:").pack(side="left", padx=5)
        
        # Define unnormalized view of tables with all possible attributes
        unnormalized_tables = {
            "Competitions View": [
                "Competition_Name", "Location", "Duration",
                "Organizer_Name", "Sponsor_Name", 
                "Broadcaster_Name", "Platform", "Languages"
            ],
            "Players View": [
                "Player_ID", "First_Name", "Middle_Name", "Last_Name",
                "Age", "Gender", "Sport_ID", "Sport_Name",
                "Sponsor_Name", "Competition_Name"
            ],
            "Sports View": [
                "Sport_ID", "Sport_Name", "Weight", "Age",
                "Supplier_ID", "Supplier_Name", "Equipment_Name",
                "Number_of_Players"
            ],
            "Sponsors View": [
                "Sponsor_Name", "Sport_ID", "Sport_Name",
                "Budget", "Competition_Name", "Player_ID"
            ]
        }
        
        table_combo = ttk.Combobox(selection_frame, values=list(unnormalized_tables.keys()))
        table_combo.pack(side="left", padx=5)
        
        # Frame for form
        form_canvas = tk.Canvas(frame)
        form_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=form_canvas.yview)
        form_frame = ttk.Frame(form_canvas)
        
        form_frame.bind(
            "<Configure>",
            lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all"))
        )
        
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw")
        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        
        entries = {}
        
        def create_form(event=None):
            # Clear previous form
            for widget in form_frame.winfo_children():
                widget.destroy()
            entries.clear()
            
            selected_table = table_combo.get()
            if not selected_table:
                return
            
            # Create entry fields for each attribute
            for i, column in enumerate(unnormalized_tables[selected_table]):
                ttk.Label(form_frame, text=column).grid(row=i, column=0, padx=5, pady=5)
                
                # Use regular Entry widget for all fields
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries[column] = entry
                
                # Add a hint label for required fields
                if column.endswith('_ID') or column.endswith('_Name'):
                    ttk.Label(form_frame, text="(Required)", 
                             foreground="red").grid(row=i, column=2, padx=5, pady=5)
            
            def insert_data():
                try:
                    cursor = conn.cursor()
                    cursor.execute("START TRANSACTION")
                    
                    values = {column: entry.get() for column, entry in entries.items()}
                    
                    if selected_table == "Competitions View":
                        # First ensure organizer exists if provided
                        if values.get('Organizer_Name'):
                            cursor.execute("""
                                INSERT IGNORE INTO organizers (Organizer_Name)
                                VALUES (%s)
                            """, (values['Organizer_Name'],))
                        
                        # Ensure sponsor exists if provided
                        if values.get('Sponsor_Name'):
                            cursor.execute("""
                                INSERT IGNORE INTO sponsors (Sponsor_Name, Sport_ID)
                                VALUES (%s, NULL)
                            """, (values['Sponsor_Name'],))
                        
                        # Insert into competitions
                        cursor.execute("""
                            INSERT INTO competitions (Competition_Name, Location, Duration)
                            VALUES (%s, %s, %s)
                        """, (values['Competition_Name'], values['Location'], values['Duration']))
                        
                        # Insert organizer relationship if provided
                        if values.get('Organizer_Name'):
                            cursor.execute("""
                                INSERT INTO organizers_competitions (Organizer_Name, Competition_Name)
                                VALUES (%s, %s)
                            """, (values['Organizer_Name'], values['Competition_Name']))
                        
                        # Insert sponsor relationship if provided
                        if values.get('Sponsor_Name'):
                            cursor.execute("""
                                INSERT INTO sponsors_competition (Sponsor_Name, Competition_Name)
                                VALUES (%s, %s)
                            """, (values['Sponsor_Name'], values['Competition_Name']))
                        
                        # Insert broadcaster if provided
                        if values.get('Broadcaster_Name'):
                            cursor.execute("""
                                INSERT INTO broadcasters 
                                (Broadcaster_Name, Location, Competition_Name, Platform, Languages)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (values['Broadcaster_Name'], values['Location'], 
                                  values['Competition_Name'], values['Platform'], 
                                  values['Languages']))
                    
                    elif selected_table == "Players View":
                        # Ensure sport exists
                        if values.get('Sport_ID'):
                            cursor.execute("""
                                INSERT IGNORE INTO sports_sportinfo (Sport_ID, Sport_Name)
                                VALUES (%s, %s)
                            """, (values['Sport_ID'], values.get('Sport_Name', f'Sport_{values["Sport_ID"]}')))
                        
                        # Ensure sponsor exists
                        if values.get('Sponsor_Name'):
                            cursor.execute("""
                                INSERT IGNORE INTO sponsors (Sponsor_Name, Sport_ID)
                                VALUES (%s, %s)
                            """, (values['Sponsor_Name'], values.get('Sport_ID')))
                        
                        # Insert player
                        cursor.execute("""
                            INSERT INTO players 
                            (Player_ID, Age, Gender, First_Name, Middle_Name, Last_Name, 
                             Sponsor_Name, Sport_ID)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (values['Player_ID'], values['Age'], values['Gender'],
                              values['First_Name'], values['Middle_Name'], values['Last_Name'],
                              values['Sponsor_Name'], values['Sport_ID']))
                        
                        # Insert sponsor relationship
                        if values.get('Sponsor_Name'):
                            cursor.execute("""
                                INSERT IGNORE INTO sponsors_player (Sponsor_Name, Player_ID)
                                VALUES (%s, %s)
                            """, (values['Sponsor_Name'], values['Player_ID']))
                    
                    elif selected_table == "Sports View":
                        # Ensure supplier exists
                        if values.get('Supplier_ID'):
                            cursor.execute("""
                                INSERT IGNORE INTO suppliers (Supplier_ID, Supplier_Name)
                                VALUES (%s, %s)
                            """, (values['Supplier_ID'], values.get('Supplier_Name', f'Supplier_{values["Supplier_ID"]}')))
                        
                        # Insert sport
                        cursor.execute("""
                            INSERT INTO sports_sportinfo 
                            (Sport_ID, Sport_Name, Weight, Age, Supplier_ID)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (values['Sport_ID'], values['Sport_Name'], values['Weight'],
                              values['Age'], values['Supplier_ID']))
                        
                        # Insert sport details
                        cursor.execute("""
                            INSERT INTO sports_sportdetails (Sport_Name, Number_of_Players)
                            VALUES (%s, %s)
                        """, (values['Sport_Name'], values['Number_of_Players']))
                    
                    elif selected_table == "Sponsors View":
                        # Ensure sport exists
                        if values.get('Sport_ID'):
                            cursor.execute("""
                                INSERT IGNORE INTO sports_sportinfo (Sport_ID, Sport_Name)
                                VALUES (%s, %s)
                            """, (values['Sport_ID'], values.get('Sport_Name', f'Sport_{values["Sport_ID"]}')))
                        
                        # Insert sponsor
                        cursor.execute("""
                            INSERT INTO sponsors (Sponsor_Name, Sport_ID)
                            VALUES (%s, %s)
                        """, (values['Sponsor_Name'], values['Sport_ID']))
                        
                        # Insert budget if provided
                        if values.get('Budget'):
                            cursor.execute("""
                                INSERT INTO sponsors_budget (Sponsor_Name, Budget)
                                VALUES (%s, %s)
                            """, (values['Sponsor_Name'], values['Budget']))
                    
                    conn.commit()
                    messagebox.showinfo("Success", "Data inserted successfully!")
                    
                    # Clear form
                    for entry in entries.values():
                        if hasattr(entry, 'delete'):
                            entry.delete(0, tk.END)
                        else:
                            entry.set('')
                    
                except mysql.connector.Error as err:
                    conn.rollback()
                    logging.error(f"Database error: {err}")
                    messagebox.showerror("Error", f"Failed to insert data: {err}\nCheck if all required fields are filled and foreign keys exist.")
                finally:
                    cursor.close()
            
            ttk.Button(form_frame, text="Insert Data", command=insert_data).grid(
                row=len(unnormalized_tables[selected_table]), column=0, columnspan=2, pady=20)
        
        table_combo.bind("<<ComboboxSelected>>", create_form)
        
        form_canvas.pack(side="left", fill="both", expand=True)
        form_scrollbar.pack(side="right", fill="y")

    advanced_search_tab()
    create_visualization_tab()
    create_theme_toggle(root)
    create_backup_button(root)
    if role == "admin":
        create_sql_query_tab()
    create_insert_tab()
    root.mainloop()

def display_results(results, columns):
    result_window = tk.Toplevel()
    result_window.title("Search Results")
    tree = ttk.Treeview(result_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", stretch=True)
    for row in results:
        tree.insert("", "end", values=row)
    tree.pack(expand=True, fill="both")

# Start with login page
login_page()
