# import asyncpg
# import asyncio
# import dotenv
#
# env_path = "../.env"
#
# DATABASE_SETTINGS = {
#     'database': dotenv.get_key(env_path, 'DATABASE_NAME'),
#     'user': dotenv.get_key(env_path, 'DATABASE_USER'),
#     'password': dotenv.get_key(env_path, 'DATABASE_PASSWORD'),
#     'host': dotenv.get_key(env_path, 'DATABASE_HOST'),
#     'port': dotenv.get_key(env_path, 'DATABASE_PORT'),
# }
#
#
# async def run():
#     connection = await asyncpg.connect(**DATABASE_SETTINGS)
#     rows = await connection.fetch('''
#     SELECT * FROM products
#     WHERE name ILIKE '%phone%' AND category = 'Electronics'
#     ORDER BY product_id
#     LIMIT 2;
#     ''')
#     print(rows)
#
#
# asyncio.get_event_loop().run_until_complete(run())
