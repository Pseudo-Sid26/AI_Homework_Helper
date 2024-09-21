#smtp.py

import requests

def send_notification_to_parent(question):
    api_key = '23ce8585d363908659b4626b055ea9af-7a3af442-6461d556'
    domain = 'gmail.com'
    url = f'https://api.mailgun.net/v3/{domain}/messages'
    response = requests.post(
        url,
        auth=('api', api_key),
        data={
            'from': 'siddhesh26pseudo@gmail.com',
            'to': 'siddhesh.22210162@viit.ac.in',
            'subject': 'Homework Question Alert',
            'text': f"A new homework question was asked: {question}"
        }
    )
    if response.status_code == 200:
        print('Email sent successfully.')
    else:
        print(f"Error sending email: {response.text}")
