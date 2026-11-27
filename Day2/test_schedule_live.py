import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

token = os.environ.get("SLACK_BOT_TOKEN")
if not token:
    raise ValueError("Please configure SLACK_BOT_TOKEN")

client = WebClient(token=token)
CHANNEL_ID = "C0CMCEN83GS"  # Replace with your Channel ID

# Schedule 2 minutes (120 seconds) from now
post_at_timestamp = int(time.time()) + 120

try:
    res = client.chat_scheduleMessage(
        channel=CHANNEL_ID,
        text="⏰ *Live Test!* This scheduled reminder just arrived in Slack.",
        post_at=post_at_timestamp,
    )
    print(f"Scheduled! ID: {res['scheduled_message_id']}")
    print("Wait 2 minutes and watch your Slack channel...Reminder Message")
except SlackApiError as e:
    print(f"Slack API Error: {e.response['error']}")