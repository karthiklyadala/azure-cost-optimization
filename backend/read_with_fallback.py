import gzip
import json
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

COSMOS_URI = "your-cosmos-uri"
COSMOS_KEY = "your-cosmos-key"
DATABASE = "your-database"
CONTAINER = "your-container"
BLOB_CONN_STR = "your-blob-conn-str"
BLOB_CONTAINER = "archived-billing"

def get_billing_record(record_id, partition_key):
    try:
        cosmos_client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
        container = cosmos_client.get_database_client(DATABASE).get_container_client(CONTAINER)
        return container.read_item(record_id, partition_key)
    except exceptions.CosmosResourceNotFoundError:
        blob_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
        blob_container = blob_client.get_container_client(BLOB_CONTAINER)
        blob = blob_container.get_blob_client(f"{record_id}.json.gz")
        blob_data = blob.download_blob().readall()
        return json.loads(gzip.decompress(blob_data).decode("utf-8"))
