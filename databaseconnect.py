import mysql.connector
from mysql.connector import Error
import csv
from datetime import datetime
import main

def log_error(error_message):
    with open('error.txt', 'a') as error_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_file.write(f"{timestamp} -> {error_message}\n")

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
        # transposed_data = list(map(list, zip(*data)))
        # Open the CSV file
        with open('account.csv', 'r') as file:
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
            # for row in transposed_data:
            for row in csv_reader:
                cursor.execute(query, tuple(row))

            # Commit the transaction
            connection.commit()
            print("Data inserted successfully!")

    except mysql.connector.Error as e:
        error_message = f"Error: {e}"
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