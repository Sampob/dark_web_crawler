from app.celery_config import celery
from app.util.fetch_resources import fetch_crawl_urls, fetch_regex_patterns
from app.dark_web_crawler.spiders.dark_web_spider import DarkWebSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

@celery.task
def schedule_crawls():
    urls_to_crawl = fetch_crawl_urls()

    regex_patterns_to_find = fetch_regex_patterns()
    
    process = CrawlerProcess(get_project_settings())
    for url in urls_to_crawl:
        process.crawl(DarkWebSpider, start_urls=url, regex_patterns=regex_patterns_to_find)
    process.start()

@celery.task
def run_spider(urls: str | list, patterns: list):
    try:
        process = CrawlerProcess(get_project_settings())
        if isinstance(urls, str):
            process.crawl(DarkWebSpider, start_urls=urls, regex_patterns=patterns)
        else:
            for url in urls:
                process.crawl(DarkWebSpider, start_urls=url, regex_patterns=patterns)
        process.start()
    except Exception as e:
        if hasattr(e, "message"):
            error_msg = e.message
        else:
            error_msg = e
        return {"status": "error", "urls": urls, "error": error_msg}
    return {"status": "success", "urls": urls}