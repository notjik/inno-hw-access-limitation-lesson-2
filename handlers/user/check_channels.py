from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

channels = []


@dp.message_handler(Command("channels"))
async def show_channels(message: types.Message):
    channels_format = str()
    for channel in channels:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f'Канал <a href="{invite_link}">{chat.title}</a>\n\n'
    await message.answer(f'Вам необходимо подписаться на следующие каналы: \n' + channels_format,
                         reply_markup=types.InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     types.InlineKeyboardButton(text='Проверить подписки', callback_data="check_subs")
                                 ]
                             ]
                         )
                         ,
                         disable_web_page_preview=True)


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in channels:
        member = await bot.get_chat_member(chat_id=channels, user_id=call.from_user.id)
        status = await member.is_chat_member()
        channel = await bot.get_chat(channel)
        if status:
            result += f'Подписка на канал {channel.title} оформлена!'
        else:
            invite_link = await channel.export_invite_link()
            result += (f'Подписка на канал {channel.title} не оформлена!'
                       f'<a href="{invite_link}">Нужно  подписаться.</a>\n\n')
    await call.message.answer(result, disable_web_page_preview=False)
