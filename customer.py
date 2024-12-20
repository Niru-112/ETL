import csv
from account import generate_random_customers
import os

def create_customer(filename):
    # Input and output file names
    # filename = 'account.csv'
    customer_filename = 'customer.csv'

    # Check if account.csv exists
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"{filename} not found. Ensure the file exists.")

    # Read the number of entries in account.csv
    with open(filename, mode='r', newline='') as account_file:
        account_reader = csv.DictReader(account_file)
        accounts = list(account_reader)  # Load all rows into a list

    # Extract only the first 3 columns: 'customer_id', 'customer_name', 'address1'
    fieldnames = ['customer_id', 'customer_name']
    filtered_data = [
        {key: row.get(key,) for key in fieldnames} for row in accounts
    ]

    # Write the filtered data to customer.csv
    with open(customer_filename, mode='w', newline='') as customer_file:
        writer = csv.DictWriter(customer_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)
        
    return filtered_data

# {key: row[key] for key in fieldnames}