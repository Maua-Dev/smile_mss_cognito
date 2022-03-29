

import os

USER_POOL_ID = os.environ['USER_POOL_ID']




def lambda_handler(event, context):
    if event['userPoolId'] == USER_POOL_ID:
        if event['triggerSource'] == 'CustomMessage_ForgotPassword':
            login = event['request']['clientMetadata']['login']
            endpoint = event['request']['clientMetadata']['endpoint']
            code = event['request']['codeParameter']

            message = f"""Olá,
            
            Para confirmar sua solicitação feita para SMILE 2022 clique no link: <a href="{endpoint}?login={login}&code={code}">aqui</a> 
                
            Atenciosamente,
            
            Equipe SMILE 2022"""

            event["response"]["emailMessage"] = message
            event["response"]["emailSubject"] = 'Código de confirmação - SMILE 2022'

    return event
