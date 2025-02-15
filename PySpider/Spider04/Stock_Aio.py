import aiohttp
import asyncio

@asyncio.coroutine
def get_stock(code):
    url = 'http://hq.sinajs.cn/list=' + code
    response = yield from aiohttp.request('GET', url)
    body = yield from response.read()
    print(body.decode('gb2312'))

if __name__ == '__main__':
    codes = ['sz000878', 'sh600993', 'sz000002', 'sh600153', 'sz002230', 'sh600658']
    tasks = [get_stock(code) for code in codes]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()