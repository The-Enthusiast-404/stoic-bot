import os
import requests
from atproto import Client, models

def main():
    # Check if environment variables are set
    username = os.getenv('BSKY_USERNAME')
    password = os.getenv('BSKY_PASSWORD')
    
    if not username or not password:
        raise ValueError("BSKY_USERNAME and BSKY_PASSWORD environment variables must be set")
    
    client = Client()
    profile = client.login(username, password)
    print('Welcome,', profile.display_name)
    
    response = requests.get('https://stoic-quotes.com/api/quote')
    if response.status_code == 200:
        data = response.json()
        quote_text = data['text']
        quote_author = data['author']
        post_text = f'"{quote_text}"\n\n- {quote_author}'
        
        # Create and send post
        post = client.send_post(text=post_text)
        client.like(post.uri, post.cid)
        print("Successfully posted quote!")
    else:
        print('Failed to retrieve quote.')

if __name__ == '__main__':
    main()