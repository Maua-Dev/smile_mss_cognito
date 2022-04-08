
import os

USER_POOL_ID = os.environ['USER_POOL_ID']
FRONT_ENDPOINT = os.environ['FRONT_ENDPOINT']
API_ENDPOINT = os.environ['API_ENDPOINT']

def lambda_handler(event, context):
    if event['userPoolId'] == USER_POOL_ID:
        # ================ FORGOT PASSWORD ================================
        if event['triggerSource'] == 'CustomMessage_ForgotPassword':
            login = event['request']['clientMetadata']['login']
            code = event['request']['codeParameter']

            message = f"""
            <!DOCTYPE html>
            <html lang="en" style="font-family: Roboto; text-decoration: none; margin: 0;">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Recuperação de senha</title>
            <style>body {{
            padding: 30px;
            }}
            @media screen and (min-width:800px) {{
              #titulo-email {{
                font-size: 80px;
              }}
              #corpo-email {{
                font-size: 40px;
              }}
            }}
            </style>
            </head>
            
            <body style="font-family: Roboto; text-decoration: none; margin: 0; padding: 30px;">
                <h1 id="titulo-email" style="font-family: Roboto; text-decoration: none; font-weight: 900; font-size: 10; margin: 0 0 10px;">Esqueceu a sua senha da Smile?</h1>
                <p id="corpo-email" style="font-family: Roboto; text-decoration: none; font-weight: 400; font-size: 5; margin: 0 0 50px;">É rápido! Você apenas precisa clicar no botão abaixo:</p>
                <a id="botao-recuperar-senha" href="{FRONT_ENDPOINT}/#/login/esqueci-minha-senha?login={login}&code={code}" style="font-family: Roboto; text-decoration: none; background-color: #004680; border-radius: 30px; color: #FFF; font-weight: 700; margin: 50px 0 0; padding: 20px;">Recuperar senha</a> 
                <br>
                <footer style="font-family: Roboto; text-decoration: none; background-color: #004680; width: 100vw; align-items: center; display: flex; justify-content: center; gap: 30px; margin: 100px 0 0 -30px; padding: 30px;">
                    <img src="http://smile2022-frontend-assets.s3.sa-east-1.amazonaws.com/logo_smileee.png" style="font-family: Roboto; text-decoration: none; margin: 0;">
                    <img src="http://smile2022-frontend-assets.s3.sa-east-1.amazonaws.com/Logo+Dev+Maua.png" style="font-family: Roboto; text-decoration: none; margin: 0;">
                </footer>
            
            </body>
            </html>

            """

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
