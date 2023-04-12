import aiosqlite as sq

conn = sq.connect('history', check_same_thread=False)
cursor = conn.cursor()


async def sql_start():
    global base, cur
    base = await sq.connect('history.db')
    cur = await base.cursor()
    if base:
        print('База данных подключена')
    await base.execute('CREATE TABLE IF NOT EXISTS history(us_id INT, user_id INT, country STR, city STR, button)')
    await base.commit()


async def db_table_val(us_id: int, user_id: str, country: str, city: str, button):
    await cur.execute('INSERT INTO history (us_id, user_id, country, city, button) VALUES (?, ?, ?, ?, ?)', (us_id, user_id, country, city, button))
    await base.commit()
