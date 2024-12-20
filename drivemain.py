from account import generate_random_customers,create_or_append_account
from customer import create_customer
from address import create_address
from attribute import create_attribute_data
import sys
import io
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import csv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

def log_error(error_message):
    with open('error.txt', 'a') as error_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_file.write(f"{timestamp} -> {error_message}\n")
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
    error_filename = f'account_err_{timestamp}.csv' 
    file_exists = os.path.isfile(error_filename)
    
    with open(error_filename, 'a', newline='') as error_file:
        csv_writer = csv.writer(error_file)
        if not file_exists:
            csv_writer.writerow(['timestamp', 'error_message'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        csv_writer.writerow([timestamp, error_message])
        

def connect_to_database():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='localhost',       # Hostname (localhost for local database)
            user='root',   # Replace with your MySQL username
            password='', # Replace with your MySQL password
            database='ddsp'  # Replace with your database name
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            # Perform operations here
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            for table in cursor.fetchall():
                print(table)

    except Error as e:
        error_message = f"Error while connecting to MySQL: {e}"
        print(error_message)
        log_error(error_message)

    finally:
        # Close the connection
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")
        
                    
def insert_to_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Database connection details
    host = 'localhost'  # Usually localhost when using XAMPP
    user = 'root'       # Default MySQL username
    password = ''       # Default MySQL password is empty
    database = 'ddsp'  # Replace with your database name

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        print("Database connection successful!")

        # Open the CSV file
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row

            # Insert data into the account table
            query = """
            INSERT INTO account (
                customer_id, customer_name, billing_address1, billing_address2, billing_city, billing_state, 
                billing_country, shipping_address1, shipping_address2, shipping_city, shipping_state, 
                shipping_country, categories, sub_categories
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for row in csv_reader:
                try:
                    # Check for None or empty values before inserting
                    if any(value is None or value == '' for value in row):
                        raise ValueError("Row contains None or empty values")

                    cursor.execute(query, tuple(row))
                    # print(f"Inserted row: {row}") 
                     
                except Exception as e:
                    error_message = f"Error inserting row {row}: {e}"
                    # print(error_message)
                    log_error(error_message)  # Log the error to error.txt

            # Commit the transaction
            connection.commit()
            print("Data inserted successfully!")

    except mysql.connector.Error as e:
        error_message = f"Error occurred in {filename}: {e}"
        print(error_message)
        log_error(error_message)
        
    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")
            
def upload_file(file_name, file_path, mime_type):    
    file_metadata = {'name': file_name}  # Set the file name in Drive
    media = MediaFileUpload(file_path, mimetype=mime_type)
    try:
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()  # Execute the API call
        print(f"{file_name} uploaded successfully. File ID: {file['id']}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Function to find a file ID by name
def get_file_id(service, file_name):
    try:
        results = service.files().list(q=f"name='{file_name}'", fields="files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print(f"No file found with name: {file_name}")
            return None
        print(f"File ID for {file_name}: {items[0]['id']}")
        return items[0]['id']
    except Exception as e:
        print(f"Error getting file ID: {e}")
        return None

# Function to download a file from Google Drive
def download_file(service, file_id, output_path):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")
        
        with open(output_path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        print(f"File downloaded successfully to {output_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Function to delete a file from Google Drive
def delete_file(service, file_name):
    file_id = get_file_id(service, file_name)
    if not file_id:
        print(f"File with name {file_name} not found to delete.")
        return False
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"File '{file_name}' deleted successfully.")
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

            
            
# Set default encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
filename = f'account_{timestamp}.csv'

with open(filename, mode='w') as file:
    file.write("customer_id, customer_name , billing_address1, billing_address2,billing_city, billing_state, billing_country,shipping_address1, shipping_address2, shipping_city,shipping_state, shipping_country,categories,sub_categories\n")  # Example header
    
num_customers =  50 #int(input("Enter The number of customers you want to print: "))
  
data = generate_random_customers(num_customers,missing_rows=20)
print(len(data)) #in memory

data2 = create_or_append_account(data,filename)
print(len(data2))
print(f"Accounts have been written to {filename}.") #in csv on disk

data3 = create_customer(filename)
print(len(data3)) # transform on disk

data4= create_address(data) 
print(data4) # transform on disk

data5 = create_attribute_data(filename)
print(data5)# transform on disk

# Authenticate and create the servic
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None

# Check if token.pickle exists
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If no valid credentials, perform login flow
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Save credentials for future use
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Build the Drive API service
service = build('drive', 'v3', credentials=creds)

# Function to upload a file to Google Drive
def main():
    # Step 1: Generate dynamic filename and output path
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format the current date and time
    file_name = f"account_{current_time}.csv"  # Dynamic filename
    output_path = os.path.join(r"D:\ETL", file_name)  # Dynamic output path based on the generated filename

    print(f"File name: {file_name}")
    print(f"Output path: {output_path}")

    # Step 2: Upload the file to Google Drive
    upload_file(file_name, output_path, 'text/csv')  # Upload file to Drive

    # Step 3: Download the file (Example)
    file_id = get_file_id(service, file_name)
    if file_id:
        download_file(service, file_id, output_path)
    
    # Step 4: Insert customer data into the database (Placeholder)
    # insert_to_database()  # Assuming this function handles the database insertion
    
    # Step 5: Delete the file from Google Drive
    delete_file(service, file_name)

# Run the main function
if __name__ == "__main__":
    connect_to_database()
    insert_to_database()
    main()
