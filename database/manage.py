import aiosqlite, logging, traceback
import asyncio

path_to_db = 'database/gemsshop.db'
def error_handler(f, path_to_db = path_to_db, *args, **kwargs):
    async def wrapped(*args, **kwargs):
        async with aiosqlite.connect(path_to_db) as db:
            try:
                return await f(db, *args, **kwargs)
            except Exception as e:
                stack = traceback.extract_stack()
                print(f"An exception occured in {stack[-2][2]} | {e}")
    return wrapped

@error_handler
async def get_state(db, user):
    query = f'select state from user'
    lvl = await db.execute(query)
    lvl = await lvl.fetchall()
    print(lvl)
    if not lvl:
        return 0
    lvl, = lvl[0]
    return lvl

@error_handler
async def get_mode(db, user):
    query = f'select mode from user where user_id = {user}'
    lvl = await db.execute(query)
    lvl = await lvl.fetchall()
    if not lvl:
        return 0
    lvl, = lvl[0]
    return lvl

@error_handler
async def set_state(db, user, state, mode = 'null'):
    query = f"update user set state = {state}, mode = '{mode}' where user_id = {user};"
    await db.execute(query)
    await db.commit()

@error_handler
async def add_character(db, name):
    query = f"insert into character (name) values ('{name}');"
    await db.execute(query)
    await db.commit()

@error_handler
async def update_character(db, photo, name):
    query = f"update character set photo = '{photo}' where name = '{name}';"
    await db.execute(query)
    await db.commit()

@error_handler
async def update_default_character(db, photo):
    query = f"update default_character set photo = '{photo}';"
    await db.execute(query)
    await db.commit()

@error_handler
async def delete_character(db, name):
    query = f"delete from character where name = '{name}';"
    await db.execute(query)
    await db.commit()
    
@error_handler
async def get_characters(db):
    query = f"select name from character"
    cursor = await db.execute(query)
    characters = await cursor.fetchall()
    if characters:
        characters = [character[0] for character in characters]
    else:
        characters = []
    return characters

@error_handler
async def get_default_message(db):
    query = f"select photo from default_character;"
    cursor = await db.execute(query)
    photo = await cursor.fetchone()
    if photo:
        photo = photo[0]
    return photo

@error_handler
async def get_character(db, name):
    query = f"select photo from character where name = '{name}';"
    cursor = await db.execute(query)
    photo = (await cursor.fetchone())[0]
    return photo

@error_handler
async def get_user(db, user_id):
    query = f'select user_id from user where user_id = {user_id}'
    user = await (await db.execute(query)).fetchone()
    return user

@error_handler
async def register_user(db, user_id):
    query = f'insert into user (user_id, state) values ({user_id}, 0)'
    await db.execute(query)
    await db.commit()
