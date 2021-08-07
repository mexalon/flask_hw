from pprint import pprint

import aiohttp
import asyncio
from app.config import ADMIN, ADMIN_PASS

HOST = 'http://localhost:5000'


async def make_request(path, method='get', **kwargs):
    async with aiohttp.ClientSession() as session:
        request_method = getattr(session, method)
        async with request_method(f'{HOST}/{path}', **kwargs) as response:
            print(response.status)
            text = await response.json()
            pprint(text)
            return text


async def main():
    some_user = {
        'username': 'test_user',
        'password': 'password123',
        'email': 'its_email@gmail.com'
    }

    """тест готовности"""
    await make_request('test', 'get')

    """список пользователей"""
    await make_request('users', 'get')

    """создать пользователя"""
    resp = await make_request('users', 'post', json=some_user)
    uid = int(resp.get('id', 1))

    """посмотреть пользователя"""
    await make_request(f"users/{uid}", 'get')

    """отправить ему письмо"""
    headers = {
        'username': ADMIN,
        'password': ADMIN_PASS,
    }
    some_mail = {
        'subject': 'test subject',
        'text': 'test text'
    }

    resp = await make_request(f"send_to_db/{uid}", 'post', headers=headers, json=some_mail)
    task_id = resp.get('task_id')

    """проверить статус отправки письма"""
    await make_request(f"send_to/{task_id}", 'get')

    """сделать рассылку по всей базе"""
    await make_request(f"send_to_db", 'post', headers=headers, json=some_mail)

    """создать обьявление"""
    headers = {
        'username': some_user.get('username'),
        'password': some_user.get('password')
    }

    body = {
        'title': 'som test title',
        'description': 'test description',
    }
    resp = await make_request('adverts', 'post', headers=headers, json=body)
    aid = int(resp.get('id', 1))

    """посмотреть oбъявление"""
    await make_request(f"adverts/{aid}", 'get')


asyncio.run(main())
