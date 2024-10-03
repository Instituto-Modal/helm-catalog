import logging
import requests
import json
import re
import os
import azure.functions as func

from pypomes_http import http_post
from modal_core_python import init_modal, AUTH_JWT_BASE_SCHEME
from pypomes_logging import PYPOMES_LOGGER


app = func.FunctionApp()

@app.function_name(name="FunctionTopicUploadDiarios")
@app.service_bus_topic_trigger(arg_name="message", 
                               topic_name="upload-diarios", 
                               connection="ServiceBusConnectionString", 
                               subscription_name="svcbus-subscription-topic-upload-diarios")
def test_function(message: func.ServiceBusMessage):
    message_body_txt = message.get_body().decode("utf-8")
#    logging.warn("Message Body: " + message_body_txt)
    message_body = json.loads(message_body_txt)
    evtType = message_body['eventType']
    logging.warn("EvtType: "+evtType)
    if 'BlobCreated' not in evtType:
        return
    line = message_body['data']['url']
    vsplit = line.split('/')
    fname = vsplit[-1]
    logging.warn("Triggered ---> "+fname)
    tribunal = vsplit[5]
    pattern = r"\d{4}-\d{2}-\d{2}"
    matcher = re.search(pattern, fname)
    data_diario = None
    if matcher:
        data_diario = matcher.group()
    caminho_arquivo = line[len(os.getenv("URL_BLOB_STORAGE"))+1:]
    op = 'none'
    params = {'tribunal':tribunal,
        'data-diario':data_diario,
        'caminho-arquivo':caminho_arquivo}
    if 'ORIGINAL' in line:
        post_url = os.getenv("URL_EXTRATOR")
        op = 'invocar-extrator'
    else:
        post_url = os.getenv("URL_EXPEDIENTE")
        op = 'persistir-expediente'
    
    logging.warn('acao: '+op+'/Url['+post_url+'] params: '+str(params))

    op_errors: list[str] = []
    response: requests.Response = http_post(errors=op_errors, url=post_url, data=post_data,
          auth=AUTH_JWT_BASE_SCHEME,
          timeout=600, logger=PYPOMES_LOGGER)

#    resp = requests.post(url = url, data = params)
    logging.warn('status: '+str(response.status_code)+' content: ['+response.text+']')

def main():
    message_body = {"topic":"/subscriptions/7610c488-0969-41e0-9bf9-b40a5ea64854/resourceGroups/rg-iajuridico/providers/Microsoft.Storage/storageAccounts/stgiajuridico","subject":"/blobServices/default/containers/stgblob-iajuridico/blobs/ORIGINAL/TRT9/2022/01/TRT9-2022-01-03.pdf","eventType":"Microsoft.Storage.BlobCreated","id":"fda684ab-b01e-00a4-07c8-b2520c06b2b9","data":{"api":"PutBlob","clientRequestId":"f4390a73-20d6-4fc2-bf93-466ed505b00d","requestId":"fda684ab-b01e-00a4-07c8-b2520c000000","eTag":"0x8DB80DFE8731572","contentType":"application/json","contentLength":3727,"blobType":"BlockBlob","url":"https://stgiajuridico.blob.core.windows.net/stgblob-iajuridico/ORIGINAL/TRT9/2022/01/TRT9-2022-01-03.pdf","sequencer":"0000000000000000000000000000689D00000000005ba9c4","storageDiagnostics":{"batchId":"fbf06b75-f006-009a-00c8-b2c573000000"}},"dataVersion":"","metadataVersion":"1","eventTime":"2023-07-10T00:52:16.8985725Z"}

if __name__ == "__main__":
    main()

