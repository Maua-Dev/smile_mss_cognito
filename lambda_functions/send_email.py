import os

FRONT_ENDPOINT = os.environ['FRONT_ENDPOINT']
API_ENDPOINT = os.environ['API_ENDPOINT']


def lambda_handler(event, context):
    user = event['request']['userAttributes']
    email = user['email']
    name = user["custom:socialName"].split(' ')[0] if user.get("custom:socialName") is not None else user['name'].split(' ')[0]
    code = event['request']['codeParameter']

    if event['triggerSource'] == 'CustomMessage_SignUp' or event['triggerSource'] == "CustomMessage_ResendCode":

        message = """
                <html>
                <p>Olá, <strong>{name}</strong>!</p>


                <p>Falta só mais um passo para você se cadastrar na SMILE 2023!</p>
                <p>&nbsp;</p>
                <p>Para confirmar seu cadastro na SMILE 2023 clique:</p>

                <a href="{API_ENDPOINT}/confirm-user-creation?confirmation_code={code}&amp;email={email}" target="_blank">Confirmar inscrição!</a>
                
                <p>Atenciosamente,</p>
                <p>&nbsp;</p>
                <p><strong>Equipe SMILE 2023</strong></p>

                </html>

                """

        message = message.format(name=name, code=code, email=email, API_ENDPOINT=API_ENDPOINT)

        event["response"]["emailMessage"] = message
        event["response"]["emailSubject"] = 'Confirme seu cadastro - SMILE 2023'

    if event['triggerSource'] == 'CustomMessage_ForgotPassword':
        email_before_at = email.split('@')[0]
        email_provider = email.split('@')[1]

        message = """
                <html>
                <p>Olá, <strong>{name}</strong>!</p>

                <p>Você solicitou troca de senha, se não foi você, apenas ignore esta mensagem</p>
                <p>&nbsp;</p>
                <p>Para criar uma nova senha em seu cadastro da SMILE 2023 clique:</p>

                <a href="{FRONT_ENDPOINT}/#/login/esqueci-minha-senha/escolher-senha?code={code}&email={email_before_at}&emailProvider={email_provider}" target="_blank">Recuperar senha</a>

                <p>Atenciosamente,</p>
                <p>&nbsp;</p>
                <p><strong>Equipe SMILE 2023</strong></p>

                </html>

                """

        message = message.format(name=name, FRONT_ENDPOINT=FRONT_ENDPOINT, code=code, email_before_at=email_before_at, email_provider=email_provider)

        event["response"]["emailMessage"] = message
        event["response"]["emailSubject"] = 'Criar nova senha - SMILE 2023'


    print(event)
    return event
