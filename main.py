async def on_startup(dp):
    from database.create import create_tables, default_insert
    from database.manage import get_default_message
    # from handler.user_handler.default import on_paid
    await create_tables()
    if not (await get_default_message()):
        await default_insert()

    # for (user, billid) in await get_unpaid():
    #     await on_paid(user, billid)

if __name__ == '__main__':
    from aiogram import executor
    from handler import dp
    executor.start_polling(dp, skip_updates = True, on_startup = on_startup)