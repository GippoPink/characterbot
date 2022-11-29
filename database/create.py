import aiosqlite, logging, traceback
import asyncio

path_to_db = 'database/characters.db'
def error_handler(f, path_to_db = path_to_db):
    async def wrapped(path_to_db = path_to_db, *args, **kwargs):
        async with aiosqlite.connect(path_to_db) as db:
            try: 
                return await f(db, *args, **kwargs)
            except Exception as e:
                stack = traceback.extract_stack()
                print(f"An exception occured in {stack[-2][2]} | {e}")
    return wrapped

@error_handler
async def create_tables(db):
    await db.execute("""CREATE TABLE IF NOT EXISTS user (
            id INTEGER primary key autoincrement,
            user_id INTEGER,
            state integer,
            mode varchar(256)
            )""")

    await db.commit()
    
    await db.execute("""CREATE TABLE IF NOT EXISTS default_character (
            id INTEGER primary key autoincrement,
            photo varchar(1000) not null
            )""")
    
    await db.commit()

    await db.execute("""CREATE TABLE IF NOT EXISTS character (
            id INTEGER primary key autoincrement,
            name varchar(256),
            photo varchar(1000)
            )""")
    
    await db.commit()

@error_handler
async def default_insert(db):
    query = (
        "insert into default_character (photo) values "
        "('тестовая картинка')"
                )
    await db.execute(query)
    await db.commit()
