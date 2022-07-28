import logging
import azure.functions as func
import os



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    srcConnStr = os.environ["srcConnStr"]
    src_con = req.params.get('srcCon')
    dst_con = req.params.get('dstCon')
    src_conn_str = req.params.get('srcConnStr')
    dst_conn_str = req.params.get('srcConnStr')
    
    if not src_con or dst_con or src_conn_str or dst_conn_str:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            src_con = req_body.get('srcCon')
            dst_con = req_body.get('dstCon')
            src_conn_str = req_body.get('srcConnStr')
            dst_conn_str = req_body.get('srcConnStr')
    return func.HttpResponse(f"{src_con,dst_con,src_conn_str,dst_conn_str}")
