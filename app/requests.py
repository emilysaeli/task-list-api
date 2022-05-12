import requests
from flask import current_app
import os
import json
from dotenv import load_dotenv

load_dotenv()

def use_header(text):
    token = current_app.config["SLACK_API_TOKEN"]
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"channel": "task-notifications", "text": text}
    

    r = requests.post(slack_url, headers=headers, data=json.dumps(payload))
    return r.status_code

