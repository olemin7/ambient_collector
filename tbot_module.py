import telebot
from typing import Callable,Optional

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
        self.__cmds['subscribe'] = cmd_helper("підписатись на оновлення", self.__cmd_subscribe, [])
        self.__cmds['unsubscribe'] = cmd_helper("відписатись", self.__cmd_unsubscribe, [])
        self.__status_cb=None
        self.__config_updated_cb = None
        self.__subscribers=set()
        pass
    def __cmd_status(self,message):
        status=""
        if message.from_user.id in self.__subscribers:
            status += "підписані"
            pass
        else:
            status += "не підписані"
            pass
        status += "\n"
        if self.__status_cb:
            status+=self.__status_cb()
            pass
        else:
            status += "__status_cb is not set"
            pass
        self.__tbot.send_message(message.chat.id, status)
        pass
    def __cmd_help(self,message):
        help="доступні команди:"
        for cmd,data in self.__cmds.items():
            help+=f"\n/{cmd} {data.description}"
            pass
        self.__tbot.send_message(message.chat.id, help)
        pass
    def __cmd_subscribe(self,message):
        if message.from_user.id not in self.__subscribers:
            self.__subscribers.add(message.from_user.id)
            self.__tbot.send_message(message.from_user.id, "підписані")
            self.__config_update()
            pass
        else:
            self.__tbot.send_message(message.from_user.id, "вже підписані")
            pass
        pass
    def __cmd_unsubscribe(self,message):
        if message.from_user.id in self.__subscribers:
            self.__subscribers.remove(message.from_user.id)
            self.__tbot.send_message(message.from_user.id, "відписались")
            self.__config_update()
            pass
        else:
            self.__tbot.send_message(message.from_user.id, "не були підписані")
            pass
        pass
    def __config_update(self):
        if self.__config_updated_cb:
            self.__config_updated_cb(self.__subscribers)
            pass
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
        pass
    def send_notice(self,notice:str):
        for id in self.__subscribers:
            self.__tbot.send_message(id, notice)
            pass
        pass

    def set_status_cb(self,cb:Callable):
        self.__status_cb=cb
        pass

    def set_config_updated(self,cb:Callable):
        self.__config_updated_cb=cb
        pass

    def run(self):
        self.__tbot.infinity_polling()
        pass
    pass



if __name__ == "__main__":
    import sys
    tbot=TBot()
    tbot.start(sys.argv[1])
    @tbot.set_status_cb
    def cbfund():
        return "sdfsdfsdf"

    tbot.run()