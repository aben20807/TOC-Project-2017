from transitions.extensions import GraphMachine
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
res = requests.get("http://course-query.acad.ncku.edu.tw/qry/qry002.php?syear=0106&sem=2&college_no=C&dept_no=A9&clweek=0&co_name=&lang=zh_tw")
soup = BeautifulSoup(res.content, "html.parser")

class TocMachine(GraphMachine):
    def __init__(self, bot, forwarding_url, **machine_configs):
        self.is_class = False
        self.bot = bot
        self.forwarding_url = forwarding_url
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        return text.lower() == 'go to state1'

    def is_leaving_state1(self, update):
        text = update.message.text
        update.message.reply_text("OuO")
        return text.lower() == 'give me fsm'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def is_leaving_state2(self, update):
        text = update.message.text
        update.message.reply_text(text)
        return text.lower() == 'go back'

    def is_going_to_state3(self, update):
        text = update.message.text
        return text.lower() == 'go to state3'

    def is_leaving_state3(self, update):
        text = update.message.text
        tts = gTTS(text=text, lang='en')
        tts.save("audio/{}.mp3".format(text))
        chat_id = update.message.chat.id
        self.bot.send_audio(chat_id=chat_id, audio=open('audio/{}.mp3'.format(text), 'rb'))
        return text.lower() == 'go back'

    def is_going_to_state4(self, update):
        text = update.message.text
        return text.lower() == 'go to state4'

    def is_leaving_state4(self, update):
        text = update.message.text
        count = 0
        for eachSoup in soup.select('td'):
            tmp = eachSoup.text.strip()
            if tmp == text:
                self.is_class = True
            if tmp.startswith('[') and self.is_class:
                self.is_class = False
                update.message.reply_text(tmp)
                count = count + 1
            if count > 10:
                update.message.reply_text("too many QuQ")
                break;
        return text.lower() == 'go back'

    def on_enter_state1(self, update):
        self.bot.sendMessage(update.message.chat_id, 'Hello, ' + str(update.message.from_user.first_name))
        update.message.reply_text("I'm entering state1")
        chat_id = update.message.chat.id
        self.bot.send_photo(chat_id = chat_id, photo = 'https://avatars3.githubusercontent.com/u/14831545?s=460&v=4')

    def on_exit_state1(self, update):
        update.message.reply_text("Ok QuQ")
        update.message.reply_text(self.forwarding_url + '/show-fsm')
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        update.message.reply_text("I'm repeater!!!!")

    def on_exit_state2(self, update):
        update.message.reply_text("Ok QuQ")
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("I'm entering state3")
        update.message.reply_text("I'm speaker!!!!")

    def on_exit_state3(self, update):
        chat_id = update.message.chat.id
        self.bot.send_photo(chat_id = chat_id, photo = 'https://imgur.com/VkcGVCj.jpg')
        update.message.reply_text("Go back OuO")
        print('Leaving state3')

    def on_enter_state4(self, update):
        update.message.reply_text("I'm entering state4")
        update.message.reply_text("I can search A9 Schedule time in 106_2!!!!")

    def on_exit_state4(self, update):
        update.message.reply_text("Ok QuQ")
        print('Leaving state4')
