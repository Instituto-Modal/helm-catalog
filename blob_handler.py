from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import uuid
import os

from azure.storage.blob import BlobClient

storageConnectionString = "DefaultEndpointsProtocol=https;AccountName=stgiajuridico;AccountKey=vuyHV9B5Z0uXfMR1jQjPmqHEukRTo7wkaIvpZtyPJAwae9t250spf2wwXhRnePgOUDKmo4SNMgRl+AStCMipRw==;EndpointSuffix=core.windows.net"

# Retrieve the connection string from an environment variable. Note that a
# connection string grants all permissions to the caller, making it less
# secure than obtaining a BlobClient object using credentials.
conn_string = storageConnectionString

# Create the client object for the resource identified by the connection
# string, indicating also the blob container and the name of the specific
# blob we want.
blob_client = BlobClient.from_connection_string(
    conn_string,
    container_name="stgblob-iajuridico",
    blob_name=f"Arquitetura_COBII_Parcial.pdf",
)

props = blob_client.get_blob_properties()

print(props)
