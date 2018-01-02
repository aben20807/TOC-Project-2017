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

    def is_staying_state1(self, update):
        text = update.message.text
        return text.lower() == 'stay state1'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def is_staying_state2(self, update):
        text = update.message.text
        return text.lower() == 'stay state2'

    def on_enter_state1(self, update):
        self.bot.sendMessage(update.message.chat_id, 'Hello, ' + str(update.message.from_user.first_name))
        update.message.reply_text("I'm entering state1: Photo mode~~~")
        chat_id = update.message.chat.id
        # user = update.message.from_user
        # print('You talk with user {} and his user ID: {} '.format(user['first_name'], user['id']))
        self.bot.send_photo(chat_id = chat_id, photo = 'https://imgur.com/VkcGVCj.jpg')
        # self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')
