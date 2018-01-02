from transitions.extensions import GraphMachine

class TocMachine(GraphMachine):
    def __init__(self, bot, **machine_configs):
        self.bot = bot
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        return text.lower() == 'go to state1'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def on_enter_state1(self, update):
        update.message.reply_text("I'm entering state1")
        chat_id = update.message.chat.id
        self.bot.send_photo(chat_id = chat_id, photo = 'https://imgur.com/VkcGVCj.jpg')
        self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')
