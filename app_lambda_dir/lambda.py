from app_lambda import LambdaApp


app = LambdaApp()

@app.get(path='/hi')
def hello():
    return {'body': 'Hello World!', 'status_code': 400}

@app.get(path='/hello')
def hellow():
    return 'vai!'

def lambda_handler(event, context):
    return app(event, context)

event = {'rawPath': '/hello'}
context = "LambdaContext([aws_request_id=0ad17140-124d-40ad-9667-5aa7a4257c97,log_group_name=/aws/lambda/Functions,log_stream_name=$LATEST,function_name=test_function,memory_limit_in_mb=3008,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:us-east-1:012345678912:function:test_function,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])"


print(lambda_handler(event, context))
