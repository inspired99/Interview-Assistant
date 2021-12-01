import logging
import os.path

from leetcode_scraping.src.scrapping_bee_shared_client. \
    scrapping_bee_shared_client import ScrBeeSharedClient
from leetcode_scraping.src.utils.const import LOG_DIR, SCRAPPED_PAGES_DIR, \
    COMPANIES, STAGES, SCRAPING_BEE_API_KEYS_JSON
from leetcode_scraping.src.utils.file_utils import write_response_content
from leetcode_scraping.src.utils.url_utils import make_disc_page_url

logging.basicConfig(filename=os.path.join(LOG_DIR, 'DiscPageScrap.log'),
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    )

logging.getLogger().setLevel(logging.INFO)


class DiscPagesScrapper:
    def __init__(self, companies=COMPANIES, stages=STAGES,
                 output_dir=SCRAPPED_PAGES_DIR):
        self.companies_ = companies
        self.stages_ = stages
        self.output_dir_ = output_dir
        self.sh_scrap_client = ScrBeeSharedClient(SCRAPING_BEE_API_KEYS_JSON)

    def scrap(self):
        for comp in self.companies_:
            for stage in self.stages_:
                url = make_disc_page_url(comp, stage)
                response = \
                    self.sh_scrap_client.get(url,
                                             params={'wait_for':
                                                         '.topic-title__3LYM'})
                if response.status_code != 200:
                    logging.warning(f'got response status code'
                                    f' {response.status_code} for url: {url}')
                else:
                    write_response_content(SCRAPPED_PAGES_DIR,
                                           comp, stage, response.content)
                    logging.info(f'successfully scrapped url: {url} ')



