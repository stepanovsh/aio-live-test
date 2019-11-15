import os
from dotenv import load_dotenv

load_dotenv()

API_URL = 'http://www.giantbomb.com/api/'
API_KEY = os.environ.get('API_KEY')

PLATFORMS = ['NES', 'SNES', 'N64']
