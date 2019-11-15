import asyncio
import logging

import aiohttp
from aiohttp import web
from urllib.parse import urlencode
from collections import namedtuple

import common


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_platforms_ids(abbreviation: str, ids: set):
    """Retrieve platforms id async"""
    offset = 0
    limit = 100
    size = limit
    url_params = {
        'api_key': common.API_KEY,
        'format': 'json',
        'offset': offset,
        'limit': limit,
        'filter': 'abbreviation:{}'.format(abbreviation)
    }

    async with aiohttp.ClientSession() as session:
        while offset < size:
            url = '{}{}/?{}'.format(common.API_URL, 'platforms', urlencode(url_params))
            logging.info('fetching url: %s', url)

            resp = await fetch(session, url)

            results = resp.get('results', [])
            for res in results:
                if res['abbreviation'] == abbreviation:
                    ids.add(res['id'])
            size = resp.get('number_of_total_results', limit)
            offset += limit
            url_params['offset'] = offset


async def get_games_titles(platform_id: int, game_obj: dict):
    """Retrieve games async"""
    logging.info('Start fetching: %s games', platform_id)
    offset = 0
    limit = 100
    size = limit
    Game = namedtuple('Game', ['id', 'name', 'original_game_rating'])
    url_params = {
        'api_key': common.API_KEY,
        'format': 'json',
        'offset': offset,
        'limit': limit,
        'platforms': platform_id
    }

    async with aiohttp.ClientSession() as session:
        while offset < size:
            url = '{}{}/?{}'.format(common.API_URL, 'games', urlencode(url_params))
            logging.info('fetching url: %s', url)

            resp = await fetch(session, url)

            results = resp.get('results', [])
            for res in results:
                game_obj[res['id']] = Game(
                    id=res['id'],
                    name=res['name'],
                    original_game_rating=res.get('original_game_rating')
                )
            size = resp.get('number_of_total_results', limit)
            offset += limit
            url_params['offset'] = offset

    logging.info('Finish fetching: %s games', platform_id)


async def sync(request):
    text = "Hello,  Finish"
    result_set = set()
    tasks = [get_platforms_ids(abrv, result_set) for abrv in common.PLATFORMS]
    await asyncio.wait(tasks)

    game_obj = {}

    tasks = [get_games_titles(platform_id, game_obj) for platform_id in result_set]

    await asyncio.wait(tasks)

    return web.Response(text=text)




