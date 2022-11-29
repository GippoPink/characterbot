from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from asyncio import run
from aiogram.dispatcher.filters import BoundFilter
from database.manage import *
from keyboard.user_keyboard import *
from filter.filter import State, IsCharacter
from function.check_subcribe import check_subsription
# class State(BoundFilter):
#     def __init__(self, num):
#         self.num = num
#     async def check(self, message: types.Message):
#         return await get_state(int(message.from_user.id)) == self.num

# class IsCharacter(BoundFilter):
#     def __init__(self):
#         pass
#     async def check(self, message: types.Message):
#         return message.text.lower() in await get_characters()

@dp.chat_join_request_handler()
async def user_joined_chat(message: types.Message):
    user_id = int(message.from_user.id)
    user = await get_user(user_id)
    if user is None:
        await register_user(user_id)
    await message.approve()
    await set_state(user_id, 0)
    await bot.send_message(message.from_user.id, await get_default_message(), reply_markup = await k_main_menu(user_id))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = int(message.from_user.id)
    user = await get_user(user_id)
    if user is None:
        await register_user(user_id)
    await set_state(user_id, 0)
    await bot.send_message(message.from_user.id, await get_default_message(), reply_markup = await k_main_menu(user_id))

@dp.message_handler(lambda message: message.text.lower() == 'главное меню')
async def cancel(message: types.message):
    user = int(message.from_user.id)
    await set_state(user, 0)
    message = await get_default_message()
    await bot.send_message(user, message, reply_markup = await k_main_menu(user))

@dp.message_handler(State(0), lambda message: message.text.lower() == 'выбрать персонажа')
async def choose_character(message: types.message):
    user = int(message.from_user.id)
    message = f'Выбери персонажа'
    await set_state(user, 1)
    await bot.send_message(user, message, reply_markup = await k_characters())

@dp.message_handler(State(1), IsCharacter())
async def send_character(message: types.message):
    user = int(message.from_user.id)
    if await check_subsription(user):
        await bot.send_message(user, await get_character(message.text), reply_markup = await k_main_menu(user))
        await set_state(user, 0)
    else: 
        await bot.send_message(user, '🔻ОШИБКА! Вы не подписаны на наших спонсоров!\nБот бесплатный благодаря им!', reply_markup= await sub())
    
@dp.callback_query_handler(text = "gotovo")
async def gotovo(message: types.Message):
    user = int(message.from_user.id)
    if await check_subsription(user):
        await bot.send_message(user, await get_character(message.text), reply_markup = await k_main_menu(user))
        await set_state(user, 0)
    else: 
        await bot.send_message(user, '🔻ОШИБКА! Вы не подписаны на наших спонсоров!\nБот бесплатный благодаря им!', reply_markup= await sub())

