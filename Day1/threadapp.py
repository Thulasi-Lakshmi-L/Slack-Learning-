import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say, client):

    user_id = event["user"]

    # Fetch the user's real name from Slack
    response = client.users_info(user=user_id)
    real_name = response["user"]["real_name"]

    # Reply in the message thread
    say(
        text=f"Hello {real_name}! I am AcademyBot. How can I help you? 😊",
        thread_ts=event.get("thread_ts") or event["ts"],
        channel=event["channel"]
    )

if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    )
    handler.start()