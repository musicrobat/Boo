import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand

from Zenakusn import config

from ..logging import LOGGER


class ZenakusnBot(Client):
    def __init__(self):       
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            name="BgtxD",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,        
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.id = get_me.id
        self.name = get_me.first_name
        self.username = get_me.username                
        try:
            await self.send_message(
                config.LOG_GROUP_ID, f"**» {config.MUSIC_BOT_NAME} Bot Started :**\n\nId : `{self.id}`\nName : {self.name}\nUserName : @{self.username}"
            )
        except:
            LOGGER(__name__).error(
                "Bot has failed to access the log Group. Make sure that you have added your bot to your log channel and promoted as admin!"
            )
            sys.exit()
        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("ping", "Check that bot is alive or dead"),
                        BotCommand("play", "Starts playing the requested song"),
                        BotCommand("skip", "Moves to the next track in queue"),
                        BotCommand("pause", "Pause the current playing song"),
                        BotCommand("resume", "Resume the paused song"),
                        BotCommand("end", "Clear the queue and leave voice chat"),
                        BotCommand("shuffle", "Randomly shuffles the queued playlist."),
                        BotCommand("playmode", "Allows you to change the default playmode for your chat"),
                        BotCommand("settings", "Open the settings of the music bot for your chat.")
                        ]
                    )
            except:
                pass
        else:
            pass
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote Bot as Admin in Logger Group"
            )
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
