import logging
import os
import sys
from datetime import datetime, timedelta
from time import sleep
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,generate_blob_sas, BlobSasPermissions

#Copy blob from source container to destination container
def copy_blob(src_url, dest_blb_srv,dest_container_name,dest_blob):
    dest_container_client = dest_blb_srv.get_container_client(dest_container_name)
    if(not dest_container_client.exists()):
        dest_container_client.create_container()
        logging.info('dest container not exist, create container %s',dest_container_name) 
    dest_blob_client = dest_blb_srv.get_blob_client(dest_container_name, dest_blob)
    try:
        copy = dest_blob_client.start_copy_from_url(src_url)
        dest_lease = dest_blob_client.acquire_lease() 
        while( dest_blob_client.get_blob_properties().copy.status == 'pending'):
            logging.info('copy status is  pending')
            sleep(2)
        logging.info('copy status is  %s',dest_blob_client.get_blob_properties().copy.status)
    finally:
        dest_lease.release()