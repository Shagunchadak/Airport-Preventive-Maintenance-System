DROP DATABASE IF EXISTS new_airport_db;
CREATE DATABASE airporthii;
USE airporthii;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS maintenance_records;
DROP TABLE IF EXISTS fault_reports;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS vendor_details;
DROP TABLE IF EXISTS equipment_info;
DROP TABLE IF EXISTS sap_details;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS sat_details;

-- Create tables
CREATE TABLE equipment_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    model_number VARCHAR(100),
    purchase_date DATE,
    installation_date DATE,
    location VARCHAR(255),
    warranty_period INT,
    last_service_date DATE,
    service_interval INT,
    current_status ENUM('operational', 'under maintenance') NOT NULL
);

CREATE TABLE maintenance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    maintenance_date DATE,
    type_of_maintenance ENUM('routine', 'corrective', 'preventive') NOT NULL,
    details TEXT,
    technician_name VARCHAR(100),
    cost DECIMAL(10, 2),
    next_scheduled_maintenance DATE,
    FOREIGN KEY (equipment_id) REFERENCES equipment_info(id)
);

CREATE TABLE fault_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    fault_date DATE,
    fault_description TEXT,
    severity ENUM('minor', 'major', 'critical') NOT NULL,
    status ENUM('reported', 'in progress', 'resolved') NOT NULL,
    resolution_details TEXT,
    resolved_by VARCHAR(100),
    FOREIGN KEY (equipment_id) REFERENCES equipment_info(id)
);

CREATE TABLE vendor_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    contact_information TEXT,
    services_provided TEXT,
    contract_start_date DATE,
    contract_end_date DATE,
    terms_and_conditions TEXT
);

CREATE TABLE sat_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    sat_date DATE,
    test_details TEXT,
    results TEXT,
    passed_failed ENUM('passed', 'failed') NOT NULL,
    tested_by VARCHAR(100),
    comments TEXT,
    bill_file_path VARCHAR(255), -- Path for the uploaded bill file
    agreement_file_path VARCHAR(255), -- Path for the uploaded agreement file
    FOREIGN KEY (equipment_id) REFERENCES equipment_info(id)
);

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    notification_type ENUM('upcoming maintenance', 'fault alert', 'vendor contract expiration', 'critical issue') NOT NULL,
    description TEXT NOT NULL,
    notification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example queries for testing
SHOW TABLES;

-- Example search queries
SELECT * FROM equipment_info WHERE CONCAT_WS(' ', name, manufacturer, model_number, location) LIKE '%search_term%';
SELECT * FROM maintenance_records WHERE CONCAT_WS(' ', maintenance_date, type_of_maintenance, details, technician_name) LIKE '%search_term%';
SELECT * FROM fault_reports WHERE CONCAT_WS(' ', fault_date, fault_description, severity, status, resolution_details) LIKE '%search_term%';
SELECT * FROM vendor_details WHERE CONCAT_WS(' ', vendor_name, contact_person, contact_information, services_provided) LIKE '%search_term%';
SELECT * FROM sat_details WHERE CONCAT_WS(' ', sat_date, test_details, results, passed_failed, tested_by) LIKE '%search_term%';
SELECT * FROM feedback;
SELECT * FROM notifications;
ALTER TABLE vendor_details
ADD COLUMN equipment_id INT,
ADD FOREIGN KEY (equipment_id) REFERENCES equipment_info(id);
RENAME TABLE sat_details TO sap_details;
SELECT * FROM sap_details;