from aws_cdk import (
    aws_cognito
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class CognitoStack(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_pool = aws_cognito.UserPool(self, "smile_user_pool",
                                         user_pool_name="smile_user_pool",
                                         self_sign_up_enabled=True,
                                         auto_verify=aws_cognito.AutoVerifiedAttrs(email=True),
                                         user_verification=aws_cognito.UserVerificationConfig(
                                             email_subject="Verify your email for our awesome app",
                                             email_body="Hello {username}, Thanks for signing up to our awesome app! Your verification code is {####}",
                                             email_style=aws_cognito.VerificationEmailStyle.CODE),
                                         standard_attributes=aws_cognito.StandardAttributes(
                                             fullname=aws_cognito.StandardAttribute(
                                                 required=True,
                                                 mutable=False
                                             ),
                                             email=aws_cognito.StandardAttribute(
                                                 required=True,
                                                 mutable=True
                                             )),
                                         custom_attributes={
                                             "accessLevel": aws_cognito.StringAttribute(min_len=1, max_len=2048),
                                             "userType": aws_cognito.StringAttribute(min_len=1, max_len=2048),
                                             "certWithSocialName": aws_cognito.BooleanAttribute(),
                                             "ra": aws_cognito.StringAttribute(min_len=1, max_len=2048),
                                             "role": aws_cognito.StringAttribute(min_len=1, max_len=2048),
                                             "socialName": aws_cognito.StringAttribute(min_len=1, max_len=2048),
                                         }
                                         )

        user_pool.add_client("smile_user_pool_client",
                             user_pool_client_name="smile_user_pool_client",
                             generate_secret=False,
                             auth_flows=aws_cognito.AuthFlow(
                                 admin_user_password=True,
                                 user_password=True,
                                 user_srp=True
                             )
                             )
