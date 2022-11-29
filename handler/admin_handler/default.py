from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from asyncio import run
from aiogram.dispatcher.filters import BoundFilter
from database.manage import *
from keyboard.admin_keyboard import *
from keyboard.user_keyboard import k_main_menu
from filter.filter import State, IsCharacter, IsAdmin, AdminStates, Mode

@dp.message_handler(IsAdmin(), lambda message: message.text.lower() == 'режим бога')
async def change_mode(message: types.message):
    user = int(message.from_user.id)
    await set_state(user, -1)
    print(await get_state(user))
    message = '''Выбери действие:'''
    await bot.send_message(user, message, reply_markup = await k_god_menu())

# @dp.message_handler(lambda message: message.text.lower() == 'главное меню')
# async def cancel(message: types.message):
#     user = int(message.from_user.id)
#     await set_state(user, 0)
#     message = await get_default_message()
#     await bot.send_message(user, message, reply_markup = await k_main_menu(user))

@dp.message_handler(IsAdmin(), AdminStates(0), lambda message: message.text.lower() == 'отмена')
async def cancel(message: types.message):
    user = int(message.from_user.id)
    await set_state(user, -1)
    message = await get_default_message()
    await bot.send_message(user, message, reply_markup = await k_god_menu())

modes = {
    -2: 'change_start_message_1',
    -3: 'add_character_step_1',
    -4: 'add_character_step_2',
    -5: 'change_character',
    -6: 'delete_character'
    }

@dp.message_handler(IsAdmin(), lambda message: message.text.lower() in ['изменить стартовое сообщение', 'удалить персонажа'])
async def choose_action(message: types.message):
    user = int(message.from_user.id)
    if message.text.lower() == 'изменить стартовое сообщение':
        # await set_state(user, -2, mode = 'choose')
        message = 'Введи новое сообщение:'
        await set_state(user, -2, mode = 'enter')
    else:
        await set_state(user, -6, mode = 'delete')
        message = 'Выбери персонажа:'
    await bot.send_message(user, message, reply_markup = await k_god_characters())


@dp.message_handler(IsAdmin(), IsCharacter(), State(-6), Mode('delete'))
async def del_character(message: types.message):
    user = int(message.from_user.id)
    await delete_character(message.text)
    message = 'Персонаж успешно удален'
    await set_state(user, -2)
    await bot.send_message(user, message, reply_markup = await k_god_menu())

@dp.message_handler(IsAdmin(), State(-2), Mode('enter'))
async def change_start_message_2(message: types.message):
    user = int(message.from_user.id)
    await update_default_character(message.text)
    await set_state(user, -1)
    message = f'Новое сообщение: {message.text}'
    await bot.send_message(user, message, reply_markup = await k_god_menu())

@dp.message_handler(IsAdmin(), lambda message: message.text.lower() in ['изменить персонажа'])
async def choose_action(message: types.message):
    user = int(message.from_user.id)
    message = 'Выбери персонажа:'
    await bot.send_message(user, message, reply_markup = await k_god_characters())
    await set_state(user, -3, mode = 'choose')

@dp.message_handler(IsAdmin(), State(-3), Mode('choose'))
async def add_character_step_1(message: types.message):
    user = int(message.from_user.id)
    await set_state(user, -4, mode = f'{message.text}')
    message = f'Ты выбрал {message.text}. Введи сообщение:'
    await bot.send_message(user, message, reply_markup = await k_cancel())
    
@dp.message_handler(IsAdmin(), State(-4))
async def add_character_step_2(message: types.message):
    user = int(message.from_user.id)
    await update_character(message.text, await get_mode(user))
    message = f'Новое сообщение: {message.text}'
    await set_state(user, -1)
    await bot.send_message(user, message, reply_markup = await k_god_menu())

@dp.message_handler(IsAdmin(), lambda message: message.text.lower() in ['добавить персонажа'])
async def choose_action(message: types.message):
    user = int(message.from_user.id)
    message = 'Введи имя персонажа:'
    await bot.send_message(user, message, reply_markup = await k_god_characters())
    await set_state(user, -5, mode = 'choose')

@dp.message_handler(IsAdmin(), State(-5), Mode('choose'))
async def add_character_step_1(message: types.message):
    user = int(message.from_user.id)
    await add_character(message.text)
    await set_state(user, -4, mode = f'{message.text}')
    message = f'Ты добавляешь {message.text}. Введи сообщение:'
    await bot.send_message(user, message, reply_markup = await k_cancel())
    
