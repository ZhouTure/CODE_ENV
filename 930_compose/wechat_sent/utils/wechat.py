import json
import requests

def wechat_sent(data):
    url = "your_url"
    headers= {'Content-Type':'application/json'}
    response = requests.post(url,   
                             headers=headers,
                             data=json.dumps(data))
    if response.status_code == 200:
        print('Sent succesd!')
        return None
    else:
        print(f"Error getting access token: {response.status_code}, {response.text}")
        return None
