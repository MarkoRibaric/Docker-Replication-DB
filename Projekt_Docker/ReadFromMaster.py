import asyncio
import aiomysql
import time

loop = asyncio.get_event_loop()

async def read_from_database(conn, query):
    cur = await conn.cursor()
    await cur.execute(query)
    result = await cur.fetchall()
    await cur.close()

async def read_from_single_database():
    conn = await aiomysql.connect(host='127.0.0.1', port=3308,
                                   user='my_db_user', password='S3cret', db='my_db',
                                   loop=loop)

    query = "SELECT * FROM mytable"

    start_time = time.time()

    await read_from_database(conn, query)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time taken to read all data from Master Server: {elapsed_time:.2f} seconds")

    conn.close()
print("Reading data only from Master Server!")
loop.run_until_complete(read_from_single_database())
