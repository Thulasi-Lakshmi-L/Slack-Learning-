import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

token = os.environ.get("SLACK_BOT_TOKEN")
if not token:
    raise ValueError("Please configure SLACK_BOT_TOKEN")

client = WebClient(token=token)

CHANNEL_ID = "C0CMCEN83GS"  # Replace with your #general Channel ID
CSV_FILE_PATH = "channel_inventory.csv"  # Replace with your Lab 2.1 CSV filename

def upload_channel_report(channel_id, file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find {file_path} in the current directory.")

    try:
        response = client.files_upload_v2(
            channel=channel_id,
            file=file_path,
            title="Public Channel Inventory Report",
            initial_comment="📄 Here is the exported public channel inventory CSV from Lab 2.1.",
        )
        if response["ok"]:
            print(f"Successfully uploaded '{file_path}' to channel {channel_id}!")
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")

if __name__ == "__main__":
    upload_channel_report(CHANNEL_ID, CSV_FILE_PATH)