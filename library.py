import random
import os
import csv

# Sample data for generating random customers
sample_names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Davis"]
sample_streets = ["123 Elm St", "456 Oak St", "789 Pine St", "101 Maple St", "202 Birch St"]
sample_cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
sample_states = ["NY", "CA", "IL", "TX", "AZ"]
sample_countries = ["USA", "Canada", "UK", "Australia", "Germany"]

def generate_random_customers(num_customers):
    customers = []

    for _ in range(num_customers):
        customer = {
            'customer_id': random.randint(100, 999),  # Random customer ID
            'customer_name': random.choice(sample_names),  # Random customer name
            'billing_address1': random.choice(sample_streets),  # Random billing address line 1
            'billing_address2': random.choice(sample_streets),  # Random billing address line 2
            'billing_city': random.choice(sample_cities),  # Random billing city
            'billing_state': random.choice(sample_states),  # Random billing state
            'billing_country': random.choice(sample_countries),  # Random billing country
            'shipping_address1': random.choice(sample_streets),  # Random shipping address line 1
            'shipping_address2': random.choice(sample_streets),  # Random shipping address line 2
            'shipping_city': random.choice(sample_cities),  # Random shipping city
            'shipping_state': random.choice(sample_states),  # Random shipping state
            'shipping_country': random.choice(sample_countries)  # Random shipping country
        }
        customers.append(customer)

    return customers

def create_or_append_account(customers):
    filename='account.csv'
    # Check if the file exists to determine if we need to write headers
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        fieldnames = ['customer_id', 'customer_name', 'billing_address1', 'billing_address2',
                      'billing_city', 'billing_state', 'billing_country',
                      'shipping_address1', 'shipping_address2', 'shipping_city',
                      'shipping_state', 'shipping_country']
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()  # Write the header row with labels

        # Write the customer data
        for customer in customers:
            writer.writerow(customer)

def create_customer():

    # Read from the account.csv file
    filename = 'account.csv'
    customer_data = []

    # Check if the file exists before trying to read it
    if os.path.isfile(filename):
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            # Read each row and extract customer_id and customer_name
            for row in reader:
                customer_data.append({
                    'customer_id': row['customer_id'],
                    'customer_name': row['customer_name']
                })

    # Write the extracted data to customer.csv
    with open('customer.csv', mode='w', newline='') as file:
        fieldnames = ['customer_id', 'customer_name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the customer data
        for customer in customer_data:
            writer.writerow(customer)
            
def create_address(customers):
    filename = 'address.csv'  # Specify the filename for addresses

    # Check if the file exists to determine if we need to write headers
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        fieldnames = ['customer_id', 'billing_type', 'address1', 'address2', 'city', 'state', 'country']
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()  # Write the header row with labels

        # Loop through each customer to write billing and shipping addresses
        for customer in customers:
            # Write billing address
            billing_data = {
                'customer_id': customer['customer_id'],
                'billing_type': 'billing',
                'address1': customer['billing_address1'],
                'address2': customer['billing_address2'],
                'city': customer['billing_city'],
                'state': customer['billing_state'],
                'country': customer['billing_country']
            }
            writer.writerow(billing_data)

            # Write shipping address
            shipping_data = {
                'customer_id': customer['customer_id'],
                'billing_type': 'shipping',
                'address1': customer['shipping_address1'],
                'address2': customer['shipping_address2'],
                'city': customer['shipping_city'],
                'state': customer['shipping_state'],
                'country': customer['shipping_country']
            }
            writer.writerow(shipping_data)
    

def logic():

        pass
    # # Create array of all line items. 
    # for (i=0;i<max(line);++)
    # {
    #     customerlines[] = array (line[0],line[1]);
    # }


    # # Write into file from array.

    # for (j=0;j<size(customerlines);j++)
    # {
    #      writer = csv.DictWriter(customerlines[], fieldnames=fieldnames)
    # }pass
   

    # Check if the file exists to determine if we need to write headers


