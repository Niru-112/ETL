# account.py
import random
import os
import csv

# Sample data for generating random customers
sample_names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Davis"]
sample_streets = ["123 Elm St", "456 Oak St", "789 Pine St", "101 Maple St", "202 Birch St"]
sample_cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
sample_states = ["NY", "CA", "IL", "TX", "AZ"]
sample_countries = ["USA", "Canada", "UK", "Australia", "Germany"]
sample_categories = [" ", "Shirts","Shirts;Pants","Top;Jacket;Hoodies","Tops;Sweatshirts;Cargo"]
sample_sub_categories = ["All","Small","Medium","Large","Small;medium","small;medium;large"]

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
            'shipping_country': random.choice(sample_countries), # Random shipping country
            'categories': random.choice(sample_categories), #Random Categories
            'sub_categories': random.choice(sample_sub_categories) # Random Sub_categories
        }
        customers.append(customer)

    return customers

def create_or_append_account(customers):
    filename = 'account.csv'

    existing_entries = []

    file_exists = os.path.isfile(filename) #flag
        
    with open(filename, mode='r') as file:
            reader = csv.reader(file)
            existing_entries = list(reader)  # Read all existing entries
            # header = existing_entries[0]  # Assuming the first row is the header
            existing_entries = existing_entries[1:]  # Exclude the header

    # Combine existing entries with new customers
    combined_entries = existing_entries + customers

    with open(filename, mode='a', newline='') as file:
            fieldnames = ['customer_id', 'customer_name', 'billing_address1', 'billing_address2',
                      'billing_city', 'billing_state', 'billing_country',
                      'shipping_address1', 'shipping_address2', 'shipping_city',
                      'shipping_state', 'shipping_country','categories','sub_categories']
        
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader() 
            if not file_exists:
                writer.writeheader()

            for customer in customers:
                writer.writerow(customer)
    return combined_entries
    
