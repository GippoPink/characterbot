from loader import dp, bot
# from aiogram import types
# from aiogram.types import ReplyKeyboardRemove
# from aiogram.dispatcher import FSMContext

# @dp.chat_join_request_handler()
# async def user_joined_chat(message: types.Message):
#     user_id = int(message.from_user.id)
#     user = await get_user(user_id)
#     if user is None:
#         await register_user(user_id)
#     await message.approve()
#     await bot.send_message(message.from_user.id, await get_start_message())

# @dp.message_handler(command=['start'])
# async def start(message: types.Message):
#     user_id = int(message.from_user.id)
#     user = await get_user(user_id)
#     if user is None:
#         await register_user(user_id)
#     await message.approve()
#     await bot.send_message(message.from_user.id, await get_start_message())