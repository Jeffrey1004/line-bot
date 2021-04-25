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

line_bot_api = LineBotApi('29Au07MDPuqy7Z21tWpty934jHDtOUz/zXSw+ILAQ1G3Xr8D1S1gAZwJd15eUzUMaiR3bn3SzFBZG3lNJ8BzmKVl7/UUvaFp5md7Q0qykyI3SXQhYt0QAe7c8Vc7VUMI7r4nXEe+bsv9QK+B/s94pgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5cfa7a3c486870f3863fea16d1d2c596')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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
