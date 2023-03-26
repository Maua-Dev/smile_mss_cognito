import os

import boto3


def addEnviromentVariable(api_endpoint: str, function_name: str):
    boto3.client('lambda').update_function_configuration(
        FunctionName=function_name,
        Environment={
            'Variables': {
                    'API_ENDPOINT': f"{api_endpoint}",
                    'FROM_EMAIL': os.environ.get("FROM_EMAIL"),
                    'FRONT_ENDPOINT': os.environ.get("FRONT_ENDPOINT"),
            }
        },
    )


if __name__ == '__main__':

    cloudformation_client = boto3.client('cloudformation')

    stack_name = os.environ.get("STACK_NAME")

    stack_outputs = cloudformation_client.describe_stacks(StackName=stack_name)['Stacks'][0]['Outputs']

    api_endpoint = [output['OutputValue'] for output in stack_outputs if output.get("ExportName") == 'AuthRestApiUrlValue'][0]

    function_name = [output['OutputValue'] for output in stack_outputs if output.get("ExportName") == 'CustomMessageFunctionValue'][0]

    addEnviromentVariable(api_endpoint, function_name)
