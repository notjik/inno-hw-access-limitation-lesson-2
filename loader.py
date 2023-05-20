import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import DatabaseManager

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DatabaseManager('database.db')
db.create_tables()
