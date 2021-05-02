from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('rICc2cLl8No5EvDmFzgE4KJ0a6RKYtKwiL3Uxdb4nrOUB0EoxQjvYV49/koccNKu98txJBs73tf8r2zwHcAyJdfgNs1YuRlq6lJCPT2zDOl+bd6NWOjIxh1O25hDNSwWpHQ/wNT4FJBCV68CmGsSNwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f80a0306848c0fd11b9a44baec6839d7')

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()