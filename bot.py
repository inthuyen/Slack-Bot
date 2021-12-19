import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

# Load from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configure your flask application
app = Flask(__name__)

# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

# Use WebClient in Slack
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# Get bot ID
BOT_ID = client.api_call("auth.test")['user_id']

# This 
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if BOT_ID != user_id:
        if "?" in text:
            # Connects the bot to the Slack channel
            client.chat_postMessage(channel=channel_id, text=text)

# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True)