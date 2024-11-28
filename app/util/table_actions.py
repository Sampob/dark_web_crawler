from app.util.azure_storage_account import get_table_service_client

from azure.core.exceptions import ResourceNotFoundError

def send_to_table(data: dict, table_name: str = "CrawlResults"):
    table_service_client = get_table_service_client()
    try:
        table_client = table_service_client.get_table_client(table_name)
        table_client.create_entity(entity=data)
    except ResourceNotFoundError:
        table_client = table_service_client.create_table(table_name)
        table_client.create_entity(entity=data)
    except Exception as e:
        # TODO: Logger util
        print(e)
        raise e