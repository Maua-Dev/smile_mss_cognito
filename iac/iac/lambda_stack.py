
import os
from aws_cdk import (
    aws_lambda as lambda_,
    NestedStack, Duration
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration



class LambdaStack(Construct):

    functions_that_need_cognito_permissions = []
    def createLambdaApiGatewayIntegration(self, module_name: str, method: str, mss_student_api_resource: Resource, environment_variables: dict = {"STAGE": "TEST"}):
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            memory_size=512,
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer, self.lambda_power_tools],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        mss_student_api_resource.add_resource(module_name.replace("_", "-")).add_method(method,
                                                                                        integration=LambdaIntegration(
                                                                                            function))

        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict) -> None:
        super().__init__(scope, "Smile_Auth_Lambdas")

        self.lambda_layer = lambda_.LayerVersion(self, "Smile_Auth_Layer",
                                                 code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                 )

        self.lambda_power_tools = lambda_.LayerVersion.from_layer_version_arn(self, "Lambda_Power_Tools", layer_version_arn=f"arn:aws:lambda:{os.environ.get('AWS_REGION')}:017000801446:layer:AWSLambdaPowertoolsPythonV2:22")

        self.change_password_function = self.createLambdaApiGatewayIntegration(
            module_name="change_password",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        self.check_token_function = self.createLambdaApiGatewayIntegration(
            module_name="check_token",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        self.confirm_change_password_function = self.createLambdaApiGatewayIntegration(
            module_name="confirm_change_password",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        self.confirm_user_creation_function = self.createLambdaApiGatewayIntegration(
            module_name="confirm_user_creation",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        self.create_user_function = self.createLambdaApiGatewayIntegration(
            module_name="create_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        # self.delete_user_function = self.createLambdaApiGatewayIntegration(
        #     module_name="delete_user",
        #     method="POST",
        #     mss_student_api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        #
        # )
        self.get_user_function = self.createLambdaApiGatewayIntegration(
            module_name="get_user",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        # self.list_users_function = self.createLambdaApiGatewayIntegration(
        #     module_name="list_users",
        #     method="GET",
        #     mss_student_api_resource=api_gateway_resource,
        #     environment_variables=environment_variables
        #
        # )
        self.login_user_function = self.createLambdaApiGatewayIntegration(
            module_name="login_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        self.refresh_token_function = self.createLambdaApiGatewayIntegration(
            module_name="refresh_token",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )
        self.resend_creation_confirmation_function = self.createLambdaApiGatewayIntegration(
            module_name="resend_creation_confirmation",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables

        )

        self.list_professors_function = self.createLambdaApiGatewayIntegration(
            module_name="list_professors",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.update_user_function = self.createLambdaApiGatewayIntegration(
            module_name="update_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables
        )

        self.functions_that_need_cognito_permissions = [
            self.change_password_function,
            self.check_token_function,
            self.confirm_change_password_function,
            self.confirm_user_creation_function,
            self.create_user_function,
            # self.delete_user_function,
            self.get_user_function,
            # self.list_users_function,
            self.login_user_function,
            self.refresh_token_function,
            self.resend_creation_confirmation_function,
            self.list_professors_function,
            self.update_user_function
        ]
