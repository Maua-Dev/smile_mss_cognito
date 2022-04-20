
import os

USER_POOL_ID = os.environ['USER_POOL_ID']
FRONT_ENDPOINT = os.environ['FRONT_ENDPOINT']
API_ENDPOINT = os.environ['API_ENDPOINT']

def lambda_handler(event, context):
    if event['userPoolId'] == USER_POOL_ID:
        # ================ FORGOT PASSWORD ================================
        if event['triggerSource'] == 'CustomMessage_ForgotPassword':
            login = event['request']['clientMetadata']['login']
            email = login.split('@')[0] if '@' in login else login
            emailProvider = login.split('@')[1] if '@' in login else ''

            code = event['request']['codeParameter']

            message = f"""Olá, <br> <br>

            Para criar uma nova senha em seu cadastro da SMILE 2022 clique no link: <a id="botao-recuperar-senha" href="{FRONT_ENDPOINT}/#/login/esqueci-minha-senha/escolher-senha?code={code}&email={email}&emailProvider={emailProvider}">Recuperar senha</a>
                                                                                     
               
            <br> <br> 

            Atenciosamente, <br> <br>

            Equipe SMILE 2022"""


            event["response"]["emailMessage"] = message
            event["response"]["emailSubject"] = 'Código de confirmação - SMILE 2022'

        # ================================================================

        # ================ SIGN UP =======================================

        if event['triggerSource'] == 'CustomMessage_SignUp':
            code = event['request']['codeParameter']
            subId = event['request']['userAttributes']['sub']

            message = f"""Olá, <br> <br>

            Para confirmar seu cadastro na SMILE 2022 clique no link: <a id="link-confirmar-usuario" href="{API_ENDPOINT}/confirmUserCreation?login={subId}&code={code}">confirmar usuário</a>
            <br> <br> 

            Atenciosamente, <br> <br>

            Equipe SMILE 2022"""

            event["response"]["emailMessage"] = message
            event["response"]["emailSubject"] = 'Código de confirmação - SMILE 2022'


        # ================================================================
    print(event)
    return event
