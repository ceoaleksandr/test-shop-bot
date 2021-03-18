import logging
import config
import asyncio
from aiogram import Bot , Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage 

bot = Bot(
    token = config.TG_TOKEN,
)

loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop , storage = MemoryStorage())

logging.basicConfig(level = logging.INFO)