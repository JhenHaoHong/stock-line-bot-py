# -*- coding: utf-8 -*-
import openai
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi('iorom1rpMZiOzur1CHpeMA3o6M/1FgxgK/x0Bwjc3X7Ut0sApgfB8ISMZV8Q+8Nufu+d3JGy+Kg9Gf4f1tk7uKD/wkU9aFjBjftNb9aLA/jn9T/QWgFZ4JTUkhv0GvKlQqIOGDEcFsuMtMaRWbKEAQdB04t89/1O/w1cDnyilFU=')
        handler = WebhookHandler('9a59bb9a909e1603b000de04483c03e0')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息

        ai_msg = msg[:6].lower()
        reply_msg = ''
        if ai_msg == 'hi ai:':
            openai.api_key = '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'
            response = openai.completions.create(
                model='text-davinci-003',
                prompt=msg[6:],
                max_tokens=256,
                temperature=0.5,
            )
            reply_msg = response["choices"][0]["text"].replace('\n','')
        else:
            reply_msg = msg
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)
    except Exception as error:
        print(error)
    return 'OK'

if __name__ == "__main__":
    app.run()

# from flask import Flask, request, abort
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import *
# import os

# app = Flask(__name__)

# line_bot_api = LineBotApi('iorom1rpMZiOzur1CHpeMA3o6M/1FgxgK/x0Bwjc3X7Ut0sApgfB8ISMZV8Q+8Nufu+d3JGy+Kg9Gf4f1tk7uKD/wkU9aFjBjftNb9aLA/jn9T/QWgFZ4JTUkhv0GvKlQqIOGDEcFsuMtMaRWbKEAQdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('9a59bb9a909e1603b000de04483c03e0')

# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = TextSendMessage(text=event.message.text)
#     line_bot_api.reply_message(event.reply_token, message)

# import os
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='127.0.0.1', port=port)