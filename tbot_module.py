import telebot

class TBot:
    def __init__(self):
        class cmd_helper:
            def __init__(self,description,handler,scope):
                self.description=description
                self.handler = handler
                self.scope = scope
                pass
        self.__cmds={}
        self.__cmds['status'] = cmd_helper("стан системи",self.__cmd_status,['menu'])
        self.__cmds['help'] = cmd_helper("допомога", self.__cmd_help, ['menu'])
        pass
    def __cmd_status(self,message):
        print(message)
        self.__tbot.reply_to(message.chat.id, '__cmd_status')
        pass
    def __cmd_help(self,message):
        help="доступні команди"
        for cmd,data in self.__cmds.items():
            help+=f"\n/{cmd} {data.description}"
            pass
        self.__tbot.reply_to(message, help)
        pass
    def __handle_messages(self,messages):
        for message in messages:
            print(message)
            self.__tbot.reply_to(message, 'Hi')
            pass
        pass

    def __message_handler(self,message):
        print(message)
        self.__tbot.reply_to(message.chat.id, 'Hi')
        pass
    def start(self,token):
        self.__tbot=telebot.TeleBot(token)
        self.__tbot.delete_my_commands()
        menu_commands=[]
        for cmd,data in self.__cmds.items():
            if 'menu' in data.scope:
                menu_commands.append(telebot.types.BotCommand(cmd,data.description))
                pass
            self.__tbot.register_message_handler(data.handler, commands=[cmd])
            pass
        self.__tbot.set_my_commands(
            commands=menu_commands,
        )

        #self.__tbot.set_update_listener(self.__handle_messages)
        pass

    def run(self):
        self.__tbot.infinity_polling()
        pass
    pass





if __name__ == "__main__":
    import sys
    tbot=TBot()
    tbot.start(sys.argv[1])
    tbot.run()