import os

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam, aws_cognito,
    aws_apigateway as api_gateway,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_lambda as lambda_, Duration,
    CfnOutput
)
from constructs import Construct

# from .lambda_stack import LambdaStack
from aws_cdk.aws_apigateway import RestApi, Cors

from .cognito_stack import CognitoStack
from .lambda_stack import LambdaStack



class IacStack(Stack):

    front_endpoint = os.environ.get('FRONT_ENDPOINT')
    github_ref = os.environ.get("GITHUB_REF")


    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.mss_name = os.environ.get("MSS_NAME")

        self.rest_api = RestApi(self, f"smile_auth_rest_api_{self.github_ref}",
                                rest_api_name="Smile_Cognito_RestApi",
                                description="This is the Smile RestApi",
                                default_cors_preflight_options=
                                {
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                )

        self.cognito_stack = CognitoStack(self, f"smile_cognito_stack_{self.github_ref}")

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
            "MSS_NAME": self.mss_name
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

        custom_message_function = lambda_.Function(
            self, "pre_sign_up-smile-cognito",
            code=lambda_.Code.from_asset(f"../lambda_functions"),
            memory_size=512,
            handler=f"send_email.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(15),
        )

        self.cognito_stack.user_pool.add_trigger(
            aws_cognito.UserPoolOperation.CUSTOM_MESSAGE,
            custom_message_function
        )

        CfnOutput(self,
                  f"AuthRestApiUrl-{self.github_ref}",
                  value=f"{self.rest_api.url}mss-cognito",
                  export_name=f"AuthRestApiUrlValue")

        CfnOutput(self,
                  f"CustomMessageFunction-{self.github_ref}",
                    value=custom_message_function.function_name,
                    export_name=f"CustomMessageFunctionValue")
