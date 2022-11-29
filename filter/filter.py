from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from config.config import global_admins
from database.manage import get_state, get_mode, get_characters

class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in global_admins

class State(BoundFilter):
    def __init__(self, num):
        self.num = num
    async def check(self, message: types.Message):
        return await get_state(int(message.from_user.id)) == self.num

class Mode(BoundFilter):
    def __init__(self, mode):
        self.mode = mode
    async def check(self, message: types.Message):
        return await get_mode(int(message.from_user.id)) == self.mode

class AdminStates(BoundFilter):
    def __init__(self, num):
        self.num = num
    async def check(self, message: types.Message):
        return await get_state(int(message.from_user.id)) < self.num

class IsCharacter(BoundFilter):
    def __init__(self):
        pass
    async def check(self, message: types.Message):
        return message.text.lower() in await get_characters()
