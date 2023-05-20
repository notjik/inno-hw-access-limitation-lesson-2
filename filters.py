from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import BoundFilter
from config import ADMINS


class IsUser(BoundFilter):
    async def check(self, message: Message):
        return message.from_user.id not in ADMINS


class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        return message.from_user.id in ADMINS


class IsChannel(BoundFilter):
    async def check(self, message: Message):
        return message.chat.type in ChatType.CHANNEL
