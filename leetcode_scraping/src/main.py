from lc_tasks_scrapper.lc_tasks_scrapper import LcTasksScrapper
from utils.const import SCRAPPED_LC_LINKS_JSON


def main():
    lcts = LcTasksScrapper(SCRAPPED_LC_LINKS_JSON)
    lcts.scrap_lc_tasks()


if __name__ == '__main__':
    main()
