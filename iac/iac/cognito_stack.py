import os

from aws_cdk import (
    aws_cognito, RemovalPolicy,
    aws_lambda as lambda_,
    Duration, CfnOutput
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration


class CognitoStack(Construct):
    user_pool: aws_cognito.UserPool
    client: aws_cognito.UserPoolClient

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.email = aws_cognito.UserPoolEmail.with_ses(
            ses_region=os.environ.get("SES_EMAIL"),
            from_email=os.environ.get("FROM_EMAIL"),
            reply_to=os.environ.get("REPLY_TO_EMAIL"),
        )

        self.github_ref = os.environ.get("GITHUB_REF")

        REMOVAL_POLICY = RemovalPolicy.RETAIN if 'prod' in self.github_ref else RemovalPolicy.DESTROY

        self.user_pool = aws_cognito.UserPool(self, "smile_user_pool",
                                         removal_policy=REMOVAL_POLICY,
                                         self_sign_up_enabled=True,
                                         auto_verify=aws_cognito.AutoVerifiedAttrs(email=True),
                                         user_verification=aws_cognito.UserVerificationConfig(
                                             email_subject="Verifique seu email para acessar o portal Smile",
                                             email_body="Olá, obrigado por se inscrever na Semana Mauá de Inovação Liderança e Empreendedorismo, seu código de confirmação é {####}",
                                             email_style=aws_cognito.VerificationEmailStyle.CODE),
                                         standard_attributes=aws_cognito.StandardAttributes(
                                             fullname=aws_cognito.StandardAttribute(
                                                 required=True,
                                                 mutable=True
                                             ),
                                             email=aws_cognito.StandardAttribute(
                                                 required=True,
                                                 mutable=True
                                             )),
                                         custom_attributes={
                                             "accessLevel": aws_cognito.StringAttribute(min_len=1, max_len=2048, mutable=True),
                                             "userType": aws_cognito.StringAttribute(min_len=1, max_len=2048, mutable=True),
                                             "certWithSocialName": aws_cognito.BooleanAttribute(mutable=True),
                                             "ra": aws_cognito.StringAttribute(min_len=1, max_len=2048, mutable=False),
                                             "role": aws_cognito.StringAttribute(min_len=1, max_len=2048, mutable=True),
                                             "socialName": aws_cognito.StringAttribute(min_len=1, max_len=2048, mutable=True),
                                             "acceptedTerms": aws_cognito.BooleanAttribute(mutable=True),
                                             "acceptedNotificSMS": aws_cognito.BooleanAttribute(mutable=True),
                                             "acceptedNotificMail": aws_cognito.BooleanAttribute(mutable=True),
                                         },
                                        email=self.email
                                        )


        self.client = self.user_pool.add_client("smile_user_pool_client",
                             user_pool_client_name="smile_user_pool_client",
                             generate_secret=False,
                             auth_flows=aws_cognito.AuthFlow(
                                 admin_user_password=True,
                                 user_password=True,
                                 user_srp=True
                             )
                             )

        CfnOutput(self, 'CognitoRemovalPolicy',
                  value=REMOVAL_POLICY.value,
                  export_name='CognitoRemovalPolicyValue')

