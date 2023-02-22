import os

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam
)
from constructs import Construct

# from .lambda_stack import LambdaStack
from aws_cdk.aws_apigateway import RestApi, Cors

from .cognito_stack import CognitoStack
from .lambda_stack import LambdaStack



class IacStack(Stack):

    front_endpoint = os.environ.get('FRONT_ENDPOINT')
    rest_api_url = os.environ.get('API_ENDPOINT')

    # lambda_stack: LambdaStack

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.rest_api = RestApi(self, "smile_auth_rest_api",
                                rest_api_name="Smile_Cognito_RestApi",
                                description="This is the Smile RestApi",
                                default_cors_preflight_options=
                                {
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                )

        self.cognito_stack = CognitoStack(self, "smile_cognito_stack", api_endpoint=self.rest_api_url, front_endpoint=self.front_endpoint)

        api_gateway_resource = self.rest_api.root.add_resource("mss-cognito", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
                                                               )

        ENVIRONMENT_VARIABLES = {
            "STAGE": "DEV",
            "USER_POOL_ID": self.cognito_stack.user_pool.user_pool_id,
            "CLIENT_ID": self.cognito_stack.client.user_pool_client_id,
            "REGION": self.region,
            "FRONT_ENDPOINT": self.front_endpoint,
        }

        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        cognito_admin_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=[
                "cognito-idp:*",
            ],
            resources=[
                self.cognito_stack.user_pool.user_pool_arn,
            ]
        )

        for f in self.lambda_stack.functions_that_need_cognito_permissions:
            f.add_to_role_policy(cognito_admin_policy)
