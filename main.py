from account import generate_random_customers, create_or_append_account
from customer import create_customer
from address import create_address
from attribute import create_attribute_data
import sys
import io
from datetime import datetime


# Set default encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
filename = f'account_{timestamp}.csv'

with open(filename, mode='w') as file:
    file.write("customer_id, customer_name , billing_address1, billing_address2,billing_city, billing_state, billing_country,shipping_address1, shipping_address2, shipping_city,shipping_state, shipping_country,categories,sub_categories\n")  # Example header
    
num_customers =  5 #int(input("Enter The number of customers you want to print: "))
  
data = generate_random_customers(num_customers)
print(len(data))
# print( "Random Customers are generated!")

data2 = create_or_append_account(data,filename)
print(len(data2))
print(f"Accounts have been written to {filename}.")
# print("AccountCSV file written successfully.")

data3 = create_customer(filename)
print(len(data3))
# print("CustomerCSV file written successfully.")

data4= create_address(data)
print(data4)
# print("AddressCSV file written successfully.")

data5 = create_attribute_data(filename)
print(data5)













#It is used for library.py when all the functions are in one file
# import library

# def main():
#     # Generate random customers
#     data = library.generate_random_customers(100)

#     # Append to CSV
#     library.create_or_append_account(data)
#     print("Customers have been appended to the CSV file.")

#     #creating customer details
#     library.create_customer()
#     print("Customer Details Created")

#     #creating address details
#     library.create_address(data)
#     print("Address CSV Created!!")

# if __name__ == "__main__":
#     main()

#It is used when functions are separated!

