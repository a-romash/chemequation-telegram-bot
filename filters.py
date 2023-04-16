from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from config import CREATOR_ID


class IsAdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


class IsCreatorFilter(BoundFilter):
    key = "is_creator"

    def __init__(self, is_creator):
        self.is_creator = is_creator

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        if member["user"]["id"] == CREATOR_ID:
            return True
        else:
            return False
