import json
import logging.handlers
import os

from bs4 import BeautifulSoup

from leetcode_scraping.src.scrapping_bee_shared_client. \
    scrapping_bee_shared_client import ScrBeeSharedClient
from leetcode_scraping.src.utils.const import SCRAPPED_PAGES_DIR, LOG_DIR, \
    SCRAPING_BEE_API_KEYS_JSON

logging.basicConfig(filename=os.path.join(LOG_DIR, 'CommonLog.log'),
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


class DiscLinksScrapper:
    LC_PREFIX = "https://leetcode.com"

    def __init__(self, output_json_fname,
                 scrapped_discuss_pages_dir=SCRAPPED_PAGES_DIR) -> None:
        self.output_json_fname_ = output_json_fname
        self.scrapped_discuss_pages_dir_ = scrapped_discuss_pages_dir
        self.comp_stage_to_disc_link = {}

    def scrap_links(self) -> None:
        for html_fname in os.listdir(self.scrapped_discuss_pages_dir_):
            logging.info(f'Started processing {html_fname}...')
            html_f_path = os.path.join(self.scrapped_discuss_pages_dir_,
                                       html_fname)
            with open(html_f_path, 'r') as in_html:
                html_text = in_html.read()

            soup = BeautifulSoup(html_text, 'lxml')
            if soup is None:
                logging.warning(f'Error parsing {html_fname}'
                                f' (bs4 returned None)')
                continue
            content = soup.find_all('a', class_='title-link__1ay5')
            self.comp_stage_to_disc_link[html_fname.split('.')[0]] = \
                [self.LC_PREFIX + x.get('href') for x in content]
            logging.info(f'Successfully done with {html_fname}!')

        with open(self.output_json_fname_, 'w') as out_json:
            json.dump(self.comp_stage_to_disc_link, out_json)
