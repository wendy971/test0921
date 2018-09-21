# -*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('97ENE9L1ecJQLi5Vni12aP83Ue2O94tk01Kc0IEq5Qd3S0t6ji8o1kYd7/PiFvliNKyYI2J/b5vjFS7Mbx5KiP9AhYUcPcNUU3I0mESx0gfckatmQ83oeheTkp7QfP/7ofN2rpJTLXu/Zf8629q0xgdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('8937db21866c78dffb04a44e76d60227')

line_bot_api.push_message('U4b6918fbd070336e8382c598405ad217', TextSendMessage(text='哈囉你好嗎'))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得個人資料
    profile = line_bot_api.get_profile(event.source.user_id)
    nameid = profile.display_name
    uid = profile.user_id

    print('uid: '+uid)
    print('name:'+nameid)

    # 傳送圖片
    if event.message.text == '我要看超值推薦':
        message = ImageSendMessage(
            original_content_url='https://i.imgur.com/8g83GnI.jpg',
            preview_image_url='https://i.imgur.com/8g83GnI.jpg'
        )
    # 傳送影片
    elif event.message.text == '試試看影片':
        message = VideoSendMessage(
            original_content_url='https://i.imgur.com/g2aQYSZ.mp4',
            preview_image_url='https://i.imgur.com/g2aQYSZ.mp4'
        )
    # 傳送位置
    elif event.message.text == '公司位置':
        message = LocationSendMessage(
            title='公司地點',
            address='板橋',
            latitude=25.013132,
            longitude=121.4670082
        )
    # 傳送貼圖
    elif event.message.text == '給我一個貼圖':
        message = StickerSendMessage(
            package_id='1',
            sticker_id='2'
        )
    # 傳送組圖訊息
    elif event.message.text == '我要看報紙':
        message = ImagemapSendMessage(
            base_url='https://i.imgur.com/PjvwT6d.png',
            alt_text='Imagemap',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://tw.appledaily.com/',
                    area=ImagemapArea(
                        x=0, y=0, width=520, height=1040
                    )
                ),
                MessageImagemapAction(
                    text='您需要付費喔！',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=1040
                    )
                )
            ]
        )
    # 傳送確認介面訊息
    elif event.message.text == '我想要評分':
        message = TemplateSendMessage(
            alt_text='你覺得這個機器人方便嗎？',
            template=ConfirmTemplate(
                text='你覺得這個機器人方便嗎？',
                actions=[
                    MessageTemplateAction(
                        label='很棒',
                        text='ＧＯＯＤ'
                    ),
                    MessageTemplateAction(
                        label='非常棒!',
                        text='ＶＥＲＹ　ＧＯＯＤ'
                    )
                ]
            )
        )
        # 傳送按鈕介面訊息
    elif event.message.text == 'HAPPYGO':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/m1sFvq3.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='公司位置',
                        text='公司位置'
                    ),
                    MessageTemplateAction(
                        label='超值推薦',
                        text='我要看超值推薦'
                    ),
                    URITemplateAction(
                        label='HAPPY GO官方網站',
                        uri='https://www.happygocard.com.tw/#'
                    )
                ]
            )
        )
    # 傳送多重按鈕介面訊息
    elif event.message.text == '所有功能':
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/m1sFvq3.jpg',
                        title='HAPPYGO',
                        text='HAPPYGO',
                        actions=[
                            MessageTemplateAction(
                                label='公司位置',
                                text='公司位置'
                            ),
                            MessageTemplateAction(
                                label='超值推薦',
                                text='我要看超值推薦'
                            ),
                            URITemplateAction(
                                label='HAPPY GO官方網站',
                                uri='https://www.happygocard.com.tw/#'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/F8WHUU6.jpg',
                        title='其他功能',
                        text='這裡存放各種功能！',
                        actions=[
                            MessageTemplateAction(
                                label='為機器人評分',
                                text='我想要評分'
                            ),
                            MessageTemplateAction(
                                label='更多HAPPYGO消息',
                                text='HAPPYGO'
                            ),
                            MessageTemplateAction(
                                label='放鬆一下',
                                text='給我一個貼圖'
                            )
                        ]
                    )
                ]
            )
        )
    # 傳送多重圖片訊息
    elif event.message.text == '圖圖圖':
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/F8WHUU6.jpg',
                        action=PostbackTemplateAction(
                            label='做你的好伴',
                            text='快樂應援團',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/8g83GnI.jpg',
                        action=PostbackTemplateAction(
                            label='快樂多一點',
                            text='超值推薦',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        )
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)


if __name__ == '__main__':
    app.run(debug=True)
