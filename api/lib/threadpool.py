import asyncio
import concurrent.futures
import functools


EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4)


async def call_async(fn, *args, **kwargs):
    fn = functools.partial(fn, *args, **kwargs)
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(EXECUTOR, fn)
    return result
