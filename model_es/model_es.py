import requests
import json


def send_json_to_es(json_obj):
    url = "http://localhost:9200/instagram/_doc/"

    payload = json.dumps(json_obj)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
