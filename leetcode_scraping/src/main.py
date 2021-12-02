from lc_tasks_refs_scrapper.lc_tasks_refs_scrapper import LcTasksRefsScrapper
from utils.const import DISCUSS_LINKS_JSON, SCRAPPED_LC_LINKS_JSON


def main():
    lctrs = LcTasksRefsScrapper(DISCUSS_LINKS_JSON, SCRAPPED_LC_LINKS_JSON)
    lctrs.scrap_task_links()


if __name__ == '__main__':
    main()
