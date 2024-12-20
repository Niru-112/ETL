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
from datetime import datetime


# Set default encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
filename = f'account_{timestamp}.csv'

with open(filename, mode='w') as file:
    file.write("customer_id, customer_name , billing_address1, billing_address2,billing_city, billing_state, billing_country,shipping_address1, shipping_address2, shipping_city,shipping_state, shipping_country,categories,sub_categories\n")  # Example header
    
num_customers =  50 #int(input("Enter The number of customers you want to print: "))
  
data = generate_random_customers(num_customers,missing_rows=20)
print(len(data))

data2 = create_or_append_account(data,filename)
print(len(data2))
print(f"Accounts have been written to {filename}.")

data3 = create_customer(filename)
print(len(data3))

data4= create_address(data) 
print(data4)

data5 = create_attribute_data(filename)
print(data5)

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
    filename = f'account_{timestamp}.csv'
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
                    print(f"Inserted row: {row}") 
                     
                except Exception as e:
                    error_message = f"Error inserting row {row}: {e}"
                    print(error_message)
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

if __name__ == "__main__":
    connect_to_database()
    insert_to_database()