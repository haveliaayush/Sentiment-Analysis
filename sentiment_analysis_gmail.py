import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from textblob import TextBlob

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailClient:

    def __init__(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_message_sentiment(self,message):
        analysis = TextBlob(message)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_messages(self):
        messages = []
        results = self.service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
        temp_messages = results.get('messages',[])
        for temp_message in temp_messages:
            parsed_message = {}
            msg = self.service.users().messages().get(userId='me', id=temp_message['id']).execute()
            parsed_message['text'] = msg['snippet']
            parsed_message['sentiment'] = self.get_message_sentiment(msg['snippet'])
            messages.append(parsed_message)
        return messages
    
def main():
    api = GmailClient()
    messages = api.get_messages()
    pmessages = [message for message in messages if message['sentiment'] == 'positive']
    nmessages = [message for message in messages if message['sentiment'] == 'negative']
    print('Positive messages percentage: {} %'.format(100*len(pmessages)/len(messages)))
    print('Negative messages percentage: {} %'.format(100*len(nmessages)/len(messages)))
    print('Neutral messages percentage: {} %'.format(100*(len(messages) - len(pmessages) - len(nmessages))/len(messages)))
    
if __name__ == "__main__" :
    main()