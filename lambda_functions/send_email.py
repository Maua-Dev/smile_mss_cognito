
import os

FRONT_ENDPOINT = os.environ['FRONT_ENDPOINT']
API_ENDPOINT = os.environ['API_ENDPOINT']


def lambda_handler(event, context):
    user = event['request']['userAttributes']
    email = user['email']
    name = user["custom:socialName"].split(' ')[0] if user.get("custom:socialName") is not None else user['name'].split(' ')[0]
    code = event['request']['codeParameter']

    if event['triggerSource'] == 'CustomMessage_SignUp' or event['triggerSource'] == "CustomMessage_ResendCode":


        message = f"""Olá, {name}!<br> <br>
                    
                    Falta só mais um passo para você se cadastrar na SMILE 2023! <br> <br>
               
                    Para confirmar seu cadastro na SMILE 2023 clique:
                    
                    <br> <br> 
                     <a id="link-confirmar-usuario" href="{API_ENDPOINT}/confirm-user-creation?confirmation_code={code}&email={email}" style="background-color: orange; color: white; padding: 10px;">Confirmar inscrição!</a>
                    <br> <br> 
    
                    Atenciosamente, <br> <br>
    
                    Equipe SMILE 2023"""

        event["response"]["emailMessage"] = message
        event["response"]["emailSubject"] = 'Código de confirmação - SMILE 2023'

    if event['triggerSource'] == 'CustomMessage_ForgotPassword':
        email_before_at = email.split('@')[0]
        email_provider = email.split('@')[1]

        message = f"""Olá, {name}<br> <br>
    
                    Para criar uma nova senha em seu cadastro da SMILE 2023 clique:
    
                     <br> <br> 
                     <a id="link-confirmar-usuario" href="{FRONT_ENDPOINT}/#/login/esqueci-minha-senha/escolher-senha?code={code}&email={email_before_at}&emailProvider={email_provider}" style="background-color: orange; color: white; padding: 10px;">Recuperar senha</a>
                    <br> <br> 
    
                    Atenciosamente, <br> <br>
    
                    Equipe SMILE 2023"""

        event["response"]["emailMessage"] = message
        event["response"]["emailSubject"] = 'Criar nova senha - SMILE 2023'


    print(event)
    return event
