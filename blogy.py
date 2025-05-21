import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '7630266776583232027'  # Your blog ID

def authenticate():
    creds = None
    token_path = 'token.pickle'

    # Load saved credentials
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, run the OAuth flow again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for next time
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('blogger', 'v3', credentials=creds)

def build_html():
    return "<h1>Automated Post</h1><p>This is a post created without logging in again!</p>"

def post_to_blogger(service, title, content, labels=None):
    post_body = {
        'kind': 'blogger#post',
        'title': title,
        'content': content,
    }
    if labels:
        post_body['labels'] = labels

    post = service.posts().insert(blogId=BLOG_ID, body=post_body).execute()
    print(f"✅ Post published! Title: {post['title']}, URL: {post['url']}")
    return post

def main():
    service = authenticate()
    title = "Repeat Auto Post"
    content = build_html()
    labels = ['Auto', 'Python', 'NoLogin']

    post_to_blogger(service, title, content, labels)

if __name__ == '__main__':
    main()
