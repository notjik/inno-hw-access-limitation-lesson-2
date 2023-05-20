import os
import logging
import config
import handlers

from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv
from loader import dp, bot

logging.basicConfig(level=logging.INFO)
load_dotenv()

user_message = 'Пользователь'
admin_message = 'Админ'


class CheckoutState(StatesGroup):
    check_cart = State()
    name = State()
    address = State()
    confirm = State()


class ProductState(StatesGroup):
    title = State()
    body = State()
    image = State()
    price = State()
    confirm = State()


class CategoryState(StatesGroup):
    title = State()


class SosState(StatesGroup):
    question = State()
    submit = State()


class AnswerState(StatesGroup):
    answer = State()
    submit = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer('''Привет! 👋
🤖 Я бот-магазин по продаже товаров любой категории.
🛍️ Чтобы перейти в каталог и выбрать приглянувшиеся товары возпользуйтесь командой /menu.
💰 Пополнить счет можно через Яндекс.кассу, Сбербанк или Qiwi.
❓ Возникли вопросы? Не проблема! Команда /sos поможет связаться с админами, которые постараются как можно быстрее откликнуться.
    ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)

    await message.answer('Включен пользовательский режим.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('Включен админский режим.', reply_markup=ReplyKeyboardRemove())


async def startup(callback):
    await bot.set_webhook(os.getenv('WEBHOOK_HOST') + os.getenv('WEBHOOK_PATH'))


async def shutdown(callback):
    await bot.delete_webhook()


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=os.getenv('WEBHOOK_PATH'),
        host=os.getenv('WEBAPP_HOST'),
        port=os.getenv('WEBAPP_PORT'),
        on_startup=startup,
        on_shutdown=shutdown,
        skip_updates=True,
    )
