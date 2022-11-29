from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from config.config import channel_links, global_admins
from database.manage import get_characters

async def k_main_menu(user_id):
    keyboard = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    buttons = ['Выбрать персонажа']
    keyboard.add(*buttons)
    if user_id in global_admins:
        keyboard.add('Режим бога')
    return keyboard

async def sub():
    keyboard = InlineKeyboardMarkup(row_width=1)
    links = channel_links
    for i, link in enumerate(links):
        txt = str(i + 1)
        keyboard.add(InlineKeyboardButton(f'Канал {txt}', url=link))
    keyboard.add(InlineKeyboardButton(f'Я подписался✅', callback_data='gotovo'))
    return keyboard

async def k_characters():
    keyboard = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    buttons = await get_characters() + ['Главное меню'] if await get_characters() else ['Главное меню']
    keyboard.add(*buttons)
    return keyboard
