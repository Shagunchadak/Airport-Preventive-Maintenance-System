import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import webbrowser
from tkinter import Tk, Menu, Toplevel,PhotoImage,Label, Text, Scrollbar, RIGHT, Y
import time
import customtkinter as ctk
from datetime import datetime, timedelta
# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='new_airport_db',
            user='root',
            password='Shagun@123',
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Database functions
def authenticate_user(username, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            connection.close()
            return user
        except Error as e:
            print(f"Error retrieving user: {e}")
            return None

def add_equipment(name, site_acceptance_date, purchase_order, cmc_start_date, cmc_end_date, equipment_number):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO equipment_info (name, site_acceptance_date, purchase_order, cmc_start_date, cmc_end_date, equipment_number)
                              VALUES (%s, %s, %s, %s, %s, %s)''', 
                              (name, site_acceptance_date, purchase_order, cmc_start_date, cmc_end_date, equipment_number))
            connection.commit()
            print("Equipment added successfully.")
        except Error as e:
            print(f"Error inserting data: {e}")
        finally:
            connection.close()

def add_maintenance(equipment_id, maintenance_date, maintenance_by):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO maintenance_records (equipment_id, maintenance_date, maintenance_by)
                              VALUES (%s, %s, %s)''', 
                              (equipment_id, maintenance_date, maintenance_by))
            connection.commit()
            print("Maintenance record added successfully.")
        except Error as e:
            print(f"Error inserting maintenance data: {e}")
        finally:
            connection.close()

def add_fault(equipment_id, fault_description, reported_by):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO fault_reports (equipment_id, fault_description, reported_by)
                              VALUES (%s, %s, %s)''', 
                              (equipment_id, fault_description, reported_by))
            connection.commit()
            print("Fault report added successfully.")
        except Error as e:
            print(f"Error inserting fault report data: {e}")
        finally:
            connection.close()

def add_vendor(vendor_name, services_provided):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO vendor_details (vendor_name, services_provided)
                              VALUES (%s, %s)''', 
                              (vendor_name, services_provided))
            connection.commit()
            print("Vendor details added successfully.")
        except Error as e:
            print(f"Error inserting vendor details: {e}")
        finally:
            connection.close()

def add_sap(vendor_id, invoice_number, cost, sap_details, bill_file_path, agreement_file_path):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO sap_details (vendor_id, invoice_number, cost, sap_details, bill_file_path, agreement_file_path)
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                              (vendor_id, invoice_number, cost, sap_details, bill_file_path, agreement_file_path))
            connection.commit()
            print("SAP details added successfully.")
        except Error as e:
            print(f"Error inserting SAP details: {e}")
        finally:
            connection.close()

def fetch_data(table_name):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            return columns, rows
        except Error as e:
            print(f"Error retrieving data: {e}")
            return None, None
        finally:
            connection.close()

def fetch_vendor_data():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM vendor_details')
            rows = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            return columns, rows
        except Error as e:
            print(f"Error retrieving vendor data: {e}")
            return None, None
        finally:
            connection.close()

def get_upcoming_maintenance():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            next_week = datetime.now() + timedelta(days=7)
            cursor.execute('''SELECT equipment_info.name, maintenance_records.maintenance_date 
                              FROM equipment_info 
                              JOIN maintenance_records ON equipment_info.id = maintenance_records.equipment_id 
                              WHERE maintenance_records.maintenance_date <= %s''', (next_week,))
            upcoming_maintenance = cursor.fetchall()
            return upcoming_maintenance
        except Error as e:
            print(f"Error retrieving data: {e}")
            return []
        finally:
            connection.close()

# GUI application
def show_notification():
    upcoming = get_upcoming_maintenance()
    if upcoming:
        msg = "Upcoming Maintenance:\n"
        for item in upcoming:
            msg += f"{item[0]} on {item[1]}\n"
        messagebox.showinfo("Notification", msg)
    else:
        messagebox.showinfo("Notification", "No upcoming maintenance.")

def submit_equipment():
    add_equipment(equipment_name_entry.get(), site_acceptance_date_entry.get(), purchase_order_entry.get(),
                  cmc_start_date_entry.get(), cmc_end_date_entry.get(), equipment_number_entry.get())
    messagebox.showinfo("Success", "Equipment added successfully")

def submit_maintenance():
    equipment_id = equipment_id_entry.get()
    maintenance_date = maintenance_date_entry.get()
    maintenance_by = maintenance_by_entry.get()
    
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if equipment_id exists in equipment_info table
            cursor.execute('SELECT * FROM equipment_info WHERE id = %s', (equipment_id,))
            if cursor.fetchone() is None:
                messagebox.showerror("Error", "Equipment ID does not exist.")
                return
            
            # Insert maintenance record
            cursor.execute('''INSERT INTO maintenance_records (equipment_id, maintenance_date, maintenance_by)
                              VALUES (%s, %s, %s)''', 
                              (equipment_id, maintenance_date, maintenance_by))
            connection.commit()
            messagebox.showinfo("Success", "Maintenance record added successfully.")
        except Error as e:
            print(f"Error inserting maintenance data: {e}")
        finally:
            connection.close()

def submit_fault():
    add_fault(fault_equipment_id_entry.get(), fault_description_entry.get("1.0", tk.END), fault_reported_by_entry.get())
    messagebox.showinfo("Success", "Fault report added successfully")

def submit_vendor():
    add_vendor(vendor_name_entry.get(), services_provided_entry.get())
    messagebox.showinfo("Success", "Vendor details added successfully")

def submit_sap():
    vendor_id = vendor_id_entry.get()
    invoice_number = invoice_number_entry.get()
    cost = cost_entry.get()
    sap_details = sap_details_entry.get("1.0", tk.END)
    
    # Open file dialogs to select PDF files
    bill_file_path = filedialog.askopenfilename(
        title="Select Bill File",
        filetypes=[("PDF files", "*.pdf")],
        initialdir="/"
    )
    
    agreement_file_path = filedialog.askopenfilename(
        title="Select Agreement File",
        filetypes=[("PDF files", "*.pdf")],
        initialdir="/"
    )

    # Ensure files are selected
    if not bill_file_path or not agreement_file_path:
        messagebox.showerror("Error", "Both files must be selected.")
        return

    add_sap(vendor_id, invoice_number, cost, sap_details, bill_file_path, agreement_file_path)
    messagebox.showinfo("Success", "SAP details added successfully")

def create_interactive_map():
    map_window = tk.Toplevel()
    map_window.title("Kangra Airport Map")
    map_window.geometry("1200x800")  # Adjust size as needed

    try:
        # Load the map image
        map_image = Image.open("c:\\Users\\HP\\Desktop\\Screenshot_29-7-2024_74456_.jpeg")  # Ensure this path is correct
        map_photo = ImageTk.PhotoImage(map_image)
    except FileNotFoundError:
        messagebox.showerror("Error", "Map file not found.")
        return

    # Create a canvas to display the image
    canvas = tk.Canvas(map_window, width=map_photo.width(), height=map_photo.height())
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=map_photo)

    # Ensure the image reference is maintained
    canvas.image = map_photo

def add_page(page_type):
    add_window = tk.Toplevel()
    add_window.title(f"Add {page_type.capitalize()} Details")

    # Set the Toplevel window to full screen
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    add_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Create a frame to hold the content and center it
    frame = tk.Frame(add_window, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.9)

    if page_type == "equipment":
        tk.Label(frame, text="Name").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Site Acceptance Date").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Purchase Order").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame, text="CMC Start Date").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(frame, text="CMC End Date").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(frame, text="Equipment Number").grid(row=5, column=0, padx=10, pady=10)

        global equipment_name_entry, site_acceptance_date_entry, purchase_order_entry, cmc_start_date_entry, cmc_end_date_entry, equipment_number_entry
        equipment_name_entry = tk.Entry(frame)
        site_acceptance_date_entry = tk.Entry(frame)
        purchase_order_entry = tk.Entry(frame)
        cmc_start_date_entry = tk.Entry(frame)
        cmc_end_date_entry = tk.Entry(frame)
        equipment_number_entry = tk.Entry(frame)

        equipment_name_entry.grid(row=0, column=1, padx=10, pady=10)
        site_acceptance_date_entry.grid(row=1, column=1, padx=10, pady=10)
        purchase_order_entry.grid(row=2, column=1, padx=10, pady=10)
        cmc_start_date_entry.grid(row=3, column=1, padx=10, pady=10)
        cmc_end_date_entry.grid(row=4, column=1, padx=10, pady=10)
        equipment_number_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_equipment).grid(row=6, columnspan=2, pady=20)

    elif page_type == "maintenance":
        tk.Label(frame, text="Equipment ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Maintenance Date").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Maintenance By").grid(row=2, column=0, padx=10, pady=10)

        global equipment_id_entry, maintenance_date_entry, maintenance_by_entry
        equipment_id_entry = tk.Entry(frame)
        maintenance_date_entry = tk.Entry(frame)
        maintenance_by_entry = tk.Entry(frame)

        equipment_id_entry.grid(row=0, column=1, padx=10, pady=10)
        maintenance_date_entry.grid(row=1, column=1, padx=10, pady=10)
        maintenance_by_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_maintenance).grid(row=3, columnspan=2, pady=20)

    elif page_type == "fault":
        tk.Label(frame, text="Equipment ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Fault Description").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Reported By").grid(row=2, column=0, padx=10, pady=10)

        global fault_equipment_id_entry, fault_description_entry, fault_reported_by_entry
        fault_equipment_id_entry = tk.Entry(frame)
        fault_description_entry = tk.Text(frame, height=4, width=50)
        fault_reported_by_entry = tk.Entry(frame)

        fault_equipment_id_entry.grid(row=0, column=1, padx=10, pady=10)
        fault_description_entry.grid(row=1, column=1, padx=10, pady=10)
        fault_reported_by_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_fault).grid(row=3, columnspan=2, pady=20)

    elif page_type == "vendor":
        tk.Label(frame, text="Vendor Name").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Services Provided").grid(row=1, column=0, padx=10, pady=10)

        global vendor_name_entry, services_provided_entry
        vendor_name_entry = tk.Entry(frame)
        services_provided_entry = tk.Entry(frame)

        vendor_name_entry.grid(row=0, column=1, padx=10, pady=10)
        services_provided_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_vendor).grid(row=2, columnspan=2, pady=20)

    elif page_type == "sap":
        tk.Label(frame, text="Vendor ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Invoice Number").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Cost").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame, text="SAP Details").grid(row=3, column=0, padx=10, pady=10)

        global vendor_id_entry, invoice_number_entry, cost_entry, sap_details_entry
        vendor_id_entry = tk.Entry(frame)
        invoice_number_entry = tk.Entry(frame)
        cost_entry = tk.Entry(frame)
        sap_details_entry = tk.Text(frame, height=4, width=50)

        vendor_id_entry.grid(row=0, column=1, padx=10, pady=10)
        invoice_number_entry.grid(row=1, column=1, padx=10, pady=10)
        cost_entry.grid(row=2, column=1, padx=10, pady=10)
        sap_details_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_sap).grid(row=4, columnspan=2, pady=20)


def view_equipment_page():
    view_page("equipment_info")

def view_maintenance_page():
    view_page("maintenance_records")

def view_fault_reports_page():
    view_page("fault_reports")

def view_vendor_details_page():
    view_page("vendor_details")

def view_sap_details_page():
    view_window = tk.Toplevel()
    view_window.title("View SAP Details")

    columns, rows = fetch_data("sap_details")
    if columns:
        # Display column headers
        for col in range(len(columns)):
            tk.Label(view_window, text=columns[col], relief=tk.RAISED, width=15).grid(row=0, column=col)
        
        # Display rows
        for row in range(len(rows)):
            for col in range(len(columns)):
                tk.Label(view_window, text=rows[row][col], width=15).grid(row=row+1, column=col)

            # Add a button to view the document for each SAP record
            view_button = tk.Button(view_window, text="View Document", command=lambda row=row: view_document(rows[row][0]))
            view_button.grid(row=row+1, column=len(columns), padx=5, pady=5)

        # Search and Delete options
        tk.Label(view_window, text="Search").grid(row=len(rows)+1, column=0)
        search_entry = tk.Entry(view_window)
        search_entry.grid(row=len(rows)+1, column=1)
        tk.Button(view_window, text="Search", command=lambda: search_table("sap_details", search_entry.get())).grid(row=len(rows)+1, column=2)
        tk.Button(view_window, text="Delete", command=lambda: delete_record("sap_details")).grid(row=len(rows)+1, column=3)


def view_document(record_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT bill_file_path, agreement_file_path FROM sap_details WHERE id = %s', (record_id,))
            result = cursor.fetchone()
            
            if result:
                bill_file_path, agreement_file_path = result
                # Open the PDF files
                if bill_file_path:
                    webbrowser.open(bill_file_path)
                if agreement_file_path:
                    webbrowser.open(agreement_file_path)
            else:
                messagebox.showerror("Error", "Document not found.")
        except Error as e:
            print(f"Error retrieving document paths: {e}")
        finally:
            connection.close()


def view_page(table_name):
    view_window = tk.Toplevel()
    view_window.title(f"View {table_name.replace('_', ' ').capitalize()}")

    columns, rows = fetch_data(table_name)
    if columns:
        for col in range(len(columns)):
            tk.Label(view_window, text=columns[col], relief=tk.RAISED, width=15).grid(row=0, column=col)
        
        for row in range(len(rows)):
            for col in range(len(columns)):
                tk.Label(view_window, text=rows[row][col], width=15).grid(row=row+1, column=col)

        # Add search and delete options
        tk.Label(view_window, text="Search").grid(row=len(rows)+1, column=0)
        search_entry = tk.Entry(view_window)
        search_entry.grid(row=len(rows)+1, column=1)
        tk.Button(view_window, text="Search", command=lambda: search_table(table_name, search_entry.get())).grid(row=len(rows)+1, column=2)
        tk.Button(view_window, text="Delete", command=lambda: delete_record(table_name)).grid(row=len(rows)+1, column=3)

def search_table(table_name, search_term):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM {table_name} WHERE CONCAT_WS(' ', {', '.join(['`' + col + '`' for col in fetch_data(table_name)[0]])}) LIKE %s"
            cursor.execute(query, ('%' + search_term + '%',))
            rows = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            
            # Create a new window to display the search results
            search_window = tk.Toplevel()
            search_window.title(f"Search Results for {table_name.replace('_', ' ').capitalize()}")
            
            if columns:
                for col in range(len(columns)):
                    tk.Label(search_window, text=columns[col], relief=tk.RAISED, width=15).grid(row=0, column=col)
                
                for row in range(len(rows)):
                    for col in range(len(columns)):
                        tk.Label(search_window, text=rows[row][col], width=15).grid(row=row+1, column=col)
            
        except Error as e:
            print(f"Error searching data: {e}")
        finally:
            connection.close()


def delete_record(table_name):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Prompt user to enter the ID of the record to delete
            record_id = tk.simpledialog.askstring("Delete Record", "Enter the ID of the record to delete:")
            
            if record_id:
                cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
                connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully.")
                
            else:
                messagebox.showerror("Error", "Record ID must be provided.")
                
        except Error as e:
            print(f"Error deleting data: {e}")
        finally:
            connection.close()



def open_help_desk():
    chatbot_window = tk.Toplevel(root)
    chatbot_window.title("Help Desk Chatbot")
    chatbot_window.geometry("600x500")

    def chatbot_response(user_input):
        """Generate a response based on the user's input."""
        responses = {
            # General
            "hello": "Hello! How can I assist you today?",
            "hi": "Hi there! How can I help you today?",
            "help": "You can ask me about flight information, weather, emergency procedures, maintenance, adding details, and more. How can I help?",
            
            # Flight Information
            "flight information": "You can check real-time flight information on our flight info page.",
            "current flights": "View current flight statuses on our flight information page.",
            "flight status": "For flight status, visit our flight tracking page.",
            "departure times": "Check the departure times on our flight schedule page.",
            "arrival times": "Find arrival times on our flight arrivals page.",
            
            # Weather
            "weather": "Current weather details are available on the weather information section.",
            "current weather": "Visit the weather information section for the latest weather updates.",
            "weather forecast": "Check our weather forecast section for upcoming weather conditions.",
            
            # Emergency
            "emergency": "For emergencies, please contact our emergency services or check the emergency procedures section.",
            "emergency contact": "In case of emergencies, contact our emergency services directly at [emergency contact number].",
            
            # Lost and Found
            "lost and found": "Report lost items to our lost and found department at the airport.",
            "baggage claim": "For baggage claim, visit the baggage claim desk at the airport.",
            
            # Check-in and Boarding
            "check-in": "Check-in counters are located in the main terminal. Please arrive early to complete the check-in process.",
            "boarding pass": "Print your boarding pass at the self-service kiosks or at the check-in counter.",
            "check-in time": "Check-in typically opens 3 hours before departure for domestic flights and 4 hours for international flights.",
            "boarding time": "Boarding usually begins 30-60 minutes before the scheduled departure time.",
            
            # Security
            "security procedures": "Follow the security guidelines posted at the airport for a smooth security screening process.",
            
            # Airport Facilities
            "airport facilities": "Our airport offers various facilities including lounges, dining options, and shopping.",
            "lounges": "Airport lounges are available for eligible passengers. Check the lounge section for more details.",
            "food and beverages": "Dining options are available throughout the terminal. Check our food and beverages page.",
            "shopping": "Explore shops and boutiques at the airport for your shopping needs.",
            "wifi": "Free Wi-Fi is available throughout the airport. Connect to the 'Airport_WiFi' network.",
            
            # Parking and Transport
            "parking": "Information about parking facilities and rates can be found on our parking page.",
            "car rentals": "Car rental services are available at the airport. Visit the car rental desk for assistance.",
            "public transport": "Public transport options are available from the airport, including buses and taxis.",
            "taxi services": "Taxi services are available at the designated taxi stand outside the terminal.",
            "bus services": "Airport buses operate to various destinations. Check the bus services page for schedules.",
            
            # Hotels and Bookings
            "hotel bookings": "Find information about nearby hotels and book accommodations through our hotel services page.",
            
            # Flight Issues
            "flight delays": "For information on flight delays, visit the flight status section or check with your airline.",
            "cancellations": "For flight cancellations, contact your airline directly or check the airline's website.",
            
            # Special Assistance
            "special assistance": "If you need special assistance, contact our customer service team in advance.",
            "lost luggage": "Report lost luggage to the airline's baggage claim office or contact our lost luggage department.",
            
            # Airport Map and Navigation
            "airport map": "An airport map is available on our website to help you navigate the terminal.",
            
            # Maintenance and Details
            "add details": "To add details for equipment, maintenance, faults, or vendors, please use the 'Add Details' section in the application.",
            "view details": "You can view added details for equipment, maintenance, faults, and vendors in the 'View Details' section.",
            "maintenance": "For information on maintenance schedules and procedures, visit the maintenance section.",
            
            # Kangra Airport Specific
            "kangra airport": "Kangra Airport serves the Kangra region. For specific services and facilities at Kangra Airport, please visit our airport page.",
            "kangra airport facilities": "Check out the Kangra Airport facilities section for information on services available at this airport.",
            "kangra airport contact": "For contact details of Kangra Airport, please visit the contact page or call [Kangra Airport contact number]."
        }
        
        user_input = user_input.lower()
        return responses.get(user_input, "Sorry, I don't understand that query. Please ask something else.")

    def send_message():
        """Handle the sending of messages."""
        user_message = user_entry.get()
        if user_message.strip():
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, "You: " + user_message + "\n")

            # Get the chatbot's response
            bot_message = chatbot_response(user_message)
            chat_history.insert(tk.END, "Bot: " + bot_message + "\n")

            # Clear the entry field
            user_entry.delete(0, tk.END)

            # Auto-scroll to the bottom of the chat history
            chat_history.yview(tk.END)
            chat_history.config(state=tk.DISABLED)

    # Create the chat history area
    chat_history = tk.Text(chatbot_window, wrap=tk.WORD, state=tk.DISABLED)
    chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create the user entry area
    user_entry = tk.Entry(chatbot_window, width=50)
    user_entry.pack(pady=10, padx=10, side=tk.LEFT, fill=tk.X, expand=True)

    # Create the send button
    send_button = tk.Button(chatbot_window, text="Send", command=send_message)
    send_button.pack(pady=10, padx=10, side=tk.RIGHT)

    # Bind the Enter key to send the message
    chatbot_window.bind('<Return>', lambda event: send_message())


BUTTON_COLOR = "#ADD8E6"  # Light blue color for buttons
TEXT_WIDGET_BG_COLOR = "#E0F7FA"  # Light blue color for text widgets
TEXT_COLOR = "black"
LOGOUT_COLOR = "white"
NOTIFICATION_COLOR = "white"


# Global variable for animation
animation_position = 0

def logout():
    root.destroy()
    # Add logic to redirect to the login page

def show_about_us():
    about_text = (
        "Airports Authority of India\n\n"
        "Kangra Airport, Gaggal, Himachal Pradesh\n\n"
        "Contact: contact@kangraairport.com\n"
        "Address: Gaggal, District Kangra, Himachal Pradesh, India\n\n"
        "For more information, visit our website:"
    )
    result = messagebox.askyesno("About Us", about_text + "\n\nWould you like to visit the website?")
    
    if result:
        webbrowser.open("https://www.aai.aero/en/airports/kangra")
        
def show_help_center():
    help_window = Toplevel(root)
    help_window.title("Help Center")

    faq_info = (
        "FAQs:\n"
        "1. How do I add equipment?\n"
        "   - Go to the 'Add Details' menu and select 'Equipment'. Fill in the details and click 'Submit'.\n"
        "2. How do I view maintenance records?\n"
        "   - Go to the 'View Details' menu and select 'Maintenance'.\n"
        "3. How do I contact support?\n"
        "   - Contact us at: support@airport-authority.com\n"
        "4. How do I upload files?\n"
        "   - Use the 'Add Details' menu to add SAP details and upload files there.\n"
        "5. How do I log in?\n"
        "   - Enter your username and password on the login page, then click 'Submit'.\n"
        "6. How do I view fault reports?\n"
        "   - Go to the 'View Details' menu and select 'Fault Reports'.\n"
        "7. How do I search for specific details?\n"
        "   - Use the search bar available in the 'View Details' sections to find specific records.\n"
        "8. How do I delete an entry?\n"
        "   - Use the delete button next to the entry in the 'View Details' sections.\n"
        "9. How do I get notifications for upcoming maintenance?\n"
        "   - Notifications for upcoming maintenance will appear in the notification bar at the top right corner.\n"
        "10. How do I add vendor details?\n"
        "   - Go to the 'Add Details' menu and select 'Vendor'. Fill in the details and click 'Submit'.\n"
        "11. How do I add SAT (Site Acceptance Test) details?\n"
        "   - Go to the 'Add Details' menu and select 'SAT'. Fill in the details and click 'Submit'.\n"
        "12. How do I view SAP details?\n"
        "   - Go to the 'View Details' menu and select 'SAP Details'.\n"
        "13. How do I view uploaded files?\n"
        "   - In the 'SAP Details' section, click the 'View File' button next to the corresponding entry.\n"
        "14. How do I log out?\n"
        "   - Click the 'Logout' button at the bottom right corner of the main page.\n"
        "15. How do I maximize or minimize the application window?\n"
        "   - Use the buttons at the top right corner of the window to maximize, minimize, or close the application.\n"
        "16. How do I add details for maintenance?\n"
        "   - Go to the 'Add Details' menu and select 'Maintenance'. Fill in the details and click 'Submit'.\n"
        "17. How do I contact the Airport Authority of India?\n"
        "   - Contact us at: contact@airport-authority.com or visit our 'About Us' section.\n"
    )

    tk.Label(help_window, text=faq_info, padx=10, pady=10, justify='left').pack()

        
def show_maintenance_info():
    # Create a new full-screen window
    maintenance_window = Toplevel(root)
    maintenance_window.title("Maintenance Information")

    # Set the window to full-screen
    maintenance_window.attributes("-fullscreen", True)

    # Create a frame to contain the content
    content_frame = tk.Frame(maintenance_window, bg="#f0f0f0")
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Create a text widget for displaying the information
    text_widget = Text(content_frame, wrap='word', bg="#f5f5f5", fg="#333333", font=("Helvetica", 12, "normal"))
    text_widget.pack(side='left', fill='both', expand=True)

    # Create a scrollbar for the text widget
    scrollbar = Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Insert the maintenance information into the text widget
    maintenance_info = """
    PURPOSE OF AIRPORT MAINTENANCE
    An airport, being an important part of the Aeronautical Infrastructure, has to meet high Safety Standards. The required level of safety can only be achieved by proper Maintenance of all the elements composing an airport.
    Maintenance includes measures to keep or restore the operational function as well as measures to check and to evaluate the present function of an element.
    The basic components of maintenance are:
    — inspection;
    — servicing and overhaul; and
    — repair.

    Assist Airports with the following:
    Compile Standard Operating Procedures, predictive preventative maintenance plans and schedules for equipment, infrastructure and facilities.
    Assist with Service Level Agreements for Infrastructure and Equipment.

    Maintenance of Visual Aids
    Spare parts
    Light maintenance schedule General
    Basic maintenance programme for approach, runway and taxi way light systems

    Additional maintenance programme
    Special types of lights
    Maintenance programme for other Airport lights

    Docking guidance systems
    Light maintenance procedures
    General hints for the maintenance of lights
    Cleaning procedures for lights
    Light measurement
    Lamp replacement
    Removal of water

    Signs
    Markings

    Maintenance of Airport Electrical Systems
    Schedule of maintenance
    Power cables and distributors in field
    Transformers and regulators (including standby units)
    Transformer stations for electric power supply
    Relay and switch cabinets (including switch cabinets in sub-stations)
    Control cables, monitoring units, control desk
    Secondary power supplies (generators)
    Fixed 400 Hz ground power supplies
    Apron floodlighting

    Maintenance of Pavements
    Surface repair
    Portland cement concrete pavements
    Bituminous pavements
    Repair of joints and cracks
    Joints in concrete pavements
    Concrete joint maintenance
    Joints in bituminous pavements
    Cracks in concrete pavements
    Cracks in bituminous pavements
    Repair of pavement edge damage
    Edge repair
    Corner repair
    Repair of other pavement surface deficiencies

    Sweeping
    Purpose of sweeping
    Surface monitoring

    Cleaning of surfaces
    Cleaning of contaminants
    Purpose of cleaning pavements
    Removal of rubber deposits
    Fuel and oil removal

    Removal of snow and ice
    Snow plan and Snow Committee
    Responsibilities
    Procedures for interrupting air traffic
    Procedures for snow removal
    Surface de-icing
    Surface anti-icing
    Personnel training

    Drainage
    Cleaning of slot drains
    Drain pipes or culverts between surfaces and collector basins
    Oil and fuel separators
    Water hydrants

    Maintenance of Unpaved Areas
    Maintenance of green areas within strips
    Maintenance of grass on unpaved runways and taxiways
    Maintenance of green areas outside strips

    Equipment for maintenance of grass
    Treatment of cut grass
    Removal of Disabled Aircraft
    Removal plan
    Personnel training
    Storage of equipment
    Maintenance of removal equipment

    Maintenance of Equipment and Vehicles
    General
    Organization of vehicle maintenance
    Schedule of vehicle maintenance
    Workshops

    Buildings
    Lighting and electric equipment
    Communication facilities
    Air conditioning system
    Heating facilities
    Automatic doors
    Baggage conveyor belts (fixed installations)
    Baggage claim units
    Passenger boarding bridges
    People lifts (elevators)
    People movers (escalators, etc.)
    Fixed fire protection installations
    Safety Department
    """
    
    # Insert the maintenance info into the text widget
    text_widget.insert('1.0', maintenance_info)

    # Add a close button
    close_button = tk.Button(maintenance_window, text="Close", command=maintenance_window.destroy, bg="#FF5722", fg="#ffffff", font=("Helvetica", 12, "bold"))
    close_button.pack(side=tk.BOTTOM, pady=10)

def show_atsep_facilities():
    atsep_window = tk.Toplevel(root)
    atsep_window.title("ATSEP Facilities at Kangra Airport")
    
    # Remove the full-screen attribute for window decorations
    atsep_window.attributes("-fullscreen", False)
    atsep_window.geometry("1000x700")  # Set a default window size

    # Create a frame for the canvas and scrollbar(s)
    frame = tk.Frame(atsep_window)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Add a canvas widget
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Add a scrollbar widget
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # Enable scrolling with arrow keys
    def on_key_press(event):
        if event.keysym == 'Down':
            canvas.yview_scroll(1, 'units')
        elif event.keysym == 'Up':
            canvas.yview_scroll(-1, 'units')
    
    canvas.bind_all('<KeyPress>', on_key_press)
    
    # Create a frame to hold the content
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    # Add detailed descriptions for each facility
    facilities = {
        "VHF": "VHF (Very High Frequency) systems are used for line-of-sight communication between aircraft and air traffic control. "
               "At Kangra Airport, the VHF facility ensures clear communication within a specific range, enhancing safety and coordination. "
               "The system operates in the frequency range of 30 to 300 MHz, providing reliable communication in both terminal and en-route airspaces. "
               "VHF communication is essential for routine operations, emergency procedures, and providing pilots with vital information. "
               "This facility is maintained regularly to ensure optimal performance and minimal disruption to services. "
               "Technicians at Kangra Airport monitor the VHF system continuously to detect and rectify any faults promptly. "
               "The airport's VHF system also supports various other navigational aids, ensuring comprehensive coverage for aircraft. "
               "Training and certification of personnel handling VHF equipment are mandatory to maintain high standards of operation. "
               "Kangra Airport's VHF system plays a critical role in maintaining seamless and efficient communication between air traffic control and aircraft. "
               "Advancements in VHF technology continue to enhance the reliability and clarity of communication at Kangra Airport.",
        "NDB": "NDB (Non-Directional Beacon) is a radio transmitter at a known location used as an aviation or marine navigational aid. "
               "At Kangra Airport, the NDB aids in providing directional information to pilots, particularly during poor visibility conditions. "
               "The NDB transmits signals in all directions, allowing aircraft to determine their position relative to the beacon. "
               "NDBs operate in the low to medium frequency range (190 to 535 kHz), making them useful for both short and long-range navigation. "
               "Kangra Airport's NDB is strategically positioned to assist with the approach and landing phases of flight. "
               "The system is regularly tested and maintained to ensure it operates without interruption. "
               "Pilots rely on the NDB for en-route navigation and to perform instrument approaches. "
               "NDB signals can be affected by various factors like weather and terrain, but at Kangra Airport, the facility is optimized to minimize such issues. "
               "Training for the use and interpretation of NDB signals is crucial for pilots and air traffic controllers. "
               "The NDB at Kangra Airport enhances the safety and efficiency of air navigation by providing a reliable navigational reference.",
        "DVOR": "DVOR (Doppler VHF Omnidirectional Range) is a type of radio navigation system for aircraft. "
                "At Kangra Airport, the DVOR provides precise bearing information to pilots, enhancing navigational accuracy. "
                "The DVOR system transmits VHF radio signals that aircraft receivers can interpret to determine their position relative to the station. "
                "It operates in the VHF band between 108.00 to 117.95 MHz, making it reliable for short to medium-range navigation. "
                "The Doppler effect in DVOR reduces signal distortion, providing more accurate directional information compared to conventional VOR systems. "
                "Maintenance of the DVOR at Kangra Airport includes regular calibration and testing to ensure high accuracy and reliability. "
                "Pilots use DVOR for en-route navigation and during approaches to align with the runway. "
                "The DVOR facility at Kangra Airport is crucial for ensuring safe and efficient flight operations, especially in complex airspace. "
                "Personnel operating the DVOR are trained to handle equipment and interpret signals accurately, ensuring seamless operations. "
                "Technological advancements in DVOR systems continue to improve navigational capabilities at Kangra Airport, contributing to overall aviation safety.",
        "HPDME": "HPDME (High-Precision Distance Measuring Equipment) provides accurate distance information between the aircraft and the ground station. "
                 "At Kangra Airport, HPDME enhances the accuracy of position determination, critical for approach and landing procedures. "
                 "HPDME operates in the UHF spectrum, typically between 960 and 1215 MHz, providing high precision over long distances. "
                 "The system works by measuring the time delay between transmitted and received signals, converting it into distance. "
                 "Regular maintenance and calibration of HPDME at Kangra Airport ensure it delivers precise distance measurements. "
                 "Pilots use HPDME data to enhance situational awareness and for precise navigation during various phases of flight. "
                 "HPDME integration with other navigational aids like DVOR further improves navigational accuracy and safety. "
                 "The facility at Kangra Airport is continuously monitored to ensure its optimal performance. "
                 "Training for using and maintaining HPDME is essential for airport technical staff and pilots. "
                 "HPDME at Kangra Airport is a critical component of the navigational infrastructure, supporting safe and efficient flight operations.",
        "W/T": "W/T (Wireless Telegraphy) refers to the transmission of telegraph signals via radio waves. "
               "At Kangra Airport, W/T is used for various communication needs, including coordination between ground personnel and aircraft. "
               "W/T systems operate in various frequency bands, depending on the communication requirements and range. "
               "The use of W/T at Kangra Airport includes transmitting weather information, operational instructions, and emergency messages. "
               "Maintenance of W/T equipment ensures reliable communication channels are available at all times. "
               "W/T plays a crucial role in supporting other navigational aids by providing supplementary communication capabilities. "
               "Personnel at Kangra Airport are trained to use and maintain W/T systems to ensure they meet operational standards. "
               "The integration of W/T with modern communication systems enhances overall airport communication infrastructure. "
               "W/T systems at Kangra Airport are regularly updated to incorporate the latest technology and improve efficiency. "
               "W/T communication is essential for ensuring the smooth operation of airport services and enhancing safety."
    }

    # Create a Text widget for better handling of long text content
    text_widget = tk.Text(content_frame, wrap="word", font=("Segoe UI", 12), bg="#f0f8ff", fg="#333333", padx=10, pady=10)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Insert the facility details into the Text widget
    for facility, description in facilities.items():
        text_widget.insert(tk.END, f"{facility}\n\n{description}\n\n")
    
    # Add a scrollbar to the Text widget
    text_scrollbar = tk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_widget.yview)
    text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=text_scrollbar.set)

    # Add a close button
    close_button = tk.Button(content_frame, text="Close", command=atsep_window.destroy, font=("Segoe UI", 12, "bold"))
    close_button.pack(side=tk.BOTTOM, pady=10)
    
    # Bind the escape key to exit fullscreen mode
    def exit_fullscreen(event):
        atsep_window.attributes("-fullscreen", False)
        atsep_window.geometry("1000x700")  # Restore to default size

    atsep_window.bind("<Escape>", exit_fullscreen)



def resize_image(image_path, width, height):
    try:
        image = Image.open(image_path)
        resized_image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None

def update_background_image(background_label, image_path):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    resized_image = resize_image(image_path, window_width, window_height)
    if resized_image:
        background_label.config(image=resized_image)
        background_label.image = resized_image 

def open_feedback():
    global feedback_window, feedback_entry
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Submit Feedback")
    
    tk.Label(feedback_window, text="Enter your feedback:").pack(pady=10)
    feedback_entry = tk.Entry(feedback_window, width=50)
    feedback_entry.pack(pady=10)
    
    submit_button = tk.Button(feedback_window, text="Submit", command=submit_feedback, bg="green", fg="white")
    submit_button.pack(pady=10)
    
    cancel_button = tk.Button(feedback_window, text="Cancel", command=feedback_window.destroy, bg="red", fg="white")
    cancel_button.pack(pady=10)

def submit_feedback():
    feedback = feedback_entry.get()
    if feedback:
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shagun@123",
                database="new_airport_db",
                auth_plugin='mysql_native_password'
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO feedback (feedback) VALUES (%s)", (feedback,))
            connection.commit()
            messagebox.showinfo("Feedback", "Thank you for your feedback!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    else:
        messagebox.showwarning("Feedback", "Please enter feedback before submitting.")
    feedback_window.destroy()


def animate_title():
    global animation_position
    # Move title leftwards
    title_label.place(x=animation_position, y=10)  # Adjust y-position as needed
    animation_position -= 2
    if animation_position < -title_label.winfo_width():
        animation_position = root.winfo_width()
    root.after(50, animate_title)  # Call this function every 50 milliseconds

def create_button(parent, text, command=None, color=BUTTON_COLOR):
    return tk.Button(parent, text=text, bg=color, fg=TEXT_COLOR, font=("Arial", 12, "bold"), command=command)


def main():
    global root, title_label, animation_position
    root = tk.Tk()
    root.title("Airport Maintenance System")

    background_image_path = "c:\\Users\\HP\\Desktop\\Airplane at Luis Muoz Marn International Airport.jpg"

    # Set initial window size
    root.geometry("800x600")  # Adjust as needed

    # Create background label
    background_label = tk.Label(root)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Update background image
    update_background_image(background_label, background_image_path)

    # Resize background image when window size changes
    root.bind("<Configure>", lambda event: update_background_image(background_label, background_image_path))

    # Add logo
    logo_image_path = "c:\\Users\\HP\\Desktop\\Airports_Authority_of_India_logo.svg.png"
    logo_image = Image.open(logo_image_path)
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Resize the image to 100x100 pixels
    logo_image_tk = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(root, image=logo_image_tk, bg='white')
    logo_label.place(x=2, y=2)


    
    # Create animated title
    title_label = tk.Label(root, text="AIRPORTS AUTHORITY OF INDIA", font=("Arial", 20, "bold"), bg='white', fg='blue')
    title_label.place(relx=0.5, y=10, anchor='n')

     # Welcome Message
    welcome_message = tk.Label(root, text="Welcome to Kangra Airport Maintenance System", font=("Arial", 18, "bold"), bg='white', fg='blue')
    welcome_message.place(relx=0.5, rely=0.1, anchor='n')

    # Info Text
    info_text = (
    "Kangra Airport, also known as Gaggal Airport, is one of the busiest airports in the region, "
    "serving thousands of passengers each year. Located in the picturesque Kangra Valley and surrounded by the "
    "scenic Himalayas, this airport features a single runway and provides crucial connectivity for both domestic and "
    "international travelers. Known for its high standards of safety and service, Kangra Airport plays a key role in "
    "supporting tourism and business in Himachal Pradesh. Its modern facilities and efficient operations make it a "
    "vital hub in the region's transportation network."
)

    info_label = tk.Label(
    root,
    text=info_text,
    font=("Segoe UI", 12),  # Modern font
    bg='#f0f8ff',  # Light background color for better contrast
    fg='#333333',  # Dark grey text color for better readability
    wraplength=700,  # Adjust this value based on the window width
    justify='left',
    padx=10,  # Add horizontal padding
    pady=10,  # Add vertical padding
    relief='solid',  # Add a border around the label
    borderwidth=1  # Border width
)
    info_label.place(relx=0.5, rely=0.2, anchor='n', relwidth=0.8)

    # Create the menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Add "Add Details" and "View Details" menu items
    add_menu = tk.Menu(menu_bar, tearoff=0)
    view_menu = tk.Menu(menu_bar, tearoff=0)

    about_menu = tk.Menu(menu_bar, tearoff=0)
    about_menu.add_command(label="About Us", command=show_about_us)
    menu_bar.add_cascade(label="About Us", menu=about_menu)

    maintenance_menu = tk.Menu(menu_bar, tearoff=0)
    maintenance_menu.add_command(label="View Maintenance Info", command=show_maintenance_info)
    menu_bar.add_cascade(label="Maintenance", menu=maintenance_menu)

    # Create the "Help Desk" menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Help Desk", command=open_help_desk)


    menu_bar.add_cascade(label="Add Details", menu=add_menu)
    menu_bar.add_cascade(label="View Details", menu=view_menu)

    add_menu.add_command(label="Add Equipment", command=lambda: add_page("equipment"))
    add_menu.add_command(label="Add Maintenance", command=lambda: add_page("maintenance"))
    add_menu.add_command(label="Add Fault", command=lambda: add_page("fault"))
    add_menu.add_command(label="Add Vendor", command=lambda: add_page("vendor"))
    add_menu.add_command(label="Add SAP Details", command=lambda: add_page("sap"))

    view_menu.add_command(label="View Equipment Details", command=view_equipment_page)
    view_menu.add_command(label="View Maintenance Details", command=view_maintenance_page)
    view_menu.add_command(label="View Fault Reports", command=view_fault_reports_page)
    view_menu.add_command(label="View Vendor Details", command=view_vendor_details_page)
    view_menu.add_command(label="View SAP Details", command=view_sap_details_page)
    

    footer_text = "Contact Us: info@kangraairport.in | +91 123 456 7890"
    footer_label = tk.Label(root, text=footer_text, font=("Arial", 10), bg='white', fg='black')
    footer_label.place(relx=0.5, rely=0.95, anchor='s')
    
    atsep_button = tk.Button(
        root,
        text="ATSEP Facilities at Kangra Airport",
        command=show_atsep_facilities,
        font=("Arial", 10, "bold"),  # Smaller font size
        bg="#0044cc",  # Background color
        fg="white",  # Text color
        relief="raised",  # Raised button effect
        padx=8,  # Horizontal padding
        pady=4,  # Vertical padding
        width=25,  # Set a specific width
        height=1  # Set a specific height
    )
    atsep_button.place(x=10, y=120)  # Position the button under the logo

    footer_text = "Contact Us: info@kangraairport.in | +91 123 456 7890"
    footer_label = tk.Label(root, text=footer_text, font=("Arial", 10), bg='white', fg='black')
    footer_label.place(relx=0.5, rely=0.95, anchor='s')


    logout_button = create_button(root, "Logout", logout, LOGOUT_COLOR)
    logout_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=40)

    notification_button = create_button(root, "Show Notifications", show_notification, NOTIFICATION_COLOR)
    notification_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
    
    feedback_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Feedback", menu=feedback_menu)
    feedback_menu.add_command(label="Submit Feedback", command=open_feedback)
    
    features_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Features", menu=features_menu)
    features_menu.add_command(label="Show Airport Map", command=create_interactive_map)


    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
