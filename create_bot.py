from config import BOT_TOKEN
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)
db = Dispatcher(bot, storage=MemoryStorage())
