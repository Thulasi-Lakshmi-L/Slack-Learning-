import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

try:
    response = client.chat_postMessage(
        channel="#academy-bot",
        text="Hello from Thulasi"
    )

    print("Message sent successfully!")

except SlackApiError as e:
    print(f"Slack error: {e.response['error']}")