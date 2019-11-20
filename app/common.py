import logging
import os
import json
import base64
from collections import namedtuple
from urllib.parse import urlencode

import aiofiles as aiof
import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_URL = 'http://www.giantbomb.com/api/'
API_KEY = os.environ.get('API_KEY')

PLATFORMS = ['NES', 'SNES', 'N64']

Game = namedtuple('Game', ['id', 'name'])


async def save_to_file(result: dict, filename: str) -> bool:
    result_str = json.dumps(result).encode('utf-8')
    result_dump = base64.b64encode(result_str)

    async with aiof.open(filename, "wb") as out:
        await out.write(result_dump)
        await out.flush()
    return True


async def return_from_file(filename: str) -> dict:
    async with aiof.open(filename, "rb") as out:
        result_dump = await out.read()
        await out.flush()
    result_str = base64.b64decode(result_dump)

    return json.loads(result_str)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_platforms_ids(abbreviation: str) -> frozenset:
    """Retrieve platforms id async"""
    offset = 0
    limit = 100
    size = limit
    ids = set()
    url_params = {
        'api_key': API_KEY,
        'format': 'json',
        'offset': offset,
        'limit': limit,
        'filter': 'abbreviation:{}'.format(abbreviation)
    }

    async with aiohttp.ClientSession() as session:
        while offset < size:
            url = '{}{}/?{}'.format(API_URL, 'platforms', urlencode(url_params))
            logging.info('fetching url: %s', url)

            resp = await fetch(session, url)

            results = resp.get('results', [])
            for res in results:
                if res['abbreviation'] == abbreviation:
                    ids.add(res['id'])
            size = resp.get('number_of_total_results', limit)
            offset += limit
            url_params['offset'] = offset
    return frozenset(ids)


async def get_games_titles(platform_id: int) -> dict:
    """Retrieve games async"""
    logging.info('Start fetching: %s games', platform_id)
    offset = 0
    limit = 100
    size = limit
    game_obj = dict()
    url_params = {
        'api_key': API_KEY,
        'format': 'json',
        'offset': offset,
        'limit': limit,
        'platforms': platform_id
    }

    async with aiohttp.ClientSession() as session:
        while offset < size:
            url = '{}{}/?{}'.format(API_URL, 'games', urlencode(url_params))
            logging.info('fetching url: %s', url)

            resp = await fetch(session, url)

            results = resp.get('results', [])
            for res in results:
                game_obj[res['id']] = Game(
                    id=res['id'],
                    name=res['name']
                )
            size = resp.get('number_of_total_results', limit)
            offset += limit
            url_params['offset'] = offset

    logging.info('Finish fetching: %s games', platform_id)
    return game_obj

