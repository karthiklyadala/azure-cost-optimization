import os
import json
import gzip
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

COSMOS_URI = os.environ['COSMOS_URI']
COSMOS_KEY = os.environ['COSMOS_KEY']
DATABASE = os.environ['COSMOS_DB']
CONTAINER = os.environ['COSMOS_CONTAINER']

BLOB_CONN_STR = os.environ['BLOB_CONN_STR']
BLOB_CONTAINER = os.environ['BLOB_CONTAINER']

def main(mytimer):
    threshold = (datetime.utcnow() - timedelta(days=90)).isoformat()

    cosmos_client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
    container = cosmos_client.get_database_client(DATABASE).get_container_client(CONTAINER)

    blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    blob_container = blob_service.get_container_client(BLOB_CONTAINER)

    query = "SELECT * FROM c WHERE c.timestamp < @threshold"
    parameters = [{"name": "@threshold", "value": threshold}]
    
    for item in container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True):
        blob_name = f"{item['id']}.json.gz"
        compressed = gzip.compress(json.dumps(item).encode('utf-8'))
        blob_container.upload_blob(blob_name, compressed, overwrite=True)
        container.delete_item(item['id'], partition_key=item['partitionKey'])
