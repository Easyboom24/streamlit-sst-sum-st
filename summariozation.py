import requests
import json

def summarization(text):
    url = "https://api.aicloud.sbercloud.ru/public/v2/summarizator/predict"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        'instances': [
            {
                'text': text
            }
        ]
    }

    response = requests.post(url,headers=headers,data=json.dumps(data))
    return json.loads(response.text)