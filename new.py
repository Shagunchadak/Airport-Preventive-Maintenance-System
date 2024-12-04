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
from tkinter import messagebox, simpledialog
import subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import matplotlib.pyplot as plt
from tkinter import ttk
import pymysql
from datetime import datetime
from tkcalendar import Calendar
from plyer import notification
import os
import webbrowser
from datetime import datetime
import requests
from tkinter import messagebox

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='airporthii',
            user='root',
            password='Shagun@123',
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

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

def add_equipment(name, manufacturer, model_number, purchase_date, installation_date, location, warranty_period, last_service_date, service_interval, current_status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO equipment_info (name, manufacturer, model_number, purchase_date, installation_date, location, warranty_period, last_service_date, service_interval, current_status)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                              (name, manufacturer, model_number, purchase_date, installation_date, location, warranty_period, last_service_date, service_interval, current_status))
            connection.commit()
            print("Equipment added successfully.")
        except Error as e:
            print(f"Error inserting data: {e}")
        finally:
            connection.close()

def add_maintenance(equipment_id, maintenance_date, type_of_maintenance, details, technician_name, cost, next_scheduled_maintenance):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO maintenance_records (equipment_id, maintenance_date, type_of_maintenance, details, technician_name, cost, next_scheduled_maintenance)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                              (equipment_id, maintenance_date, type_of_maintenance, details, technician_name, cost, next_scheduled_maintenance))
            connection.commit()
            print("Maintenance record added successfully.")
        except Error as e:
            print(f"Error inserting maintenance data: {e}")
        finally:
            connection.close()

def add_fault(equipment_id, fault_date, fault_description, severity, status, resolution_details, resolved_by):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO fault_reports (equipment_id, fault_date, fault_description, severity, status, resolution_details, resolved_by)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                              (equipment_id, fault_date, fault_description, severity, status, resolution_details, resolved_by))
            connection.commit()
            print("Fault report added successfully.")
        except Error as e:
            print(f"Error inserting fault report data: {e}")
        finally:
            connection.close()

def add_vendor_details():
    def submit_vendor_details():
        try:
            vendor_name = vendor_name_entry.get()
            contact_person = contact_person_entry.get()
            contact_information = contact_information_entry.get()
            services_provided = services_provided_entry.get()
            contract_start_date = contract_start_date_entry.get()
            contract_end_date = contract_end_date_entry.get()
            terms_and_conditions = terms_and_conditions_entry.get()
            equipment_id = equipment_id_entry.get()  # New field for equipment ID

            # Validate input
            if not vendor_name or not equipment_id:
                messagebox.showerror("Input Error", "Vendor Name and Equipment ID are required!")
                return

            # Insert vendor details into the database
            conn = mysql.connector.connect(user='root', password='Shagun@123', database='airporthii')
            cursor = conn.cursor()
            query = """
            INSERT INTO vendor_details 
            (vendor_name, contact_person, contact_information, services_provided, 
             contract_start_date, contract_end_date, terms_and_conditions, equipment_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (vendor_name, contact_person, contact_information, services_provided,
                                   contract_start_date, contract_end_date, terms_and_conditions, equipment_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Vendor details added successfully!")
            add_vendor_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    add_vendor_window = tk.Toplevel()
    add_vendor_window.title("Add Vendor Details")

    # Create and place labels and entry fields for vendor details
    tk.Label(add_vendor_window, text="Vendor Name").grid(row=0, column=0)
    vendor_name_entry = tk.Entry(add_vendor_window)
    vendor_name_entry.grid(row=0, column=1)

    tk.Label(add_vendor_window, text="Contact Person").grid(row=1, column=0)
    contact_person_entry = tk.Entry(add_vendor_window)
    contact_person_entry.grid(row=1, column=1)

    tk.Label(add_vendor_window, text="Contact Information").grid(row=2, column=0)
    contact_information_entry = tk.Entry(add_vendor_window)
    contact_information_entry.grid(row=2, column=1)

    tk.Label(add_vendor_window, text="Services Provided").grid(row=3, column=0)
    services_provided_entry = tk.Entry(add_vendor_window)
    services_provided_entry.grid(row=3, column=1)

    tk.Label(add_vendor_window, text="Contract Start Date").grid(row=4, column=0)
    contract_start_date_entry = tk.Entry(add_vendor_window)
    contract_start_date_entry.grid(row=4, column=1)

    tk.Label(add_vendor_window, text="Contract End Date").grid(row=5, column=0)
    contract_end_date_entry = tk.Entry(add_vendor_window)
    contract_end_date_entry.grid(row=5, column=1)

    tk.Label(add_vendor_window, text="Terms and Conditions").grid(row=6, column=0)
    terms_and_conditions_entry = tk.Entry(add_vendor_window)
    terms_and_conditions_entry.grid(row=6, column=1)

    tk.Label(add_vendor_window, text="Equipment ID").grid(row=7, column=0)  # New field
    equipment_id_entry = tk.Entry(add_vendor_window)
    equipment_id_entry.grid(row=7, column=1)

    tk.Button(add_vendor_window, text="Submit", command=submit_vendor_details).grid(row=8, columnspan=2)

def add_sap(equipment_id, sat_date, test_details, results, passed_failed, tested_by, comments, bill_file_path, agreement_file_path):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO sat_details (equipment_id, sat_date, test_details, results, passed_failed, tested_by, comments, bill_file_path, agreement_file_path)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                              (equipment_id, sat_date, test_details, results, passed_failed, tested_by, comments, bill_file_path, agreement_file_path))
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

def get_upcoming_and_overdue_maintenance():
    """Retrieve equipment that is overdue or needs maintenance within the next 15 days."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            current_date = datetime.now()
            next_maintenance_date = current_date + timedelta(days=15)

            # Query for overdue maintenance
            cursor.execute('''SELECT equipment_info.name, maintenance_records.next_scheduled_maintenance 
                              FROM equipment_info 
                              JOIN maintenance_records ON equipment_info.id = maintenance_records.equipment_id 
                              WHERE maintenance_records.next_scheduled_maintenance < %s''', (current_date,))
            overdue_maintenance = cursor.fetchall()

            # Query for upcoming maintenance
            cursor.execute('''SELECT equipment_info.name, maintenance_records.next_scheduled_maintenance 
                              FROM equipment_info 
                              JOIN maintenance_records ON equipment_info.id = maintenance_records.equipment_id 
                              WHERE maintenance_records.next_scheduled_maintenance BETWEEN %s AND %s''',
                           (current_date, next_maintenance_date))
            upcoming_maintenance = cursor.fetchall()

            return overdue_maintenance, upcoming_maintenance

        except Error as e:
            print(f"Error retrieving data: {e}")
            return [], []  # Return empty lists if there's an error
        finally:
            connection.close()

def show_notification():
    """Show a notification with overdue and upcoming maintenance information."""
    overdue, upcoming = get_upcoming_and_overdue_maintenance()
    
    if overdue:
        msg = "Overdue Equipment Maintenance:\n"
        for item in overdue:
            msg += f"Equipment: {item[0]}, Next Scheduled Maintenance: {item[1].strftime('%Y-%m-%d')}\n"
    else:
        msg = "No overdue equipment maintenance.\n"

    msg += "\nUpcoming Maintenance:\n"
    if upcoming:
        for item in upcoming:
            msg += f"Equipment: {item[0]}, Next Scheduled Maintenance: {item[1].strftime('%Y-%m-%d')}\n"
    else:
        msg += "No upcoming maintenance."

    messagebox.showinfo("Maintenance Notifications", msg)
def submit_equipment():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO equipment_info (name, manufacturer, model_number, purchase_date, installation_date, location, warranty_period, last_service_date, service_interval, current_status)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                              (equipment_name_entry.get(), manufacturer_entry.get(), model_number_entry.get(), 
                               purchase_date_entry.get(), installation_date_entry.get(), location_entry.get(),
                               warranty_period_entry.get(), last_service_date_entry.get(), 
                               service_interval_entry.get(), current_status_entry.get()))
            connection.commit()
            messagebox.showinfo("Success", "Equipment added successfully")
        except Error as e:
            print(f"Error inserting equipment data: {e}")
        finally:
            connection.close()

def submit_maintenance():
    equipment_id = equipment_id_entry.get()
    maintenance_date = maintenance_date_entry.get()
    type_of_maintenance = type_of_maintenance_entry.get()
    details = details_entry.get("1.0", tk.END).strip()
    technician_name = technician_name_entry.get()
    cost = cost_entry.get()
    next_scheduled_maintenance = next_scheduled_maintenance_entry.get()

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM equipment_info WHERE id = %s', (equipment_id,))
            if cursor.fetchone() is None:
                messagebox.showerror("Error", "Equipment ID does not exist.")
                return

            cursor.execute('''INSERT INTO maintenance_records (equipment_id, maintenance_date, type_of_maintenance, details, technician_name, cost, next_scheduled_maintenance)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                              (equipment_id, maintenance_date, type_of_maintenance, details, technician_name, cost, next_scheduled_maintenance))
            connection.commit()
            messagebox.showinfo("Success", "Maintenance record added successfully.")
        except Error as e:
            print(f"Error inserting maintenance data: {e}")
        finally:
            connection.close()

def submit_fault():
    equipment_id = fault_equipment_id_entry.get()
    fault_date = fault_date_entry.get()
    fault_description = fault_description_entry.get("1.0", tk.END).strip()
    severity = severity_entry.get()
    status = status_entry.get()
    resolution_details = resolution_details_entry.get("1.0", tk.END).strip()
    resolved_by = resolved_by_entry.get()

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO fault_reports (equipment_id, fault_date, fault_description, severity, status, resolution_details, resolved_by)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                              (equipment_id, fault_date, fault_description, severity, status, resolution_details, resolved_by))
            connection.commit()
            messagebox.showinfo("Success", "Fault report added successfully")
        except Error as e:
            print(f"Error inserting fault data: {e}")
        finally:
            connection.close()

def submit_vendor():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO vendor_details (vendor_name, contact_person, contact_information, services_provided, contract_start_date, contract_end_date, terms_and_conditions)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                              (vendor_name_entry.get(), contact_person_entry.get(), contact_information_entry.get("1.0", tk.END).strip(),
                               services_provided_entry.get("1.0", tk.END).strip(), contract_start_date_entry.get(),
                               contract_end_date_entry.get(), terms_and_conditions_entry.get("1.0", tk.END).strip()))
            connection.commit()
            messagebox.showinfo("Success", "Vendor details added successfully")
        except Error as e:
            print(f"Error inserting vendor data: {e}")
        finally:
            connection.close()

def submit_sap():
    equipment_id = sap_equipment_id_entry.get()
    sat_date = sat_date_entry.get()
    test_details = test_details_entry.get("1.0", tk.END).strip()
    results = results_entry.get("1.0", tk.END).strip()
    passed_failed = passed_failed_entry.get()
    tested_by = tested_by_entry.get()
    comments = comments_entry.get("1.0", tk.END).strip()

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

    if not bill_file_path or not agreement_file_path:
        messagebox.showerror("Error", "Both files must be selected.")
        return

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO sat_details (equipment_id, sat_date, test_details, results, passed_failed, tested_by, comments, bill_file_path, agreement_file_path)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                              (equipment_id, sat_date, test_details, results, passed_failed, tested_by, comments, bill_file_path, agreement_file_path))
            connection.commit()
            messagebox.showinfo("Success", "SAP details added successfully")
        except Error as e:
            print(f"Error inserting SAP data: {e}")
        finally:
            connection.close()

def create_interactive_map():
    map_window = tk.Toplevel()
    map_window.title("Kangra Airport Map")
    map_window.geometry("1200x800")  # Adjust size as needed

    try:
        # Load the map image
        map_image = Image.open("c:\\Users\\HP\\Pictures\\Screenshots\\Screenshot 2024-10-19 023916.png")  # Ensure this path is correct
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




def show_health_safety_guidelines():
    # Create a new window
    guidelines_window = Toplevel()
    guidelines_window.title("Health and Safety Guidelines")

    # Set the window to full-screen
    guidelines_window.attributes("-fullscreen", True)

    # Create a canvas to hold the background image
    canvas = tk.Canvas(guidelines_window)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Load and resize the background image
    def resize_bg_image(event=None):
        bg_image = Image.open("bg image.jpg")
        bg_image = bg_image.resize((guidelines_window.winfo_width(), guidelines_window.winfo_height()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)
        canvas.bg_photo = bg_photo  # Keep a reference to avoid garbage collection
    
    guidelines_window.bind("<Configure>", resize_bg_image)

    # Create a semi-transparent frame to contain content
    content_frame = tk.Frame(canvas, bg="#f9f9f9", bd=10, relief=tk.RAISED)
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.85, relheight=0.85)

    # Title label for guidelines page
    title_label = tk.Label(content_frame, text="Health and Safety Guidelines", bg="#f9f9f9", fg="#333333", font=("Helvetica", 20, "bold"))
    title_label.pack(pady=20)

    # Create a text widget for displaying the guidelines with improved formatting
    text_widget = Text(content_frame, wrap='word', bg="#ffffff", fg="#333333", font=("Helvetica", 12), padx=20, pady=20)
    text_widget.pack(side='left', fill='both', expand=True)

    # Create a scrollbar for the text widget
    scrollbar = Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Health and safety guidelines content
    safety_guidelines = """
    Health and Safety Guidelines at the Airport
    ===========================================

    1. General Safety:
    - Ensure that all staff are aware of and adhere to the airport's safety procedures.
    - Wear appropriate personal protective equipment (PPE) at all times.
    - Report any unsafe conditions or hazards to the safety officer immediately.

    2. Emergency Procedures:
    - Familiarize yourself with the location of emergency exits and evacuation routes.
    - In case of an emergency, follow the evacuation plan and use the designated assembly points.

    3. Health Protocols:
    - Follow hygiene practices, including frequent hand washing and use of hand sanitizers.
    - Maintain social distancing where required and follow health advisories related to infectious diseases.

    4. Equipment Safety:
    - Regularly inspect and maintain equipment to ensure it is in safe working condition.
    - Ensure that all equipment operators are trained and certified as required.

    5. Incident Reporting:
    - Report any accidents, injuries, or near-misses to the safety officer immediately.

    6. Training and Drills:
    - Participate in regular safety training and drills to stay informed about emergency procedures.

    7. Personal Conduct:
    - Follow all airport policies and procedures to ensure a safe working environment.

    8. Safety Inspections:
    - Conduct regular safety inspections of facilities and equipment.

    For more detailed information, refer to the airport's safety manual or contact the safety department.
    """
    
    # Insert guidelines into text widget
    text_widget.insert('1.0', safety_guidelines)
    text_widget.config(state='disabled')  # Make it read-only

    # Add a close button to exit the guidelines window
    close_button = tk.Button(guidelines_window, text="Close", command=guidelines_window.destroy,
                             bg="#FF5722", fg="#ffffff", font=("Helvetica", 14, "bold"), padx=20, pady=10)
    close_button.pack(side=tk.BOTTOM, pady=20)

    # Bind escape key to exit fullscreen mode
    def exit_fullscreen(event=None):
        guidelines_window.attributes("-fullscreen", False)
        close_button.focus()

    guidelines_window.bind("<Escape>", exit_fullscreen)

    # Add the logo to the top left corner
    logo_img = Image.open("logo airport.png")
    logo_img = logo_img.resize((80, 80), Image.LANCZOS)  # Resize the logo image
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(guidelines_window, image=logo_photo, bg="#f0f0f0")
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.place(x=10, y=10)

    # Trigger the resize event initially to set the background image
    resize_bg_image()

def show_kangra_airport_manual():
    manual_path = "KANGRA CNS MANUAL 2024.pdf"
    
    if os.path.exists(manual_path):
        webbrowser.open(manual_path)
    else:
        tk.messagebox.showerror("Error", "The Kangra Airport Manual file does not exist.")


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
        tk.Label(frame, text="Manufacturer").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Model Number").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame, text="Purchase Date").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(frame, text="Installation Date").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(frame, text="Location").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(frame, text="Warranty Period").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(frame, text="Last Service Date").grid(row=7, column=0, padx=10, pady=10)
        tk.Label(frame, text="Service Interval").grid(row=8, column=0, padx=10, pady=10)
        tk.Label(frame, text="Current Status").grid(row=9, column=0, padx=10, pady=10)

        global equipment_name_entry, manufacturer_entry, model_number_entry, purchase_date_entry, installation_date_entry, location_entry, warranty_period_entry, last_service_date_entry, service_interval_entry, current_status_entry
        equipment_name_entry = tk.Entry(frame)
        manufacturer_entry = tk.Entry(frame)
        model_number_entry = tk.Entry(frame)
        purchase_date_entry = tk.Entry(frame)
        installation_date_entry = tk.Entry(frame)
        location_entry = tk.Entry(frame)
        warranty_period_entry = tk.Entry(frame)
        last_service_date_entry = tk.Entry(frame)
        service_interval_entry = tk.Entry(frame)
        current_status_entry = tk.Entry(frame)

        equipment_name_entry.grid(row=0, column=1, padx=10, pady=10)
        manufacturer_entry.grid(row=1, column=1, padx=10, pady=10)
        model_number_entry.grid(row=2, column=1, padx=10, pady=10)
        purchase_date_entry.grid(row=3, column=1, padx=10, pady=10)
        installation_date_entry.grid(row=4, column=1, padx=10, pady=10)
        location_entry.grid(row=5, column=1, padx=10, pady=10)
        warranty_period_entry.grid(row=6, column=1, padx=10, pady=10)
        last_service_date_entry.grid(row=7, column=1, padx=10, pady=10)
        service_interval_entry.grid(row=8, column=1, padx=10, pady=10)
        current_status_entry.grid(row=9, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_equipment).grid(row=10, columnspan=2, pady=20)

    elif page_type == "maintenance":
        tk.Label(frame, text="Equipment ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Maintenance Date").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Type of Maintenance").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame, text="Details").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(frame, text="Technician Name").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(frame, text="Cost").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(frame, text="Next Scheduled Maintenance").grid(row=6, column=0, padx=10, pady=10)

        global equipment_id_entry, maintenance_date_entry, type_of_maintenance_entry, details_entry, technician_name_entry, cost_entry, next_scheduled_maintenance_entry
        equipment_id_entry = tk.Entry(frame)
        maintenance_date_entry = tk.Entry(frame)
        type_of_maintenance_entry = tk.Entry(frame)
        details_entry = tk.Text(frame, height=5, width=30)
        technician_name_entry = tk.Entry(frame)
        cost_entry = tk.Entry(frame)
        next_scheduled_maintenance_entry = tk.Entry(frame)

        equipment_id_entry.grid(row=0, column=1, padx=10, pady=10)
        maintenance_date_entry.grid(row=1, column=1, padx=10, pady=10)
        type_of_maintenance_entry.grid(row=2, column=1, padx=10, pady=10)
        details_entry.grid(row=3, column=1, padx=10, pady=10)
        technician_name_entry.grid(row=4, column=1, padx=10, pady=10)
        cost_entry.grid(row=5, column=1, padx=10, pady=10)
        next_scheduled_maintenance_entry.grid(row=6, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_maintenance).grid(row=7, columnspan=2, pady=20)

    elif page_type == "fault":
        tk.Label(frame, text="Equipment ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Fault Date").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Fault Description").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame, text="Severity").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(frame, text="Status").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(frame, text="Resolution Details").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(frame, text="Resolved By").grid(row=6, column=0, padx=10, pady=10)

        global fault_equipment_id_entry, fault_date_entry, fault_description_entry, severity_entry, status_entry, resolution_details_entry, resolved_by_entry
        fault_equipment_id_entry = tk.Entry(frame)
        fault_date_entry = tk.Entry(frame)
        fault_description_entry = tk.Text(frame, height=5, width=30)
        severity_entry = tk.Entry(frame)
        status_entry = tk.Entry(frame)
        resolution_details_entry = tk.Text(frame, height=5, width=30)
        resolved_by_entry = tk.Entry(frame)

        fault_equipment_id_entry.grid(row=0, column=1, padx=10, pady=10)
        fault_date_entry.grid(row=1, column=1, padx=10, pady=10)
        fault_description_entry.grid(row=2, column=1, padx=10, pady=10)
        severity_entry.grid(row=3, column=1, padx=10, pady=10)
        status_entry.grid(row=4, column=1, padx=10, pady=10)
        resolution_details_entry.grid(row=5, column=1, padx=10, pady=10)
        resolved_by_entry.grid(row=6, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_fault).grid(row=7, columnspan=2, pady=20)

    elif page_type == "vendor":
        tk.Label(frame, text="Vendor Name").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Contact Person").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Contact Information").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame, text="Services Provided").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(frame, text="Contract Start Date").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(frame, text="Contract End Date").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(frame, text="Terms and Conditions").grid(row=6, column=0, padx=10, pady=10)
        

        global vendor_name_entry, contact_person_entry, contact_information_entry, services_provided_entry, contract_start_date_entry, contract_end_date_entry, terms_and_conditions_entry
        vendor_name_entry = tk.Entry(frame)
        contact_person_entry = tk.Entry(frame)
        contact_information_entry = tk.Text(frame, height=5, width=30)
        services_provided_entry = tk.Text(frame, height=5, width=30)
        contract_start_date_entry = tk.Entry(frame)
        contract_end_date_entry = tk.Entry(frame)
        terms_and_conditions_entry = tk.Text(frame, height=5, width=30)

        vendor_name_entry.grid(row=0, column=1, padx=10, pady=10)
        contact_person_entry.grid(row=1, column=1, padx=10, pady=10)
        contact_information_entry.grid(row=2, column=1, padx=10, pady=10)
        services_provided_entry.grid(row=3, column=1, padx=10, pady=10)
        contract_start_date_entry.grid(row=4, column=1, padx=10, pady=10)
        contract_end_date_entry.grid(row=5, column=1, padx=10, pady=10)
        terms_and_conditions_entry.grid(row=6, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_vendor).grid(row=7, columnspan=2, pady=20)

    elif page_type == "sap":
        tk.Label(frame, text="Equipment ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="SAT Date").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(frame, text="Test Details").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(frame, text="Results").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(frame, text="Passed/Failed").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(frame, text="Tested By").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(frame, text="Comments").grid(row=6, column=0, padx=10, pady=10)

        global sap_equipment_id_entry, sat_date_entry, test_details_entry, results_entry, passed_failed_entry, tested_by_entry, comments_entry
        sap_equipment_id_entry = tk.Entry(frame)
        sat_date_entry = tk.Entry(frame)
        test_details_entry = tk.Text(frame, height=5, width=30)
        results_entry = tk.Text(frame, height=5, width=30)
        passed_failed_entry = tk.Entry(frame)
        tested_by_entry = tk.Entry(frame)
        comments_entry = tk.Text(frame, height=5, width=30)

        sap_equipment_id_entry.grid(row=0, column=1, padx=10, pady=10)
        sat_date_entry.grid(row=1, column=1, padx=10, pady=10)
        test_details_entry.grid(row=2, column=1, padx=10, pady=10)
        results_entry.grid(row=3, column=1, padx=10, pady=10)
        passed_failed_entry.grid(row=4, column=1, padx=10, pady=10)
        tested_by_entry.grid(row=5, column=1, padx=10, pady=10)
        comments_entry.grid(row=6, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=submit_sap).grid(row=7, columnspan=2, pady=20)

def view_page(page_type):
    view_window = tk.Toplevel()
    view_window.title(f"View {page_type.capitalize()} Details")

    # Set the Toplevel window to full screen
    screen_width = view_window.winfo_screenwidth()
    screen_height = view_window.winfo_screenheight()
    view_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Create a frame to hold the content and center it
    frame = tk.Frame(view_window)
    frame.pack(expand=True, fill="both")

    def fetch_data(query):
        # Implement this function to execute the query and return the result
        # For example, using a MySQL connector:
        # import mysql.connector
        # conn = mysql.connector.connect(user='root', password='yourpassword', host='localhost', database='new_airport_db')
        # cursor = conn.cursor()
        # cursor.execute(query)
        # return cursor.fetchall()
        pass

    if page_type == "equipment":
        # Example: Fetch and display equipment details
        query = "SELECT * FROM equipment_info"
        data = fetch_data(query)
        tk.Label(frame, text="Equipment Details").pack(pady=10)
        for row in data:
            tk.Label(frame, text=f"ID: {row[0]} Name: {row[1]}").pack()

    elif page_type == "maintenance":
        # Example: Fetch and display maintenance records
        query = "SELECT * FROM maintenance_records"
        data = fetch_data(query)
        tk.Label(frame, text="Maintenance Records").pack(pady=10)
        for row in data:
            tk.Label(frame, text=f"Equipment ID: {row[0]} Date: {row[1]} Type: {row[2]}").pack()

    elif page_type == "fault":
        # Example: Fetch and display fault reports
        query = "SELECT * FROM fault_reports"
        data = fetch_data(query)
        tk.Label(frame, text="Fault Reports").pack(pady=10)
        for row in data:
            tk.Label(frame, text=f"Equipment ID: {row[0]} Date: {row[1]} Description: {row[2]}").pack()

    elif page_type == "vendor":
        # Example: Fetch and display vendor details
        query = "SELECT * FROM vendor_details"
        data = fetch_data(query)
        tk.Label(frame, text="Vendor Details").pack(pady=10)
        for row in data:
            tk.Label(frame, text=f"Vendor Name: {row[0]} Contact: {row[1]}").pack()

    elif page_type == "sap":
        # Example: Fetch and display SAP details
        query = "SELECT * FROM sap_details"
        data = fetch_data(query)
        tk.Label(frame, text="SAP Details").pack(pady=10)
        for row in data:
            tk.Label(frame, text=f"Equipment ID: {row[0]} SAT Date: {row[1]} Results: {row[2]}").pack()

    # Add a button to close the view window
    tk.Button(view_window, text="Close", command=view_window.destroy).pack(pady=20)

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
    view_window.state('zoomed')
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
        search_row = len(rows) + 1
        tk.Label(view_window, text="Search").grid(row=search_row, column=0)
        search_entry = tk.Entry(view_window)
        search_entry.grid(row=search_row, column=1)
        tk.Button(view_window, text="Search", command=lambda: search_table("sap_details", search_entry.get())).grid(row=search_row, column=2)
        tk.Button(view_window, text="Delete", command=lambda: delete_record("sap_details", rows[0][0] if rows else None)).grid(row=search_row, column=3)
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
        except mysql.connector.Error as e:
            print(f"Error retrieving document paths: {e}")
        finally:
            connection.close()

def fetch_data(table_name):
    """Fetch column names and rows from the specified table."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
            return None, None
        finally:
            connection.close()

def view_page(table_name):
    view_window = tk.Toplevel()
    view_window.title(f"View {table_name.replace('_', ' ').capitalize()}")
    
    def toggle_fullscreen(event=None):
        view_window.attributes('-fullscreen', not view_window.attributes('-fullscreen'))

    # Function to exit fullscreen mode
    def exit_fullscreen(event=None):
        view_window.attributes('-fullscreen', False)
        view_window.state('zoomed')  # Maximize the window

    # Make the window fullscreen
    view_window.attributes('-fullscreen', True)

    # Bind the ESC key to exit fullscreen mode
    view_window.bind("<Escape>", exit_fullscreen)

    logo_path = "logo airport.png"
    logo_image = Image.open(logo_path)
    resized_logo = logo_image.resize((120, 120), Image.LANCZOS)  # Resize to 50x50 pixels
    logo = ImageTk.PhotoImage(resized_logo)
    
    logo_label = tk.Label(view_window, image=logo)
    logo_label.image = logo  # Keep a reference to the image to prevent garbage collection
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Add maximize, minimize, and close buttons
    close_button = tk.Button(view_window, text="Close", command=view_window.destroy)
    close_button.grid(row=0, column=len(fetch_data(table_name)[0]) + 1)

    columns, rows = fetch_data(table_name)
    if columns:
        for col in range(len(columns)):
            tk.Label(view_window, text=columns[col], relief=tk.RAISED, width=15).grid(row=1, column=col)
        
        for row in range(len(rows)):
            for col in range(len(columns)):
                tk.Label(view_window, text=rows[row][col], width=15).grid(row=row+2, column=col)

        # Add search and delete options
        tk.Label(view_window, text="Search").grid(row=len(rows)+3, column=0)
        search_entry = tk.Entry(view_window)
        search_entry.grid(row=len(rows)+3, column=1)
        
        search_button = tk.Button(view_window, text="Search", command=lambda: search_table(table_name, search_entry.get()), bg="#1E90FF", fg="white")  # Airport theme colors
        search_button.grid(row=len(rows)+3, column=2)
        
        delete_button = tk.Button(view_window, text="Delete", command=lambda: delete_record(table_name), bg="#FF4500", fg="white")  # Airport theme colors
        delete_button.grid(row=len(rows)+3, column=3)

def search_table(table_name, search_term):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            columns = fetch_data(table_name)[0]
            query = f"SELECT * FROM {table_name} WHERE CONCAT_WS(' ', {', '.join(['`' + col + '`' for col in columns])}) LIKE %s"
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
            
        except mysql.connector.Error as e:
            print(f"Error searching data: {e}")
        finally:
            connection.close()

def delete_record(table_name):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Prompt user to enter the ID of the record to delete
            record_id = simpledialog.askstring("Delete Record", "Enter the ID of the record to delete:")
            
            if record_id:
                cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
                connection.commit()
                messagebox.showinfo("Success", "Record deleted successfully.")
                
            else:
                messagebox.showerror("Error", "Record ID must be provided.")
                
        except mysql.connector.Error as e:
            print(f"Error deleting data: {e}")
        finally:
            connection.close()
def fetch_notifications():
    # Connect to the MySQL database
    try:
        conn = pymysql.connect(user='root', password='Shagun@123', database='airporthii')
        cursor = conn.cursor()
        query = "SELECT notification_type, description, notification_date FROM notifications ORDER BY notification_date DESC LIMIT 10;"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except pymysql.MySQLError as e:
        print(f"Error fetching notifications: {e}")
        return []

def fetch_notifications():
    return [
        ("Maintenance", "Replace Airfield Lighting", "2024-10-25"),
        ("Inspection", "Runway Surface Check", "2024-10-15"),
        ("Upgrade", "Install New Radar System", "2024-10-05"),
        ("Maintenance", "Test Emergency Generators", "2024-10-28")
    ]

def show_notifications():
    # Fetch notifications from the database (or any other source)
    notifications = fetch_notifications()

    if not notifications:
        messagebox.showinfo("No Notifications", "There are no recent notifications.")
        return

    # Separate notifications into upcoming and passed based on the date
    current_date = datetime.now().date()
    upcoming_notifications = []
    passed_notifications = []

    for notification in notifications:
        notification_type, description, notification_date_str = notification
        notification_date = datetime.strptime(notification_date_str, "%Y-%m-%d").date()

        if notification_date >= current_date:
            upcoming_notifications.append(notification)
        else:
            passed_notifications.append(notification)

    # Create a new window to display notifications
    notifications_window = tk.Toplevel()
    notifications_window.title("Recent Notifications")
    
    # Create a text widget to show the notifications
    notifications_text = tk.Text(notifications_window, width=80, height=20, wrap=tk.WORD)
    notifications_text.pack(padx=10, pady=10)

    # Insert upcoming notifications
    notifications_text.insert(tk.END, "Upcoming Maintenance:\n\n", "title")
    for notification in upcoming_notifications:
        notification_type, description, notification_date = notification
        notifications_text.insert(tk.END, f"{notification_date} - {notification_type}: {description}\n")

    # Insert a separator between upcoming and passed notifications
    notifications_text.insert(tk.END, "\n" + "-"*40 + "\n\n", "separator")

    # Insert passed notifications
    notifications_text.insert(tk.END, "Past Maintenance:\n\n", "title")
    for notification in passed_notifications:
        notification_type, description, notification_date = notification
        notifications_text.insert(tk.END, f"{notification_date} - {notification_type}: {description}\n")

    # Make the text widget read-only
    notifications_text.config(state=tk.DISABLED)

    # Apply some basic formatting for the text
    notifications_text.tag_configure("title", font=("Helvetica", 14, "bold"), justify=tk.LEFT)
    notifications_text.tag_configure("separator", justify=tk.CENTER)

class CombinedNotificationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Airport Maintenance System")
        self.geometry("800x600")
        
        # Create a button to trigger a notification
        self.notify_button = tk.Button(self, text="Show Notifications", command=self.show_notification)
        self.notify_button.pack(pady=20)
        
        self.notification_frame = None
        self.flash_icon = None

    def show_notification(self):
        if self.notification_frame:
            self.notification_frame.destroy()
        
        if self.flash_icon:
            self.flash_icon.destroy()
        
        self.notification_frame = tk.Frame(self, bg="yellow", padx=20, pady=10)
        self.notification_frame.pack(side="bottom", fill="x")
        
        label = tk.Label(self.notification_frame, text="Critical Issue Alert!", bg="yellow", font=("Helvetica", 16))
        label.pack()
        
        # Create a canvas for the flashing icon
        self.flash_icon = tk.Canvas(self, width=50, height=50, bg="yellow", highlightthickness=0)
        self.flash_icon.pack(pady=10, side="bottom")
        
        self.icon = self.flash_icon.create_oval(10, 10, 40, 40, fill="red")
        
        self.flash()

    def flash(self):
        if self.flash_icon:
            current_fill = self.flash_icon.itemcget(self.icon, "fill")
            new_fill = "yellow" if current_fill == "red" else "red"
            self.flash_icon.itemconfig(self.icon, fill=new_fill)
            
            self.after(500, self.flash)  # Change color every 500 ms
        
        self.after(5000, self.hide_notification)  # Hide notification after 5 seconds

    def hide_notification(self):
        if self.notification_frame:
            self.notification_frame.destroy()
        if self.flash_icon:
            self.flash_icon.destroy()


def open_help_desk():
    chatbot_window = tk.Toplevel(root)
    chatbot_window.title("Help Desk Chatbot")
    chatbot_window.geometry("600x500")
    
    try:
        # Load the background image
        bg_image = Image.open("c:\\Users\\HP\\Desktop\\botmage.jpg")  # Ensure the path is correct
        bg_image = bg_image.resize((600, 500), Image.LANCZOS)  # Resize if needed
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(chatbot_window, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)  # Stretch the background image to cover the window
        chatbot_window.bg_photo = bg_photo  # Keep a reference to avoid garbage collection
    except Exception as e:
        print(f"Error loading background image: {e}")

    # Load and place the logo
    try:
        logo_image = Image.open("chatbot.jpg")  # Path to your logo image
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)  # Resize logo if needed
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(chatbot_window, image=logo_photo, bg="#f0f0f0")  # Set background color to match
        logo_label.place(x=10, y=10)  # Place in the top left corner
        chatbot_window.logo_photo = logo_photo  # Keep a reference to avoid garbage collection
    except Exception as e:
        print(f"Error loading logo image: {e}")
        
    def animate_welcome_message():
        welcome_text = "Welcome to the Help Desk Chatbot! How can I assist you today?"
        animated_label.config(text=welcome_text)
        animated_label.place(x=150, y=450)
        animate_text(welcome_text)

    def animate_text(text):
        for i in range(len(text) + 1):
            animated_label.config(text=text[:i])  # Update label text
            chatbot_window.update()  # Refresh the window
            chatbot_window.after(100)  # Delay for animation effect
        chatbot_window.after(2000, clear_text)  # Wait and clear text after 2 seconds

    def clear_text():
        animated_label.config(text="")
        # Restart animation
        animate_welcome_message()

    # Create animated label for welcome message
    animated_label = tk.Label(chatbot_window, text="", font=("Arial", 12, "italic"), bg="#f0f0f0", fg="blue")
    animate_welcome_message()  # Start the animation

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
            "view equipment": "To view equipment details, enter the equipment ID.",
            "add equipment": "To add a new piece of equipment, please go to the 'Add Details' section and fill in the required information.",
            "view equipment list": "You can view the list of all equipment in the 'View Details' section.",
            "maintenance schedule": "To view the maintenance schedule, provide the equipment ID.",
            "next maintenance": "To check the next scheduled maintenance, please provide the equipment ID.",
            "upcoming maintenance": "You can check upcoming maintenance by providing the equipment ID for the specific equipment.",
            "add maintenance record": "To add a maintenance record, please use the 'Add Maintenance' section and provide the equipment ID along with the maintenance details.",
            "view maintenance records": "To view maintenance records, enter the equipment ID or navigate to the 'View Details' section.",
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

    def show_faq():
        """Display the FAQ section."""
        faq_window = tk.Toplevel(chatbot_window)
        faq_window.title("Frequently Asked Questions")
        faq_window.geometry("400x400")

        faq_text = tk.Text(faq_window, wrap=tk.WORD, state=tk.NORMAL)
        faq_text.insert(tk.END, "Frequently Asked Questions:\n\n")

        faqs = {
            "How do I check my flight status?": "You can check the flight status on our flight information page.",
            "What are the airport's security procedures?": "Please follow the guidelines posted at the airport for a smooth security screening process.",
            "How can I find parking information?": "Parking information and rates are available on our parking page.",
            "Where can I get help with lost luggage?": "Report lost luggage to the airline's baggage claim office or contact our lost luggage department.",
            "Is there free Wi-Fi at the airport?": "Yes, free Wi-Fi is available throughout the airport. Connect to the 'Airport_WiFi' network.",
            "How can I add details in the system?": "Use the 'Add Details' section in the application to add equipment, maintenance, faults, or vendor details.",
            "How do I view added details?": "Go to the 'View Details' section in the application to see added information for equipment, maintenance, faults, and vendors."
        }

        for question, answer in faqs.items():
            faq_text.insert(tk.END, question + "\n" + answer + "\n\n")

        faq_text.config(state=tk.DISABLED)
        faq_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)



    title_label = tk.Label(chatbot_window, text="Welcome to the Help Desk Chatbot", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Create the chat history area
    chat_history = tk.Text(chatbot_window, wrap=tk.WORD, state=tk.DISABLED, bg="#f5f5f5")
    chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create the user entry area
    user_entry = tk.Entry(chatbot_window, width=50)
    user_entry.pack(pady=10, padx=10, side=tk.LEFT, fill=tk.X, expand=True)

    # Create the send button
    send_button = tk.Button(chatbot_window, text="Send", command=send_message, bg="blue", fg="white")
    send_button.pack(pady=10, padx=10, side=tk.RIGHT)

    # Create the FAQ button
    faq_button = tk.Button(chatbot_window, text="FAQ", command=show_faq, bg="blue", fg="white")
    faq_button.pack(pady=10, padx=10, side=tk.RIGHT)

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
    # Create a modal Toplevel window (popup) for "About Us"
    about_window = tk.Toplevel(root)
    about_window.title("About Us")
    
    # Set the size and center the window as a popup
    window_width, window_height = 600, 400  # Set appropriate dimensions for the popup
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    about_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    about_window.resizable(False, False)
    
    # Make the window modal (popup behavior)
    about_window.transient(root)
    about_window.grab_set()  # Disable interaction with other windows until this one is closed

    # Create a canvas for the background
    canvas = tk.Canvas(about_window, width=window_width, height=window_height)
    canvas.pack(fill=tk.BOTH, expand=True)

    def resize_bg_image(event=None):
        # Load and resize the background image for the popup
        bg_image = Image.open("bgggg.jpg")
        bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)
        canvas.bg_photo = bg_photo  # Avoid garbage collection

    about_window.bind("<Configure>", resize_bg_image)
    
    # Create a frame for the content with a semi-transparent background
    content_frame = tk.Frame(about_window, bg="#f2f2f2", bd=10, relief=tk.FLAT)
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.9, relheight=0.9)

    # Add title label with enhanced font style
    title_label = tk.Label(content_frame, text="Airports Authority of India", font=("Helvetica", 22, "bold"), fg="#002b5c", bg="#f2f2f2")
    title_label.pack(pady=(20, 10))

    # Add contact information with professional font style
    about_text = (
        "Kangra Airport, Gaggal, Himachal Pradesh\n\n"
        "Email: contact@kangraairport.com\n"
        "Address: Gaggal, District Kangra, Himachal Pradesh\n"
    )
    info_label = tk.Label(content_frame, text=about_text, font=("Helvetica", 14), fg="#333333", bg="#f2f2f2", justify=tk.LEFT)
    info_label.pack(pady=(0, 20))

    # Button to visit the airport's website with modern styling
    def visit_website():
        webbrowser.open("https://www.aai.aero/en/airports/kangra")

    visit_button = tk.Button(content_frame, text="Visit Website", command=visit_website, font=("Helvetica", 12, "bold"), 
                             bg="#0055A4", fg="#ffffff", padx=20, pady=5)
    visit_button.pack(pady=(0, 10))

    # Button to close the popup window with modern styling
    close_button = tk.Button(content_frame, text="Close", command=about_window.destroy, font=("Helvetica", 12, "bold"), 
                             bg="#FF5722", fg="#ffffff", padx=20, pady=5)
    close_button.pack(pady=(10, 0))

    # Trigger the background image resize
    resize_bg_image()



def show_maintenance_info():
    # Create a new Toplevel window for "Maintenance Information"
    maintenance_window = tk.Toplevel(root)
    maintenance_window.title("Maintenance Information")

    # Set the window to full-screen
    maintenance_window.attributes("-fullscreen", True)

    # Create a canvas to hold the background image
    canvas = tk.Canvas(maintenance_window)
    canvas.pack(fill=tk.BOTH, expand=True)

    def resize_bg_image(event=None):
        # Load and resize the background image to fit the window
        bg_image = Image.open("bgggg.jpg")
        bg_image = bg_image.resize((maintenance_window.winfo_width(), maintenance_window.winfo_height()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Update the background image on the canvas
        canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)
        canvas.bg_photo = bg_photo  # Keep a reference to avoid garbage collection

    # Bind resize event to the function
    maintenance_window.bind("<Configure>", resize_bg_image)

    # Add the logo at the top-left corner
    logo_img = Image.open("logo airport.png")
    logo_img = logo_img.resize((50, 50), Image.LANCZOS)  # Resize the logo image
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(maintenance_window, image=logo_photo, bg="#ffffff")
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.place(x=10, y=10)  # Place the logo at the top-left corner

    # Create a frame for content with padding and a semi-transparent background
    content_frame = tk.Frame(canvas, bg="#f9f9f9", bd=10, relief=tk.RAISED)
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.95, relheight=0.8)

    # Create a text widget for displaying the information
    text_widget = tk.Text(content_frame, wrap='word', bg="#ffffff", fg="#333333", font=("Arial", 11), padx=10, pady=10)
    text_widget.pack(side='left', fill='both', expand=True)

    # Create a scrollbar for the text widget
    scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=text_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Insert the maintenance information into the text widget
    maintenance_info = """
    PURPOSE OF AIRPORT MAINTENANCE

    An airport, being an important part of the Aeronautical Infrastructure, has to meet high Safety Standards. The required level of safety can only be achieved by proper Maintenance of all the elements composing an airport. Maintenance includes measures to keep or restore the operational function as well as measures to check and to evaluate the present function of an element.

    The basic components of maintenance are:
    - Inspection
    - Servicing and Overhaul
    - Repair

    Assist Airports with the following:
    - Compile Standard Operating Procedures, predictive preventative maintenance plans and schedules for equipment, infrastructure and facilities.
    - Assist with Service Level Agreements for Infrastructure and Equipment.

    MAINTENANCE OF VISUAL AIDS:
    - Spare parts management
    - Light maintenance schedule
    - Basic maintenance programme for approach, runway and taxiway light systems

    ADDITIONAL MAINTENANCE PROGRAMMES:
    - Maintenance programme for special types of lights
    - Maintenance of docking guidance systems
    - Light measurement and lamp replacement
    - Removal of water from light fixtures

    MAINTENANCE OF AIRPORT ELECTRICAL SYSTEMS:
    - Schedule of maintenance for power cables, transformers, and regulators
    - Maintenance of relay and switch cabinets
    - Fixed 400 Hz ground power supplies and apron floodlighting

    MAINTENANCE OF PAVEMENTS:
    - Surface repair techniques for both concrete and bituminous pavements
    - Joint maintenance and crack repair
    - Sweeping and cleaning of pavements to maintain surface quality

    CLEANING OF SURFACES:
    - Removal of contaminants, rubber deposits, and fuel/oil residues
    - Regular monitoring of surface conditions

    REMOVAL OF SNOW AND ICE:
    - Implementation of snow plans and responsibilities
    - Training personnel on snow removal procedures

    DRAINAGE SYSTEMS MAINTENANCE:
    - Regular cleaning of slot drains, drain pipes, and oil separators
    - Maintenance of water hydrants and drainage basins

    MAINTENANCE OF UNPAVED AREAS:
    - Green area maintenance, including grass management
    - Equipment for grass maintenance and treatment

    REMOVAL OF DISABLED AIRCRAFT:
    - Efficient removal plan and personnel training
    - Maintenance of removal equipment

    MAINTENANCE OF EQUIPMENT AND VEHICLES:
    - Regular schedules for vehicle maintenance
    - Management of workshops for equipment upkeep

    MAINTENANCE OF BUILDINGS AND FACILITIES:
    - Regular checks on lighting, air conditioning, heating facilities, and baggage systems
    - Safety inspections of fixed fire protection installations

    SPECIFIC EQUIPMENT USED AT KANGRA AIRPORT:
    - FIDS (Flight Information Display Systems)
    - DVOR (Doppler VHF Omni-Directional Radio Range)
    - PAPI (Precision Approach Path Indicator)
    - Ground power units for aircraft
    - Baggage handling systems and conveyor belts

    ADDITIONAL NOTES:
    - Regularly update maintenance logs and schedules.
    - Ensure all personnel are trained on safety and operational procedures.
    """
    
    # Insert the maintenance info into the text widget with formatted paragraphs
    text_widget.insert('1.0', maintenance_info)
    text_widget.config(state='disabled')  # Make the text widget read-only

    # Add a close button with standard appearance
    close_button = tk.Button(maintenance_window, text="Close", command=maintenance_window.destroy, bg="#FF5722", fg="#ffffff", font=("Arial", 12, "bold"), padx=10, pady=5)
    close_button.pack(side=tk.BOTTOM, pady=20)

    # Add a button to exit fullscreen mode
    def exit_fullscreen(event=None):
        maintenance_window.attributes("-fullscreen", False)
        close_button.focus()

    maintenance_window.bind("<Escape>", exit_fullscreen)

# Example usage
# show_maintenance_info()
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

    background_image_path = "bgggg.jpg"

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
    logo_image_path = "logo airport.png"
    logo_image = Image.open(logo_image_path)
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Resize the image to 100x100 pixels
    logo_image_tk = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(root, image=logo_image_tk, bg='white')
    logo_label.place(x=2, y=2)


    
    # Create animated title
    title_label = tk.Label(
    root,
    text="AIRPORTS AUTHORITY OF INDIA",
    font=("Helvetica", 24, "bold"),
    bg='#e0f7fa',  # Light blue background
    fg='#00796b',  # Dark teal text color
    relief='raised',  # Slightly raised effect
    padx=10,  # Padding for better spacing
    pady=5
)
    title_label.place(relx=0.5, y=10, anchor='n')

     # Welcome Message
    welcome_message = tk.Label(
    root,
    text="Welcome to Kangra Airport Maintenance and Management System",
    font=("Helvetica", 20, "bold"),
    bg='#e0f7fa',  # Matching light blue background
    fg='#004d40',  # Deep green text color
    wraplength=600,  # Allow text wrapping
    justify='center',  # Center the text
)
    welcome_message.place(relx=0.5, rely=0.1, anchor='n')

    # Info Text
    info_text = (
    "Kangra Airport, or Gaggal Airport, is a bustling hub in the scenic Kangra Valley, "
    "nestled in the Himalayas. With a single runway, it connects thousands of domestic and "
    "international travelers each year, supporting tourism and business in Himachal Pradesh. "
    "Renowned for its safety and modern facilities, it plays a vital role in regional transport."
)

    info_label = tk.Label(
    root,
    text=info_text,
    font=("Segoe UI", 12, "italic"),  # Italic font
    fg='#333333',  # Dark grey text color
    wraplength=700,  # Text wrapping for better readability
    justify='left',
    padx=10,  # Horizontal padding
    pady=10,  # Vertical padding
    bg=root.cget("bg")  # Set background color to match the root's background
)

# Place label lower in the window
    info_label.place(relx=0.5, rely=0.85, anchor='n', relwidth=0.8)  

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




    logout_button = create_button(root, "Logout", logout, LOGOUT_COLOR)
    logout_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=40)

    notification_button = create_button(root, "Show Notifications", show_notification, NOTIFICATION_COLOR)
    notification_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
    

    
    features_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Features", menu=features_menu)
    features_menu.add_command(label="Show Airport Map", command=create_interactive_map)
    features_menu.add_command(label="Health and Safety Guidelines", command=show_health_safety_guidelines)
    features_menu.add_command(label="Kangra Airport CNS Manual", command=show_kangra_airport_manual)
    # Adding the "ATSEP Facilities" option to the "Features" menu
    features_menu.add_command(label="ATSEP Facilities", command=show_atsep_facilities)
    # Create the frame for notifications
    notifications_frame = tk.Frame(root, bg="#f0f0f0")
    notifications_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    


# Add a button to show notifications
    notifications_button = tk.Button(notifications_frame, text="Show Recent Notifications", command=show_notifications, bg="#003366", fg="white")
    notifications_button.pack(pady=10)


    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
