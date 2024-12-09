import os
import requests
from atproto import Client, client_utils


def main():
    client = Client()
    username = os.environ['BSKY_USERNAME']
    password = os.environ['BSKY_PASSWORD']
    profile = client.login(username, password)
    print('Welcome,', profile.display_name)

    response = requests.get('https://stoic-quotes.com/api/quote')
    if response.status_code == 200:
        data = response.json()
        quote_text = data['text']
        quote_author = data['author']
        post_text = f'"{quote_text}"\n\n- {quote_author}'

        text = client_utils.TextBuilder().text(post_text)
        post = client.send_post(text)
        client.like(post.uri, post.cid)
    else:
        print('Failed to retrieve quote.')


if __name__ == '__main__':
    main()
