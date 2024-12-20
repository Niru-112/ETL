import smtplib
from email.mime.multipart import MIMEMultipart
from  email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime

def get_recent_files(directory):
    try:
        # List all files in the directory
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Find the most recent account file and error file
        account_files = [f for f in files if "account_" in os.path.basename(f) and "err" not in os.path.basename(f)]
        error_files = [f for f in files if "err" in os.path.basename(f)]
        
        # Sort by modification time (most recent first)
        account_files.sort(key=os.path.getmtime, reverse=True)
        error_files.sort(key=os.path.getmtime, reverse=True)
        
        # Return the most recent files if they exist
        recent_account_file = account_files[0] if account_files else None
        recent_error_file = error_files[0] if error_files else None
        
        return [recent_account_file, recent_error_file]
    
    except Exception as e:
        print(f"Error fetching recent files: {e}") 
        return []


timestamp = datetime.now().strftime("%Y-%m-%d") 
Subject = f"Account Report for Review {timestamp}"
body = "Check this file!!"
sender_email = "ABC@gmail.com"
receiver_email = "ABC@gmail.com"
sender_password = 'password'
smtp_server ='smtp.gmail.com'
smtp_port = 465

directory_path = r"D:\\ETL"

# Fetch the recent account and error files
files_to_send = get_recent_files(directory_path)

# Check if the required files were found
if not files_to_send or not any(files_to_send):
    print("Required files not found to send.")
else:
    # Prepare email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = Subject
    body_part = MIMEText(body, 'plain')
    message.attach(body_part)

    # Attach files to the email
    for filepath in files_to_send:
        if filepath:  # Ensure the file exists
            try:
                with open(filepath, 'rb') as file:
                    file_name = os.path.basename(filepath)
                    message.attach(MIMEApplication(file.read(), Name=file_name))
            except Exception as e:
                print(f"Error attaching file {filepath}: {e}")

    # Send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email Sent Successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")