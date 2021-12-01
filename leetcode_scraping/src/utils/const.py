import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
SCRAPPED_PAGES_DIR = os.path.join(DATA_DIR, 'scrapped_discuss_pages')
RESOURCES_DIR = os.path.join(ROOT_DIR, 'resources')
SCRAPING_BEE_API_KEYS_JSON = os.path.join(RESOURCES_DIR,
                                          'scraping_bee_api_keys.json')

COMPANIES = ['google', 'facebook', 'amazon', 'uber', 'microsoft', 'airbnb']
STAGES = ['phone-screen-2', 'online-assessment', 'onsite']

BASE_DISC_PAGE_URL = 'https://leetcode.com/discuss/interview-question?' \
                     'currentPage=1&orderBy=hot&query='
