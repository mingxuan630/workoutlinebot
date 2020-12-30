from flask import Flask, request, abort, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('brKzXBCBw/ea/SSFHGCPu2EApToFk/zPax3NE+A/BEzya+bnXybTXsv4ETyJj+Y75TuiINkcDkIm23Mmul3FX755Hi7/qwKMtcKIsoAH9wLV3m8WLHqXaytI3gMdp+Ql2SGWQ+BcOizilImoI86FLgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('424c7051953ceb9a1ee6e3ed9d42e813')

@app.route("/", methods=['GET'])
def index():
    return jsonify(),200

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print(request.headers['X-Line-Signature'])
    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    
    sticker_message = StickerSendMessage(
        package_id = "11537",
        sticker_id = "52002748"    
    )   
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message
    )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # reply_txt = "請輸入所在位置:"
    image_message = ImageSendMessage(
        original_content_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/440px-Image_created_with_a_mobile_phone.png',
        preview_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/440px-Image_created_with_a_mobile_phone.png'
    )
    line_bot_api.reply_message(
        event.reply_token,
        image_message
    )

def validate_address(text):
    # validate text include major cities' name
    # 1. thrid party lib read .json
    # 2. read city name and append into array
    # 3. write validation logic
    return True


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if(event.message.text == "搜餐廳"):
        reply_txt = f"請輸入所在位置:"
        obj = TextMessage(text=reply_txt)
    elif(validate_address(event.message.text)):
        obj = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/440px-Image_created_with_a_mobile_phone.png',
            title='減肥瘦身餐',
            text='少油少鹽',
            actions=[
                PostbackAction(
                    label='postback',
                    display_text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='message text'
                ),
                URIAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
        )
    else:
        reply_txt = f"{event.message.text} 輸入有誤，請重新輸入"
        obj = TextMessage(text=reply_txt)
    line_bot_api.reply_message(
        event.reply_token,
        obj
    )



@handler.add(MessageEvent, message=ButtonsTemplate)
def buttons_template_message(event):
    buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/440px-Image_created_with_a_mobile_phone.png',
        title='減肥瘦身餐',
        text='少油少鹽',
        actions=[
            PostbackAction(
                label='postback',
                display_text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageAction(
                label='message',
                text='message text'
            ),
            URIAction(
                label='uri',
                uri='http://example.com/'
            )
        ]
    )
    )
    line_bot_api.reply_message(
        event.reply_token,
        buttons_template_message
    )   





if __name__ == "__main__":
    app.run()