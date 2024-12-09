import os
import requests
from atproto import Client
from atproto import models as api_models

def format_author_hashtag(author):
    # Remove spaces and special characters from author name
    return ''.join(c for c in author.replace(' ', '') if c.isalnum())

def create_hashtag_facets(text):
    facets = []
    words = text.split()
    current_position = 0
    
    for word in words:
        word_start = text.find(word, current_position)
        word_end = word_start + len(word)
        current_position = word_end
        
        if word.startswith('#'):
            # Remove the # for the tag value
            tag = word[1:]
            facets.append(api_models.AppBskyRichtextFacet.Main(
                index=api_models.AppBskyRichtextFacet.ByteSlice(
                    byteStart=word_start,
                    byteEnd=word_end
                ),
                features=[api_models.AppBskyRichtextFacet.Tag(
                    tag=tag
                )]
            ))
    
    return facets

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
        
        # Create author hashtag
        author_hashtag = format_author_hashtag(quote_author)
        
        # Format post with quote, author, and hashtags
        post_text = f'"{quote_text}"\n\n- {quote_author}\n\n#philosophy #stoic #{author_hashtag} #wisdom #dailystoic'
        
        # Create facets for hashtags
        facets = create_hashtag_facets(post_text)
        
        # Create and send post with facets
        post = client.send_post(
            text=post_text,
            facets=facets
        )
        client.like(post.uri, post.cid)
        print("Successfully posted quote!")
    else:
        print('Failed to retrieve quote.')

if __name__ == '__main__':
    main()