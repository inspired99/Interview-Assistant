from leetcode_scraping.src.utils.const import BASE_DISC_PAGE_URL


def make_disc_pages_urls(companies: list, stages: list,
                         base_url: str = BASE_DISC_PAGE_URL):
    res = []
    for stage in stages:
        for comp in companies:
            res.append(f'{base_url}&tag={stage}&tag={comp}')
    return res


def make_disc_page_url(company, stage, base_url=BASE_DISC_PAGE_URL):
    return f'{base_url}&tag={stage}&tag={company}'
