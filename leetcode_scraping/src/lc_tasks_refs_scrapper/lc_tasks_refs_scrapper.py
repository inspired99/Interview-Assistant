import json
import logging
import os
from collections import defaultdict

from bs4 import BeautifulSoup

from leetcode_scraping.src.scrapping_bee_shared_client.\
    scrapping_bee_shared_client import ScrBeeSharedClient
from leetcode_scraping.src.utils.const import SCRAPING_BEE_API_KEYS_JSON, \
    LOG_DIR

logging.basicConfig(filename=os.path.join(LOG_DIR, 'CommonLog.log'),
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


class LcTasksRefsScrapper:
    LC_PROBLEM_TOKEN = 'leetcode.com/problems/'

    def __init__(self, path_to_discuss_links_json, output_json_fname):
        self.path_to_discuss_links_json_ = path_to_discuss_links_json
        self.output_json_fname_ = output_json_fname
        self.sh_scrap_client = ScrBeeSharedClient(SCRAPING_BEE_API_KEYS_JSON)

    def scrap_task_links(self) -> None:
        res_dict = defaultdict(list)
        with open(self.path_to_discuss_links_json_, 'r') as in_json:
            comp_stage_to_disc_link = json.load(in_json)

        for comp_stage, link_list in comp_stage_to_disc_link.items():
            for idx, link in enumerate(link_list):
                logging.info(f'started processing {comp_stage}, {link}')

                response = self.sh_scrap_client.get(link)

                if response.status_code != 200:
                    logging.warning(f'response status code ='
                                    f' {response.status_code} for url={link}')
                    continue

                soup = BeautifulSoup(response.content, 'lxml')

                if soup is None:
                    logging.warning(f'Error parsing {link}'
                                    f' (bs4 returned None)')

                body = soup.find('div',
                                 class_='discuss-markdown-container')
                if not body:
                    logging.warning(f'Soup is not working for link {link} :(')
                    continue

                found_anchors = body.find_all('a')
                res_links = [a.get('href') for a in found_anchors]

                valid_links = [link for link in res_links if
                               self.LC_PROBLEM_TOKEN in link]
                if valid_links:
                    logging.info(
                        f'For {comp_stage}'
                        f' valid task links were found! JSON is incoming')

                    res_dict[comp_stage].extend(valid_links)
                logging.info(f'successfully processed {comp_stage}, {link}!')
        with open(self.output_json_fname_, 'w') as out_json:
            json.dump(res_dict, out_json)
