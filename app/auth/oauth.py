

from flask import request, redirect, session
import requests
import meeting

secret_token = '3b0cUKa1RlWtYHXdWiBhWA'
CLIENT_ID = 'AMrRhGqPR4i6nVsgN_M0Q'
CLIENT_SECRET = '30tgBycYVLltvUkQ574cYnLZf4mPHt7e'
  
def oauth_callback(code, redirect_uri):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    res = requests.post('https://zoom.us/oauth/token', data=data, auth=(CLIENT_ID, CLIENT_SECRET))

    if res.status_code == 200:
        access_token = res.json()['access_token']
        # Save access_token to session or database as needed
        session['access_token'] = access_token
        # meeting.start_zoom_call(access_token)
        # print('access token in session storage', session.get('access_token'))
        return "Access token saved successfully."
    else:
        return "Failed to retrieve access token."
