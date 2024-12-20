import smtplib
from email.mime.multipart import MIMEMultipart
from  email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S") 
Subject = f"Backup File upto {timestamp}"
body = "Check this file!!"
sender_email = "nirusanathara1012@gmail.com"
receiver_email = "nirusanathara1012@gmail.com"
sender_password = 'zvcr krio nmog erzq'
smtp_server ='smtp.gmail.com'
smtp_port = 465

filepath = r"D:\\ETL.zip"

# Fetch the recent account and error files

# Check if the required files were found

    # Prepare email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = Subject
body_part = MIMEText(body, 'plain')
message.attach(body_part)

with open(filepath, 'rb') as file:
    # file_name = os.path.basename(filepath)
    message.attach(MIMEApplication(file.read(), Name="D:\\ETL.zip"))

with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
print("Email Sent Successfully!")
