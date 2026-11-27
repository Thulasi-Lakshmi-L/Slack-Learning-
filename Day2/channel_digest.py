import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialize client
token = os.environ.get("SLACK_BOT_TOKEN")
if not token:
    raise ValueError("Please configure SLACK_BOT_TOKEN")

client = WebClient(token=token)

# Replace with your actual Channel ID (starts with 'C')
CHANNEL_ID = "C0CMCEN83GS"


def generate_channel_digest(channel_id):
    # Calculate Unix timestamp for 24 hours ago
    twenty_four_hours_ago = time.time() - (24 * 60 * 60)
    user_counts = {}

    try:
        # 1. Fetch messages from the last 24 hours with pagination
        cursor = None
        while True:
            response = client.conversations_history(
                channel=channel_id,
                oldest=str(twenty_four_hours_ago),
                limit=200,
                cursor=cursor,
            )

            messages = response.get("messages", [])
            for msg in messages:
                # 2. Exclude bot messages and system subtypes
                if "bot_id" in msg or msg.get("subtype") is not None:
                    continue

                user_id = msg.get("user")
                if user_id:
                    user_counts[user_id] = user_counts.get(user_id, 0) + 1

            cursor = response.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break

        # 3. Format the summary using mrkdwn
        if not user_counts:
            summary_lines = [
                "*Daily Channel Digest (Last 24 Hours)*",
                "No human messages were posted in the last 24 hours.",
            ]
        else:
            summary_lines = ["*Daily Channel Digest (Last 24 Hours)*"]
            # Sort users by highest message count first
            for user_id, count in sorted(
                user_counts.items(), key=lambda x: x[1], reverse=True
            ):
                summary_lines.append(f"• <@{user_id}>: {count} message(s)")

        digest_text = "\n".join(summary_lines)

        # 4. Post a parent message first, then post the digest as a thread reply
        parent_msg = client.chat_postMessage(
            channel=channel_id,
            text="📊 *24-Hour Channel Activity Summary* (see thread for breakdown)",
        )
        parent_ts = parent_msg["ts"]

        client.chat_postMessage(
            channel=channel_id,
            thread_ts=parent_ts,
            text=digest_text,
        )

        print("Digest successfully posted as a thread reply!")
        print(digest_text)

    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")


if __name__ == "__main__":
    generate_channel_digest(CHANNEL_ID)