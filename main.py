import asyncio

from aiogram import Bot
from aiogram.enums import ParseMode
from environs import Env

from folder_watcher_bot import FolderMonitor


env = Env()
env.read_env()


async def main():
    tgbot = Bot(token=env.str("API_TOKEN"), parse_mode=ParseMode.HTML)
    folder_monitor = FolderMonitor(
        env.str("FOLDER_PATH"), env.int("CHAT_ID"), tgbot
    )
    await folder_monitor.monitor_folder()


if __name__ == "__main__":
    asyncio.run(main())
