import httpx
import asyncio


async def test_request():
    test_urls = [
        ('get', 'http://127.0.0.1:8080/api/v2/users/1'),
        ('get', 'http://127.0.0.1:8080/api/v2/users'),
        ('get', 'http://127.0.0.1:8080/api/v2/users/N'),
        ('post', 'http://127.0.0.1:8080/api/v2/users'),
        ('post', 'http://127.0.0.1:8080/api/v2/users/1'),
        ('post', 'http://127.0.0.1:8080/api/v2/users/N'),
        ('delete', 'http://127.0.0.1:8080/api/v2/users/6'),
        ('delete', 'http://127.0.0.1:8080/api/v2/users'),
        ('delete', 'http://127.0.0.1:8080/api/v2/users/N')
    ]

    async with httpx.AsyncClient() as client:
        reqs = []
        for url in test_urls:
            method = url[0]
            if method == 'get':
                reqs.append(client.get(url[1]))
            elif method == 'post':
                reqs.append(client.post(url[1]))
            elif method == 'delete':
                reqs.append(client.delete(url[1]))
        results = await asyncio.gather(*reqs)

    for i, res in enumerate(results):
        print(i + 1, res)
        if i < 2:
            print(res.json())

asyncio.run(test_request())
