from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import io
import datetime
from main import insert_to_database

# Authenticate and create the service
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None

# Check if token.pickle exists
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If no valid credentials, perform login flow
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Save credentials for future use
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Build the Drive API service
service = build('drive', 'v3', credentials=creds)

# Example: List files in Drive
results = service.files().list(pageSize=10).execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(f"{item['name']} ({item['id']})")
        
def upload_file(file_name, file_path, mime_type):    
    file_metadata = {'name': file_name}  # Set the file name in Drive
    media = MediaFileUpload(file_path, mimetype=mime_type)
    try:
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()  # Execute the API call
        print(f"{file_name} uploaded successfully. File ID: {file['id']}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Function to find a file ID by name
def get_file_id(service, file_name):
    try:
        results = service.files().list(q=f"name='{file_name}'", fields="files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print(f"No file found with name: {file_name}")
            return None
        print(f"File ID for {file_name}: {items[0]['id']}")
        return items[0]['id']
    except Exception as e:
        print(f"Error getting file ID: {e}")
        return None

# Function to download a file from Google Drive
def download_file(service, file_id, output_path):
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")
        
        with open(output_path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        print(f"File downloaded successfully to {output_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Function to delete a file from Google Drive
def delete_file(service, file_name):
    file_id = get_file_id(service, file_name)
    if not file_id:
        print(f"File with name {file_name} not found to delete.")
        return False
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"File '{file_name}' deleted successfully.")
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

# Main code workflow
# Function to upload a file to Google Drive
def main():
    # Step 1: Generate dynamic filename and output path
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format the current date and time
    file_name = f"account_{current_time}.csv"  # Dynamic filename
    output_path = os.path.join(r"D:\ETL", file_name)  # Dynamic output path based on the generated filename

    print(f"File name: {file_name}")
    print(f"Output path: {output_path}")

    # Step 2: Upload the file to Google Drive
    upload_file(file_name, output_path, 'text/csv')  # Upload file to Drive

    # Step 3: Download the file (Example)
    file_id = get_file_id(service, file_name)
    if file_id:
        download_file(service, file_id, output_path)
    
    # Step 4: Insert customer data into the database (Placeholder)
    # insert_to_database()  # Assuming this function handles the database insertion
    
    # Step 5: Delete the file from Google Drive
    delete_file(service, file_name)

# Run the main function
if __name__ == "__main__":
    insert_to_database()
    main()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# Function to upload multiple files
# def upload_multiple_files(file_list):
#     pass
#     for file_info in file_list:
#         file_name = file_info['file_name']
#         file_path = file_info['file_path']
#         mime_type = file_info['mime_type']
#         try:
#             upload_file(file_name, file_path, mime_type)
#         except Exception as e:
#             print(f"Failed to upload {file_name}: {e}")

# Example: List of files to upload
# files_to_upload = [
#     {'file_name': 'address.py', 'file_path': 'D:\ETL\address.py', 'mime_type': 'text/x-python'},
#     {'file_name': 'customer.py', 'file_path': 'D:\ETL\customer.py', 'mime_type': 'text/x-python'},
#     {'file_name': 'attribute.py', 'file_path': 'D:\ETL\attribute.py', 'mime_type': 'text/x-python'}
# ]
