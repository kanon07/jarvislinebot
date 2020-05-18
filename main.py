from flask import Flask, request, abort
import paho.mqtt.publish as publish
import os
import json

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

# line api
    YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
    YOUR_CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']

# beebotte
    YOUR_BEEBOTTE_TOKEN = os.environ['YOUR_BEEBOTTE_TOKEN']

    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#act message
    on_msg = [s.encode('utf-8') for s in ['on', 'エアコンつけて！']]
    off_msg = [s.encode('utf-8') for s in ['off', 'エアコン切って！']]

#line notiv
    def broadcast_line_msg(msg):
        line_bot_api.broadcast(TextSendMessage(text=msg))

#mqtt republish
        def publish_aircon_control_msg(msg):
            publish.single('JARVIS/sakuravpn', \
                    msg, \
                    hostname='mqtt.beebotte.com', \
                    port=8883, \
                    auth = {'username':'token:{}'.format(YOUR_BEEBOTTE_TOKEN)}, \
                    tls={'ca_certs':'mqtt.beebotte.com.pem'})

            @app.route('/callback', methods=['POST'])
            def callback():
# get X-Line-Signature header value
                signature = request.headers['X-Line-Signature']

# get request body as text
body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

# handle webhook body
    try:
handler.handle(body, signature)
    except InvalidSignatureError:
abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        msg = event.message.text.encode('utf-8')

        if msg in on_msg:
        publish_aircon_control_msg('on')
        elif msg in off_msg:
        publish_aircon_control_msg('off')
        else:
        broadcast_line_msg('\n'.join(['エアコンをつけたい時：', \
                    *['['+s.decode('utf-8')+']' for s in on_msg], \
                    '\nエアコンを消したい時：', \
                    *['['+s.decode('utf-8')+']' for s in off_msg] , \
                    '\nって話しかけてね！']))

        if __name__ == '__main__':
        port = int(os.getenv('PORT'))
        app.run(host='0.0.0.0', port=port)
        )
        )
        )
