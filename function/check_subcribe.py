from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from config.config import channel_ids, channel_links

async def check_subsription(user_id):
    if channel_links == []:
        return True
    else:
        for channel_id in channel_ids:
            data = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            status = str(data.status)
            # print(status)
            if status == 'left':
                return False
        return True
