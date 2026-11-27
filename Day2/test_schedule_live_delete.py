import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

token = os.environ.get("SLACK_BOT_TOKEN")
if not token:
    raise ValueError("Please configure SLACK_BOT_TOKEN")

client = WebClient(token=token)
CHANNEL_ID = "C0CMCEN83GS"  # Replace with your #general Channel ID

# 1. Schedule the message 2 minutes (120 seconds) from now
post_at_timestamp = int(time.time()) + 120
message_text = "⏰ *Live Test!* This scheduled reminder just arrived in Slack."

try:
    res = client.chat_scheduleMessage(
        channel=CHANNEL_ID,
        text=message_text,
        post_at=post_at_timestamp,
    )
    print(f"1. Scheduled! ID: {res['scheduled_message_id']}")
    print("Waiting 2 minutes for Slack to post the message...")

    # 2. Wait 120 seconds, then poll for up to 30 seconds until the message appears
    time.sleep(120)
    live_ts = None

    for _ in range(6):
        history = client.conversations_history(
            channel=CHANNEL_ID,
            oldest=str(post_at_timestamp - 10),
            limit=5,
        )
        for msg in history.get("messages", []):
            if "bot_id" in msg and "Live Test!" in msg.get("text", ""):
                live_ts = msg["ts"]
                break
        if live_ts:
            break
        time.sleep(5)

    if not live_ts:
        print("Could not find the posted message in channel history.")
    else:
        print(f"2. Message is live in Slack (ts={live_ts}). Waiting 10 minutes to delete...")

        # 3. Wait 10 minutes (600 seconds)
        time.sleep(600)

        # 4. Delete the live message from the channel
        client.chat_delete(channel=CHANNEL_ID, ts=live_ts)
        print("3. Deleted the live message from Slack!")

except SlackApiError as e:
    print(f"Slack API Error: {e.response['error']}")