import boto3, json, time
from sagemaker.jumpstart.notebook_utils import list_jumpstart_models
from pprint import pprint

def list_endpoints(): 
    print("listing sagemaker endpoints")
    sagemaker_client = boto3.client('sagemaker')
    response = sagemaker_client.list_endpoints()
    # pprint(response)
    for e in response['Endpoints']:
        endpoint = sagemaker_client.describe_endpoint(EndpointName=e['EndpointName'])
        # endpoint_config = sagemaker_client.describe_endpoint_config(EndpointConfigName=endpoint['EndpointConfigName'])
        print(f'[{e["EndpointStatus"]}] - {e["EndpointName"]}')

def list_jumpstart_models(filter_value="textembedding"):
    # filter_value = "task == textgeneration1"
    print("listing jumpstart models with filter value: ", filter_value)
    jumpstart_models = list_jumpstart_models(filter=filter_value)
    for m in jumpstart_models:
        print(m)

