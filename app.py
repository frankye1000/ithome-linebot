# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage
app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi("WztvLgmxILTIj5n3au6FarxMrsD+fq31tGdIdEN3YQswISf3qWGoNFKwhRdYJ8Whq42RgrzjxV63j2KmLZfMvTG36aE5+i3aqkrCraRbODUsVBIgY/y3DMdcHLBmk+I3BDXFT8WXl8mYZQtrd5XD9gdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("98b983cc3bb1dffceacdaf29c0575474")

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


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


# 丟貼圖給ithome機器人的回應
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您好，\n歡迎使用iThome聊天機器人"))


# 丟訊息給ithome機器人的回應
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您好，\n歡迎使用iThome聊天機器人"))


# 追蹤ithome機器人的回應
@handler.add(FollowEvent)
def handle_follow_event(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您好，歡迎使用iThome聊天機器人"))
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text="輸入任意貼圖，獲取最新的iThome資訊"))
    line_bot_api.push_message(event.source.user_id, StickerSendMessage(package_id='11537', sticker_id='52002735'))



if __name__ == "__main__":
    # 要設定0.0.0.0 heroku 才會對外
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)