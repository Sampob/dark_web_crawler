from app.config import Config

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient

def get_blob_service_client() -> BlobServiceClient:
    # POC connection
    connect_str = Config.AZURE_CONNECTION_STRING

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    return blob_service_client

    # With service user
    account_url = "https://<>.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    return blob_service_client

def get_table_service_client() -> TableServiceClient:
    connect_str = Config.AZURE_CONNECTION_STRING

    table_service_client = TableServiceClient.from_connection_string(connect_str)
    
    return table_service_client