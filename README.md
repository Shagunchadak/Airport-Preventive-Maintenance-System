# Airport-Preventive-Maintenance-System
The Airport Maintenance System is a robust and user-friendly application designed to streamline maintenance and operational workflows at Kangra Airport. Developed using Python and Tkinter for the GUI, and integrated with MySQL for data storage, this project effectively manages equipment, maintenance schedules, fault reporting, vendor details, and site acceptance tests (SAT). The application includes features such as notifications for upcoming maintenance, file uploads for SAP details, and detailed views of equipment and operational facilities.

Features
Login System:

Secure login system with username and password validation.
The login page is designed with an airport theme, including a logo and dynamic animations.
Add and View Details:

Add and view options for equipment details, maintenance schedules, fault records, vendor details, and SAP details.
Each section supports smooth transitions and is accessible via a user-friendly menu bar.
Notification System:

Automatic alerts for upcoming maintenance schedules, enhancing operational efficiency.
File Upload Functionality:

Upload and view PDF files for bills and agreements in the SAP details section.
Search and Delete:

Advanced search and delete functionality across all sections, allowing users to manage data efficiently.
ATSEP Facilities Information:

A dedicated section detailing the various technical systems used at Kangra Airport, such as VHF, NDB, DVOR, HPDME, and W/T.
Comprehensive explanations for each facility, highlighting their roles and functionalities.
Full-Screen Scrolling Interface:

The ATSEP Facilities page opens in full-screen mode with a scrollable interface controlled via the keyboard and mouse.
About Us Section:

Information about the airport and its contact details is provided in the menu bar for easy reference.
User Interface Design
Login Page
The login page sets the tone for the application with a clean, professional design. It includes:

An airport-themed background image.
The Airport Authority of India logo prominently displayed.
An animated title and intuitive input fields.
Main Dashboard
The main dashboard features:

A top menu bar with options like Add Details, View Details, About Us, and ATSEP Facilities.
Notifications and logout buttons positioned at the right corner.
Tabs on the left for easy navigation and management of details.
Details Pages
Each section for equipment, maintenance, faults, vendors, and SAP details includes:

Intuitive forms for adding and managing records.
Options to view data in a tabular format, complete with column headers.
ATSEP Facilities Page
This section provides detailed descriptions of technical systems at Kangra Airport.
Includes a Close Button for seamless navigation back to the dashboard.
Database Structure
The project is backed by a robust MySQL database with tables for:

equipment_info: Stores details about airport equipment.
maintenance_records: Logs maintenance schedules and history.
fault_reports: Tracks reported issues and faults.
vendor_details: Manages information about vendors and service providers.
sap_details: Stores site acceptance test details, including uploaded files.
users: Maintains login credentials and user information.
Technologies Used
Frontend: Python, Tkinter
Backend: MySQL
Additional Libraries: ttk for styled widgets

Create a database named new_airport_db.
Run the SQL script provided in the repository to create necessary tables.
Run the application:

Future Enhancements
Integration of more advanced notification systems via email or SMS.
Enhanced reporting and analytics for maintenance and operational data.
Mobile-responsive design for broader accessibility.
