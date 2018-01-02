from transitions.extensions import GraphMachine

class TocMachine(GraphMachine):
    def __init__(self, bot, forwarding_url, **machine_configs):
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
        update.message.reply_text("Ok QuQ")
        chat_id = update.message.chat.id
        self.bot.send_photo(chat_id = chat_id, photo = self.forwarding_url + '/show-fsm')
        return text.lower() == 'give me fsm'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def is_leaving_state2(self, update):
        text = update.message.text
        return text.lower() == 'go back'

    def on_enter_state1(self, update):
        self.bot.sendMessage(update.message.chat_id, 'Hello, ' + str(update.message.from_user.first_name))
        update.message.reply_text("I'm entering state1")
        chat_id = update.message.chat.id
        # user = update.message.from_user
        # print('You talk with user {} and his user ID: {} '.format(user['first_name'], user['id']))
        self.bot.send_photo(chat_id = chat_id, photo = 'https://imgur.com/VkcGVCj.jpg')

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')
