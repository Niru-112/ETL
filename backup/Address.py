# Function to write address data to CSV
import csv
import os

def create_address(customers):
    filename = 'address.csv'

    # Check if the file exists
    file_exists = os.path.isfile(filename)

    # Open the file in append mode
    with open(filename, mode='a', newline='') as file:
        # Define the required fields
        fieldnames = ['customer_id', 'billing_type', 'address1', 'address2', 'city', 'state', 'country']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if the file does not exist
        if not file_exists:
            writer.writeheader()

        # Write both billing and shipping addresses for each customer
        for customer in customers:
            # Billing address entry
            billing_data = {
                'customer_id': customer['customer_id'],
                'billing_type': 'billing',
                'address1': customer.get('billing_address1', ''),
                'address2': customer.get('billing_address2', ''),
                'city': customer.get('billing_city', ''),
                'state': customer.get('billing_state', ''),
                'country': customer.get('billing_country', '')
            }
            writer.writerow(billing_data)

            # Shipping address entry
            shipping_data = {
                'customer_id': customer['customer_id'],
                'billing_type': 'shipping',
                'address1': customer.get('shipping_address1', ''),
                'address2': customer.get('shipping_address2', ''),
                'city': customer.get('shipping_city', ''),
                'state': customer.get('shipping_state', ''),
                'country': customer.get('shipping_country', '')
            }
            writer.writerow(shipping_data)

    return len(customers) * 2  # Returns total entries written to address.csv
