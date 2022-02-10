import logging
import os
import sys
from datetime import datetime, timedelta
from time import sleep
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,generate_blob_sas, BlobSasPermissions
import
srcConnStr = os.environ["srcConnStr"]
source_account_key = os.environ["source_account_key"]
source_account_name = os.environ["source_account_name"]
dstConnStr = os.environ["dstConnStr"]
dest_account_key = os.environ["dest_account_key"]
dest_account_name = os.environ["dest_account_name"]
dest_container_name = os.environ["dest_container_name"]

srcBlbSrvClt = BlobServiceClient.from_connection_string(srcConnStr)
dstBlbSrvClt = BlobServiceClient.from_connection_string(dstConnStr)


def main(myblob: func.InputStream):
    logging.info('Blob trigger function processed %s', myblob.name)

    
    [container_name,blob_name] = myblob.name.split('/',1)
    srcBlbClt = srcBlbSrvClt.get_blob_client(container_name, blob_name)
    srcBlobSas = generate_blob_sas(account_name=source_account_name, 
                                container_name=container_name,
                                blob_name=blob_name,
                                account_key=source_account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.utcnow() + timedelta(hours=2))
    source_blob_url= srcBlbClt.url + "?" + srcBlobSas
    logging.debug('source blob SAS_URL is  %s', source_blob_url)
    
    dest_container_client = dstBlbSrvClt.get_container_client(dest_container_name)
    if(not dest_container_client.exists()):
        dest_container_client.create_container()
        logging.info('dest container not exist, create container %s',dest_container_name)
    
    dest_blob_client = dstBlbSrvClt.get_blob_client(dest_container_name, blob_name)
    source_lease = srcBlbClt.acquire_lease()
    try:
        copy = dest_blob_client.start_copy_from_url(source_url = source_blob_url,
                        source_lease = source_lease)
        dest_lease = dest_blob_client.acquire_lease() 
        while( dest_blob_client.get_blob_properties().copy.status == 'pending'):
            logging.info('copy status is  pending')
            sleep(2)
        logging.info('copy status is  %s',dest_blob_client.get_blob_properties().copy.status)
    finally:
        source_lease.release()
        dest_lease.release()
        
'''TODO:
    rebuild the code , common function 
    put it to github'''
    
        