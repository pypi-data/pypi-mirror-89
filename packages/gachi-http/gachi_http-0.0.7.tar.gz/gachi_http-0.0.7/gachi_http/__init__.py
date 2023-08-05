import asyncio
from aiohttp import ClientSession, ClientTimeout
from json import loads
from aiohttp_socks import ProxyConnector
from threading import Thread, currentThread
from ssl import create_default_context


class Response:
    def __init__(self, status, headers, content=None):
        self.status_code = status
        self.content = content
        self.text = None
        if self.content is not None:
            self.text = self.content.decode("latin1")
        self.headers = {}
        for h in headers.keys():
            val = headers[h]
            self.headers[h] = val

    def json(self):
        return loads(self.text)

    def __repr__(self):
        return f"<Response [{self.status_code}]>"


class ThreadExecutor:
    def __init__(self):
        self.status = "not_started"
        self.data = None
        self.thread = None

    def start(self):
        if self.status != "not_started":
            return
        self.thread = currentThread()
        self.status = "running"

    def setData(self, data):
        self.data = data

    def finished(self):
        if self.status != "running":
            return [False]
        elif self.thread.is_alive():
            return [False]
        self.thread = None
        self.status = "not_started"
        return [True, self.data]

    def __repr__(self):
        return f'Thread ["{self.status}"]'


class Request:
    def __init__(self, method, url, params, data, json, headers, proxies, skip_headers):
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.json = json
        self.headers = headers
        self.proxies = proxies
        self.skip_headers = skip_headers

    def __repr__(self):
        return f'<Request [{self.method} "{self.url}"]>'


def __startswith(word, _list):
    starts = False
    for w in _list:
        if word.startswith(w):
            starts = True
            break
    return starts


def request(method, url, params=None, data=None, json=None, headers=None, proxies=None, skip_headers=None):
    if skip_headers is None:
        skip_headers = []
    if data is None and json is None:
        skip_headers.append('Content-Type')
    if method not in ['POST', 'GET', 'PUT', 'HEAD', 'OPTIONS', 'DELETE', 'PATCH']:
        return None
    if isinstance(proxies, dict):
        proxies = list(proxies.values())[0]
        if not __startswith(proxies, ['http', 'https', 'socks4', 'socks5']):
            proxies = None
        else:
            proxies = ProxyConnector.from_url(proxies)
    return Request(method, url, params, data, json, headers, proxies, skip_headers)


# ---Methods---

def get(url, params=None, headers=None, proxies=None):
    return request('GET', url=url, params=params, headers=headers, proxies=proxies)


def head(url, params=None, headers=None, proxies=None):
    return request('HEAD', url=url, params=params, headers=headers, proxies=proxies)


def options(url, params=None, headers=None, proxies=None):
    return request('OPTIONS', url=url, params=params, headers=headers, proxies=proxies)


def delete(url, params=None, headers=None, proxies=None):
    return request('DELETE', url=url, params=params, headers=headers, proxies=proxies)


def post(url, params=None, data=None, json=None, headers=None, proxies=None):
    return request('POST', url=url, params=params, data=data, json=json, headers=headers, proxies=proxies)


def patch(url, params=None, data=None, json=None, headers=None, proxies=None):
    return request('PATCH', url=url, params=params, data=data, json=json, headers=headers, proxies=proxies)


def put(url, params=None, data=None, json=None, headers=None, proxies=None):
    return request('PUT', url=url, params=params, data=data, json=json, headers=headers, proxies=proxies)


async def __execReq(sess, req, ssl, include_content, exception_handler, success_handler):
    try:
        async with sess.request(method=req.method, url=req.url, params=req.params, data=req.data, json=req.json,
                                headers=req.headers,
                                proxy=req.proxies, skip_auto_headers=req.skip_headers, ssl=ssl) as resp:
            content = None
            if include_content:
                content = await resp.read()
            final = Response(resp.status, resp.headers, content)
            if success_handler is not None:
                Thread(target=success_handler, args=[final]).start()
            return final
    except Exception as e:
        if exception_handler is not None:
            Thread(target=exception_handler, args=[e]).start()


async def __makeReqs(reqs, size, timeout, include_content, exception_handler, success_handler):
    resp = []
    sem = asyncio.Semaphore(size)
    ssl = create_default_context()
    async with ClientSession(timeout=ClientTimeout(total=timeout)) as sess:
        async with sem:
            for req in reqs:
                data = await __execReq(sess, req, ssl, include_content, exception_handler, success_handler)
                if not data:
                    resp.append(None)
                    continue
                resp.append(data)
    return resp


def map(reqs, size=10, timeout: int = None, include_content=True, exception_handler=None, success_handler=None):
    if not reqs or not isinstance(reqs[0], Request):
        return None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    fut = asyncio.gather(__makeReqs(reqs, size, timeout, include_content, exception_handler, success_handler))
    resp = loop.run_until_complete(fut)
    loop.close()
    return resp[0]


def __threaded(executor: ThreadExecutor, reqs, size, timeout, include_content, exception_handler, success_handler):
    executor.start()
    resp = map(reqs, size, timeout, include_content, exception_handler, success_handler)
    executor.setData(resp)


def mapThreaded(reqs, size=10, timeout: int = None, include_content=True, exception_handler=None, success_handler=None):
    if not reqs or not isinstance(reqs[0], Request):
        return None
    executor = ThreadExecutor()
    t = Thread(target=__threaded,
               args=[executor, reqs, size, timeout, include_content, exception_handler, success_handler])
    t.start()
    return executor
