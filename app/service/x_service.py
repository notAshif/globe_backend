import requests
from requests_oauthlib import OAuth1

def post_to_x(content, api_key, api_secret, access_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    
    auth = OAuth1(
        api_key,
        api_secret,
        access_token,
        access_token_secret
    )
    
    payload = {"text": content}
    
    res = requests.post(url, json=payload, auth=auth)
    
    return res.json()