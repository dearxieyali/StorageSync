import logging
import os
import sys
from datetime import datetime, timedelta
from time import sleep
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,generate_blob_sas, BlobSasPermissions
from Common import util

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
    srcBlobSas = generate_blob_sas(account_name=srcBlbClt.account_name, 
                                container_name=container_name,
                                blob_name=blob_name,
                                account_key=source_account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.utcnow() + timedelta(hours=2))
    source_blob_url= srcBlbClt.url + "?" + srcBlobSas
    logging.debug('source blob SAS_URL is  %s', source_blob_url)
    util.copy_blob(src_url = source_blob_url, dest_blb_srv = dstBlbSrvClt, 
                   dest_container_name = dest_container_name,dest_blob = blob_name)
        
'''TODO:
    1 Adding time and progress bar for copying file
'''
    
        