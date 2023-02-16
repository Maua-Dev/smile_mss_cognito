
import os

FRONT_ENDPOINT = os.environ['FRONT_ENDPOINT']
API_ENDPOINT = os.environ['API_ENDPOINT']


def lambda_handler(event, context):

    if event['triggerSource'] == 'CustomMessage_SignUp' or event['triggerSource'] == "CustomMessage_ResendCode":
        user = event['request']['userAttributes']
        email = user['email']
        name = user['name'].split(' ')[0]
        code = event['request']['codeParameter']

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

    print(event)
    return event
