import os
import json
import base64
import aiofiles as aiof
from dotenv import load_dotenv

load_dotenv()

API_URL = 'http://www.giantbomb.com/api/'
API_KEY = os.environ.get('API_KEY')

PLATFORMS = ['NES', 'SNES', 'N64']


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

