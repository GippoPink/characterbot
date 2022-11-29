from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from database.manage import get_characters

async def k_god_menu():
    keyboard = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    buttons = ['Изменить стартовое сообщение', 'Добавить персонажа', 'Изменить персонажа', 'Удалить персонажа', 'Главное меню']
    keyboard.add(*buttons)
    return keyboard

async def k_god_characters():
    keyboard = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    buttons = await get_characters() + ['Отмена'] if await get_characters() else ['Отмена']
    keyboard.add(*buttons)
    return keyboard

async def k_cancel():
    keyboard = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    buttons = ['Отмена']
    keyboard.add(*buttons)
    return keyboard



