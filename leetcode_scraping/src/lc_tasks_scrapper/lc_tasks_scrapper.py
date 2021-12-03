import json
import logging
import os

from leetcode_scraping.src.scrapping_bee_shared_client. \
    scrapping_bee_shared_client import ScrBeeSharedClient
from leetcode_scraping.src.utils.const import SCRAPING_BEE_API_KEYS_JSON, \
    LOG_DIR, SCRAPPED_LC_TASKS_DIR

logging.basicConfig(filename=os.path.join(LOG_DIR, 'CommonLog2.log'),
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


class LcTasksScrapper:
    TASK_CONTENT_HTML_CLASS = '.question-content__JfgR'

    def __init__(self, path_to_lc_tasks_refs_json,
                 output_dir=SCRAPPED_LC_TASKS_DIR):
        self.path_to_lc_tasks_refs_json_ = path_to_lc_tasks_refs_json
        self.output_dir_ = output_dir
        self.sh_scrap_client = ScrBeeSharedClient(SCRAPING_BEE_API_KEYS_JSON)

    def scrap_lc_tasks(self):
        with open(self.path_to_lc_tasks_refs_json_, 'r') as in_json:
            comp_stage_to_lc_links = json.load(in_json)

        stop_link_passed = False
        for comp_stage, links in comp_stage_to_lc_links.items():
            for link in links:

                # FIXME  HARDCODE:
                if link == 'https://leetcode.com/problems/' \
                           'similar-string-groups/':
                    stop_link_passed = True
                    continue

                if not stop_link_passed:
                    continue

                task_name = self.__get_task_name_from_link(link)
                logging.info(f'started processing task {task_name}, {link}')
                html_fname_path = os.path.join(self.output_dir_,
                                               f'task__{task_name}__{comp_stage}.html')

                response = self.sh_scrap_client. \
                    get(link,
                        params={'wait_for': self.TASK_CONTENT_HTML_CLASS})

                if response.status_code != 200:
                    logging.warning(f'got response status code'
                                    f' {response.status_code} for {link}.'
                                    f' {task_name} task skipped')
                    continue

                with open(html_fname_path, 'wb') as out_html:
                    out_html.write(response.content)
                logging.info(f'Successfully processed {task_name}, {link}!')

    @staticmethod
    def __get_task_name_from_link(link: str):
        return link.split('/')[-2]
