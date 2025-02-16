from typing import Callable, Optional
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
import requests
import logging

log = logging.getLogger('logger')


class TBot:
    def __init__(self):
        self.__cmds = {}
        self.__tbot = {}
        self.__config = {}
        self.add_command('start', [""], "стан системи", self.__cmd_start)
        self.add_command('status', ["menu"], "стан системи", self.__cmd_status)
        self.add_command('help', ["menu"], "допомога", self.__cmd_help)
        self.add_command('subscribe', [""], "підписатись на оновлення", self.__cmd_subscribe)
        self.add_command('unsubscribe', [""], "відписатись", self.__cmd_unsubscribe)
        self.__get_status_fn = None
        self.__config_updated_cb = None
        pass

    async def __cmd_status(self, message):
        status = ""
        if message.from_user.id in self.__config['subscribers']:
            status += "підписані"
            pass
        else:
            status += "не підписані"
            pass
        status += "\n"
        if self.__get_status_fn:
            status += self.__get_status_fn()
            pass
        else:
            status += "__status_cb is not set"
            pass
        await self.__tbot.send_message(message.chat.id, status)

    async def __cmd_help(self, message):
        help = "доступні команди:"
        for cmd, data in self.__cmds.items():
            help += f"\n/{cmd} {data['description']}"
            pass
        await  self.__tbot.send_message(message.chat.id, help)

    async def __cmd_start(self, message):
        await self.__cmd_status(message)
        await self.__cmd_help(message)

    async def __cmd_subscribe(self, message):
        if message.from_user.id not in self.__config['subscribers']:
            self.__config['subscribers'].add(message.from_user.id)
            await self.__tbot.send_message(message.from_user.id, "підписані")
            self.__config_update()
        else:
            await self.__tbot.send_message(message.from_user.id, "вже підписані")

    async def __cmd_unsubscribe(self, message):
        if message.from_user.id in self.__config['subscribers']:
            self.__config['subscribers'].remove(message.from_user.id)
            await self.__tbot.send_message(message.from_user.id, "відписались")
            self.__config_update()
        else:
            await self.__tbot.send_message(message.from_user.id, "не були підписані")

    def __config_update(self):
        log.debug(f'config_update={self.__config}')
        if self.__config_updated_cb:
            self.__config_updated_cb(self.__config)

    def is_enabled(self):
        return ("enable" in self.__config) and self.__config["enable"]

    async def start(self, config):
        log.info(f'config={config}')
        self.__config = config
        if not self.is_enabled():
            log.info("Disabled")
            return
        if not 'subscribers' in self.__config:
            self.__config['subscribers'] = set()

        self.__tbot = AsyncTeleBot(self.__config["token"])
        await self.__tbot.delete_my_commands()
        menu_commands = []
        for cmd, data in self.__cmds.items():
            if 'menu' in data['scope']:
                menu_commands.append(telebot.types.BotCommand(cmd, data['description']))
                pass
            self.__tbot.register_message_handler(data['handler'], commands=[cmd])
            pass
        await self.__tbot.set_my_commands(
            commands=menu_commands,
        )
        await self.send_notice("Запуск, використовуйте /help")
        await self.__tbot.polling(none_stop=True)

    async def send_notice(self, notice: str):
        if not self.is_enabled():
            log.info("Disabled")
            return
        log.debug(f'send_notice={notice}, subscribers={self.__config["subscribers"]}')
        for id in self.__config['subscribers']:
            await self.__tbot.send_message(id, notice)

    def set_get_status_fn(self, cb: Callable):
        self.__get_status_fn = cb

    def set_config_updated_cb(self, cb: Callable):
        self.__config_updated_cb = cb

    def add_command(self, cmd: str, scope, description: str, handler: Callable):
        self.__cmds[cmd] = {'description': description, 'handler': handler, 'scope': scope}


def tbot_send_https_notice(config: dict, text: str):
    if not config["enable"]:
        log.info("Disabled")
        return
    log.info(f"send notice={text}, to={config['subscribers']}")
    url = f"https://api.telegram.org/bot{config['token']}/sendMessage"
    for id in config['subscribers']:
        params = {
            "chat_id": id,
            "text": text,
        }
        resp = requests.get(url, params=params)


if __name__ == "__main__":
    import yaml

    logging.basicConfig(format=' %(levelname)s %(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)
    log = logging.getLogger('logger')
    log.setLevel(logging.DEBUG)
    tBot = TBot()


    @tBot.set_config_updated_cb
    def config_updated(cfg):
        print('config_updated fn =', cfg)


    @tBot.set_get_status_fn
    def status():
        return "nothing"


    with open("config/config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        print('config=', config)
        asyncio.run(tBot.start(config["telegram"]))
