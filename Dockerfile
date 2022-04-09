FROM  amazon/aws-lambda-python:3.9

EXPOSE 8080


COPY app_lambda_dir/ ${LAMBDA_TASK_ROOT}


CMD [ "lambda.lambda_handler" ]

