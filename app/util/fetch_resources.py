from app.util.azure_storage_account import get_blob_service_client

import json

from azure.storage.blob import BlobServiceClient

def fetch_crawl_urls(client: BlobServiceClient = None) -> list:
    if not client:
        service_client = get_blob_service_client()
    else:
        service_client = client
    
    # TODO: Dynamic resource fetching
    container_name = "dark-web-crawler-poc"
    resource_name = "craw-urls.txt"

    container_client = service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(resource_name)
    
    blob_data = blob_client.download_blob()
    content = blob_data.readall()

    decoded_content = content.decode("utf-8")
    content_list = decoded_content.split("\r\n")
    return content_list

def fetch_regex_patterns(client: BlobServiceClient = None) -> dict:
    if not client:
        service_client = get_blob_service_client()
    else:
        service_client = client
    
    # TODO: Dynamic resource fetching
    container_name = "dark-web-crawler-poc"
    resource_name = "regex-patterns.json"
    container_client = service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(resource_name)
    
    blob_data = blob_client.download_blob()
    content = blob_data.readall()

    decoded_content = content.decode("utf-8")
    content_dict = json.loads(decoded_content)
    return content_dict