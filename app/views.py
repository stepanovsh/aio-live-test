import asyncio
import logging
from functools import reduce

import aiohttp_jinja2
from aiohttp import web

import common
from index import index, db, indexing_document


@aiohttp_jinja2.template('base.html')
async def handle(request):
    """Search handler"""
    search = request.query.get('search', '')
    if not index.indexed:
        # ToDo add file check
        logging.info('Start indexing from file')
        games_result = await common.return_from_file('games.bin')
        indexing_document(games_result)
        logging.info('Finish indexing from file')

    result_list = []
    if search:
        result = index.lookup_query(search)

        result_list = []
        for term in result.keys():
            for appearance in result[term]:
                document = db.get(appearance.doc_id)
                result_list.append(common.Game(id=appearance.doc_id, name=document['text']))
    return {
        'title': 'Search',
        'result_list': result_list,
        'search': search
    }


async def sync(request):
    """Sync handler"""
    text = "Hello,  Finish"
    tasks = [asyncio.ensure_future(common.get_platforms_ids(abrv)) for abrv in common.PLATFORMS]
    result_set = reduce(lambda base, next_el: base.union(next_el), await asyncio.gather(*tasks))

    tasks = [asyncio.ensure_future(common.get_games_titles(platform_id)) for platform_id in result_set]

    results = await asyncio.gather(*tasks)

    def update_dict(base, next_el):
        base.update(next_el)
        return base

    games_result = reduce(update_dict, results)

    indexing_document(games_result)

    await common.save_to_file(games_result, 'games.bin')

    return web.Response(text=text)




