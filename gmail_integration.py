import os
import base64
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

# If modifying the Gmail API scopes, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
REDIRECT_URI = 'http://localhost:8503'

# Function to authenticate and fetch the latest email
def fetch_email():
    creds = None
    # The token.pickle file stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # Build the Gmail API client
        service = build('gmail', 'v1', credentials=creds)

        # Get the first email from the inbox
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            return None

        # Fetch the latest email message
        message = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        msg_str = base64.urlsafe_b64decode(message['payload']['body']['data'].encode('ASCII')).decode('utf-8')

        # Return the email content
        return msg_str

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
