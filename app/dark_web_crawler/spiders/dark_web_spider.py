from app.util.table_actions import send_to_table

import re
from datetime import datetime
from urllib.parse import urlparse

import scrapy

class DarkWebSpider(scrapy.Spider):
    name = "dark_web_crawler"
    
    def __init__(self, start_urls: str | list = None, regex_patterns: list | dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(start_urls, str):
            self.start_urls = [start_urls]
        else:
            self.start_urls = start_urls
        
        allowed_domains = []

        for url in self.start_urls:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            allowed_domains.append(domain)
        
        self.allowed_domains = allowed_domains

        if isinstance(regex_patterns, list):
            regex_patterns = {"default": regex_patterns}
        
        reg_patterns = {}
        try:
            for key, patterns in regex_patterns.items():
                patterns_list = []
                for pattern in patterns:
                    compiled = re.compile(pattern)
                    patterns_list.append(compiled)
                reg_patterns[key] = patterns_list
        except re.error:
            raise ValueError("Invalid regex pattern provided.")
        
        self.regex_patterns = reg_patterns

        self.logger.info(f"Spider will crawl: {", ".join(self.allowed_domains)}")
    
    def parse(self, response):
        try:
            if hasattr(response, "text"):
                page_text = response.text
                for key, patterns in self.regex_patterns.items():
                    for pattern in patterns:
                        pattern_matches = re.findall(pattern, page_text)
                        if pattern_matches:
                            for match in pattern_matches:
                                msg = {
                                    "PartitionKey": datetime.now().isoformat(),
                                    "RowKey": key,
                                    "pattern": pattern.pattern,
                                    "match": match,
                                    "url": response.url,
                                }
                                send_to_table(msg)
        
        except AttributeError as e:
            if hasattr(e, "message"):
                self.logger.error(e.message)
            else:
                self.logger.error(e)
        except Exception as e:
            if hasattr(e, "message"):
                self.logger.error(e.message)
            else:
                self.logger.error(e)
        
        if hasattr(response, "css"):
            try:
                for href in response.css("a::attr(href)").getall():
                        parsed_href = urlparse(response.urljoin(href))
                        if parsed_href.netloc in self.allowed_domains:
                            yield response.follow(href, self.parse)
            except scrapy.exceptions.NotSupported as e:
                pass # Links to image files raise this error
            except Exception as e:
                self.logger.error(f"Error parsing URL {href}: {str(e)}")
    
    def closed(self, reason):
        self.logger.info(f"Spider closed for {", ".join(self.allowed_domains)}")