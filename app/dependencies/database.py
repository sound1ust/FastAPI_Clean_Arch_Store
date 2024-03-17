from starlette.requests import Request


async def get_conn(request: Request):
    async with request.app.state.pool.acquire() as connection:
        yield connection
