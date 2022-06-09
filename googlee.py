import mimetypes
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import datetime


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
CLIENT_SECRET_FILE="client_secrets.json"
API_NAME="drive"
API_VERSION="v3"
SCOPES=['https://www.googleapis.com/auth/drive'] 
service=Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
#folder="majorproject"
#file_metadata={'name':folder,'mimeType':'application/vnd.google-apps.folder'}
#service.files().create(body=file_metadata).execute()
folder_id="1UIBZAO-VaU6pmNs3oNW0gGvUjg4Pnavs"
file_name="Original.txt"
mime_types="text/plain"
file_metadata={'name':file_name,'parents':[folder_id]}
media=MediaFileUpload('C:/Users/chandhan reddy/Downloads/major project/Original.txt',mimetype=mime_types)
service.files().create(body=file_metadata,media_body=media,fields='id').execute()


