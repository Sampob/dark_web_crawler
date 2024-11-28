# Dark web crawler

Python framework Scrapy based web crawler. Follows links in an attempt to find matches to regex patterns. 

Saves results to JSON format. 

Runs using docker-compose. Configure `docker-compose.yaml` and deploy. 


```
~# docker compose build
~# docker compose up
```

Features:
- Random user-agent on each request
- Tor-proxy
    - Each request is done through the tor network
    - Each new crawl gets a new tor IP address
- Scheduling
    - Configure URLs and regex expressions that will be executed daily
- On demand crawl
    - Give URLs and regex expressions to execute a crawl on demand
- Scalable
    - Celery Task Queue
    - Celery Flower to monitor tasks