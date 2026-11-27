
import os
import csv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 1. Connect to Slack
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

if not SLACK_BOT_TOKEN:
    raise ValueError("Please configure SLACK_BOT_TOKEN")

client = WebClient(token=SLACK_BOT_TOKEN)


# 2. Retrieve all public channels using pagination
def get_public_channels():

    channels_data = []
    cursor = None

    while True:

        response = client.conversations_list(
            types="public_channel",
            limit=200,
            cursor=cursor
        )

        channels = response["channels"]

        # 3. Extract channel information
        for channel in channels:

            channel_info = {
                "channel_name": channel["name"],
                "member_count": channel.get("num_members", 0),
                "purpose": channel.get("purpose", {}).get("value", "")
            }

            channels_data.append(channel_info)

        # 4. Check whether another page exists
        cursor = response.get("response_metadata", {}).get(
            "next_cursor"
        )

        if not cursor:
            break

    return channels_data


# 5. Export the information to CSV
def export_to_csv(channels):

    filename = "channel_inventory.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "channel_name",
            "member_count",
            "purpose"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(channels)

    print(f"\nCSV exported successfully: {filename}")


# 6. Main program
if __name__ == "__main__":

    try:

        print("Fetching public channels...\n")

        channels = get_public_channels()

        for channel in channels:

            print(f"Channel: {channel['channel_name']}")
            print(f"Members: {channel['member_count']}")
            print(f"Purpose: {channel['purpose']}")
            print("-" * 40)

        print(f"\nTotal public channels found: {len(channels)}")

        export_to_csv(channels)

    except SlackApiError as error:

        print("Slack API Error:", error.response["error"])

