import os
from datetime import datetime, timedelta, timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize client
token = os.environ.get("SLACK_BOT_TOKEN")
if not token:
    raise ValueError("Please configure SLACK_BOT_TOKEN")

client = WebClient(token=token)

# Replace with your actual Channel ID from Lab 2.1 / 2.2
CHANNEL_ID = "C0CMCEN83GS"


def manage_scheduled_reminder(channel_id):
    # 1. Calculate 9:30 AM IST (UTC+5:30) for tomorrow
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)
    tomorrow_930_ist = (now_ist + timedelta(days=1)).replace(
        hour=9, minute=30, second=0, microsecond=0
    )
    post_at_timestamp = int(tomorrow_930_ist.timestamp())

    try:
        # Step 1: Schedule the stand-up reminder
        schedule_res = client.chat_scheduleMessage(
            channel=channel_id,
            text="⏰ *Daily Stand-up Reminder!* Please share your updates for today.",
            post_at=post_at_timestamp,
        )
        scheduled_id = schedule_res["scheduled_message_id"]
        print(f"1. SCHEDULED: ID = {scheduled_id} | Time = {tomorrow_930_ist.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # Step 2: List pending scheduled messages
        list_res = client.chat_scheduledMessages_list(channel=channel_id)
        scheduled_messages = list_res.get("scheduled_messages", [])
        print(f"2. LISTED: Found {len(scheduled_messages)} pending scheduled message(s):")
        for msg in scheduled_messages:
            print(f"   - ID: {msg['id']} | Post At: {msg['post_at']} | Text: {msg['text']}")

        # Step 3: Delete the scheduled message
        delete_res = client.chat_deleteScheduledMessage(
            channel=channel_id,
            scheduled_message_id=scheduled_id,
        )
        if delete_res["ok"]:
            print(f"3. DELETED: Successfully canceled scheduled message {scheduled_id}.")

    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")


if __name__ == "__main__":
    manage_scheduled_reminder(CHANNEL_ID)