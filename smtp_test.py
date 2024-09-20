import requests

def send_notification_to_parent(question):
    api_key = 'Mailgun API key'
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
