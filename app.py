import json
import os
import sys
from io import BytesIO
import webbrowser

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
data_file =  open('tunnels.json', 'r')
try:
    datajson = json.load(data_file)
    for i in datajson['tunnels']:
        FORWARDING_URL = i['public_url']
finally:
    data_file.close()

token_file =  open('api_token.json', 'r')
try:
    datajson = json.load(token_file)
    for i in datajson['api_token']:
        API_TOKEN = i['token']
finally:
    token_file.close()

WEBHOOK_URL = FORWARDING_URL + '/hook'
app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
        bot,
        FORWARDING_URL,
        states=[
            'user',
            'state1',
            'state2',
            'state3'
            ],
        transitions=[
            {
                'trigger': 'advance',
                'source': 'user',
                'dest': 'state1',
                'conditions': 'is_going_to_state1'
            },
            {
                'trigger': 'advance',
                'source': 'state1',
                'dest': 'user',
                'conditions': 'is_leaving_state1'
            },
            {
                'trigger': 'advance',
                'source': 'user',
                'dest': 'state2',
                'conditions': 'is_going_to_state2'
            },
            {
                'trigger': 'advance',
                'source': 'state2',
                'dest': 'user',
                'conditions': 'is_leaving_state2'
            },
            {
                'trigger': 'advance',
                'source': 'user',
                'dest': 'state3',
                'conditions': 'is_going_to_state3'
            },
            {
                'trigger': 'advance',
                'source': 'state3',
                'dest': 'user',
                'conditions': 'is_leaving_state3'
            }
        ],
        initial='user',
        auto_transitions=False,
        show_conditions=True,
        )

def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    webbrowser.open(FORWARDING_URL + '/show-fsm')
    app.run()
