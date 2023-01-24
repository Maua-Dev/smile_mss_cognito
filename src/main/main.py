import os

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

from src.modules.change_password.app.change_password_controller import ChangePasswordController
from src.modules.check_token.app.check_token_controller import CheckTokenController
from src.adapters.controllers.confirm_change_password_controller import ConfirmChangePasswordController
from src.adapters.controllers.confirm_user_creation_controller import ConfirmUserCreationController
from src.adapters.controllers.create_user_controller import CreateUserController
from src.modules.list_users.app.list_users_controller import ListUsersController
from src.modules.login_user.app.login_user_controller import LoginUserController
from src.modules.refresh_token.app.refresh_token_controller import RefreshTokenController
from src.adapters.controllers.resend_creation_confirmation_controller import ResendCreationConfirmationController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import HttpRequest
from src.main.helpers.status import status
from src.main.users.module import Modular

app = FastAPI()


@app.exception_handler(HttpException)
async def internal_exception_handler(request: Request, exc: HttpException):
    return PlainTextResponse(exc.body, status_code=exc.status_code)


@app.post("/listUsers")
async def listUsers(request: Request, response: Response):
    getAllUsersController = Modular.getInject(ListUsersController)
    body = await request.json()
    req = HttpRequest(body=body, headers=request.headers)
    result = await getAllUsersController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.post("/user")
async def createUser(request: Request, response: Response):
    createUserController = Modular.getInject(CreateUserController)
    req = HttpRequest(body=await request.json())
    result = await createUserController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.get("/confirmUserCreation")
async def confirmUserCreation(request: Request, response: Response):
    confirmUserCreationController = Modular.getInject(
        ConfirmUserCreationController)
    # get query params
    queryData = request.query_params

    body = {
        'login': queryData.get('login'),
        'code': queryData.get('code')
    }
    req = HttpRequest(body=body)
    result = await confirmUserCreationController(req)
    if result.status_code == 200:
        response = RedirectResponse(
            url=f"{os.environ['FRONT_END_ENDPOINT']}/#/login/cadastro/sucesso", status_code=303)
        return response
    if result.status_code == 303:
        response = RedirectResponse(
            url=f"{os.environ['FRONT_END_ENDPOINT']}/#/login/cadastro/sucesso", status_code=303)
        return response
    return Response(status_code=result.status_code, content=result.body)


@app.post("/login")
async def login(request: Request, response: Response):
    loginUserController = Modular.getInject(LoginUserController)

    req = HttpRequest(body=await request.json())
    result = await loginUserController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.get("/checkToken")
async def checkToken(request: Request, response: Response):
    checkTokenController = Modular.getInject(CheckTokenController)
    req = HttpRequest(headers=request.headers)
    result = await checkTokenController(req)

    response.status_code = status.get(result.status_code)
    return result.body


# recebe refresh_token via header e retorna só access_token atualizado
@app.get("/refreshToken")
async def refreshToken(request: Request, response: Response):
    refreshTokenController = Modular.getInject(RefreshTokenController)
    req = HttpRequest(headers=request.headers)
    result = await refreshTokenController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.put("/changePassword")
async def changePassword(request: Request, response: Response):
    changePasswordController = Modular.getInject(ChangePasswordController)

    req = HttpRequest(body=await request.json())
    result = await changePasswordController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.post("/changePassword")
async def confirmChangePassword(request: Request, response: Response):
    confirmChangePasswordController = Modular.getInject(
        ConfirmChangePasswordController)

    req = HttpRequest(body=await request.json())
    result = await confirmChangePasswordController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.put("/user")
async def updateUser(request: Request, response: Response):
    updateUserController = Modular.getInject(UpdateUserController)
    body = await request.json()
    req = HttpRequest(body=body, headers=request.headers)
    result = await updateUserController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.put("/resendCreationConfirmation")
async def resendCreationConfirmation(request: Request, response: Response):
    resendConfirmationEmailController = Modular.getInject(
        ResendCreationConfirmationController)
    body = await request.json()
    req = HttpRequest(body=body)
    result = await resendConfirmationEmailController(req)
    response.status_code = status.get(result.status_code)
    return result.body
