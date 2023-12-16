from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

line_bot_api = LineBotApi('iorom1rpMZiOzur1CHpeMA3o6M/1FgxgK/x0Bwjc3X7Ut0sApgfB8ISMZV8Q+8Nufu+d3JGy+Kg9Gf4f1tk7uKD/wkU9aFjBjftNb9aLA/jn9T/QWgFZ4JTUkhv0GvKlQqIOGDEcFsuMtMaRWbKEAQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9a59bb9a909e1603b000de04483c03e0')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)