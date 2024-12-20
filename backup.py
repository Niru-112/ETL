import shutil
import os
from datetime import datetime

# Backup function
def backup_file(source_file, backup_dir, backup_name):
    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Construct backup file path
    backup_file_path = os.path.join(backup_dir, backup_name)
    
    # Copy file
    shutil.copy(source_file, backup_file_path)
    print(f'Backup created: {backup_file_path}')
    
    # Read and print file content
    with open(source_file, mode='r') as file:
        for line in file:
            print(line.strip())

# Paths for account.py
account_source = r'D:\ETL\account.py'
account_backup_dir = r'D:\ETL\backup'
backup_file_name = 'Account.py'
backup_file_path = os.path.join(account_backup_dir, backup_file_name)

# Backup for account.py
backup_file(account_source, account_backup_dir, backup_file_name)

# Paths for customer.py
customer_source = r'D:\ETL\customer.py'
customer_backup_dir = r'D:\ETL\backup'
backup_file_name = 'Customer.py'

# Backup for customer.py
backup_file(customer_source, customer_backup_dir, backup_file_name)

# Paths for address.py
address_source = r'D:\ETL\address.py'
address_backup_dir = r'D:\ETL\backup'
backup_file_name = 'Address.py'

# Backup for address.py
backup_file(address_source, address_backup_dir, backup_file_name)

address_source = r'D:\ETL\attribute.py'
address_backup_dir = r'D:\ETL\backup'
backup_file_name = 'Attribute.py'

# Backup for address.py
backup_file(address_source, address_backup_dir, backup_file_name)
