# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('1xO55kBmJ8Yy4gkm7jqw2HAtRWns819B4iPo2m06Js2r5nz7OHjgsgkIV1EptZPGq42RgrzjxV63j2KmLZfMvTG36aE5+i3aqkrCraRbODVGqzvC8PQufzSiZ4frb8wopgd3UFJYNLokEnmQtx0kxAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3dea4e0320b8230a11258d1e23275572')

# 接收 LINE 的資訊
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

if __name__ == "__main__":
    app.run()