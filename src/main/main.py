from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse

from src.adapters.controllers.change_password_controller import ChangePasswordController
from src.adapters.controllers.check_token_controller import CheckTokenController
from src.adapters.controllers.confirm_change_password_controller import ConfirmChangePasswordController
from src.adapters.controllers.confirm_user_creation_controller import ConfirmUserCreationController
from src.adapters.controllers.create_user_controller import CreateUserController
from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.refresh_token_controller import RefreshTokenController
from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import HttpRequest
from src.main.helpers.status import status
from src.main.users.module import Modular
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HttpException)
async def internal_exception_handler(request: Request, exc: HttpException):
    return PlainTextResponse(exc.body, status_code=exc.status_code)

@app.post("/user")
async def createUser(request: Request, response: Response):
    createUserController = Modular.getInject(CreateUserController)
    req = HttpRequest(body= await request.json())
    result = await createUserController(req)

    response.status_code = status.get(result.status_code)
    return result.body

@app.post("/confirmUserCreation")
async def confirmUserCreation(request: Request, response: Response):
    confirmUserCreationController = Modular.getInject(ConfirmUserCreationController)
    # get form data
    formData = await request.form()
    body = {
        'login': formData.get('login'),
        'code': formData.get('code')
    }
    req = HttpRequest(body=body)
    result = await confirmUserCreationController(req)
    if result.status_code == 200:
        response = RedirectResponse(url=f"{os.environ['FRONT_END_ENDPOINT']}/login/cadastro/", status_code=303)
        return response
    response.status_code = status.get(result.status_code)
    return result.body


@app.post("/login")
async def login(request: Request, response: Response):
    loginUserController = Modular.getInject(LoginUserController)

    req = HttpRequest(body=await request.json())
    result = await loginUserController(req)


    response.status_code = status.get(result.status_code)
    return result.body


@app.get("/checkToken")  #login com access_token
async def checkToken(request: Request, response: Response):
    checkTokenController = Modular.getInject(CheckTokenController)
    req = HttpRequest(headers=request.headers)
    result = await checkTokenController(req)

    response.status_code = status.get(result.status_code)
    return result.body

@app.get("/refreshToken") # recebe refresh_token via header e retorna só access_token atualizado
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
    confirmChangePasswordController = Modular.getInject(ConfirmChangePasswordController)

    req = HttpRequest(body=await request.json())
    result = await confirmChangePasswordController(req)

    response.status_code = status.get(result.status_code)
    return result.body



# @app.get("/user/all")
# async def getAllusers(response: Response):
#     getAllUsersController = Modular.getInject(GetAllUsersController)
#     req = HttpRequest(query=None)
#     result = await getAllUsersController(req)
#
#     response.status_code = status.get(result.status_code)
#     return result.body
#
#
# @app.get("/user/{cpfRne}")
# async def getUser(cpfRne: int, response: Response):
#     getAllUserByCpfRne = Modular.getInject(GetUserByCpfRneController)
#     req = HttpRequest(query={'cpfRne': cpfRne})
#     result = await getAllUserByCpfRne(req)
#
#     response.status_code = status.get(result.status_code)
#     return result.body




# @app.put("/user")
# async def updateUser(request: Request, response: Response):
#     updateUserController = Modular.getInject(UpdateUserController)
#     req = HttpRequest(body=await request.json())
#     result = await updateUserController(req)
#
#     response.status_code = status.get(result.status_code)
#     return result.body
#
#
# @app.delete("/user")
# async def deleteUser(request: Request, response: Response):
#     deleteUserController = Modular.getInject(DeleteUserController)
#     req = HttpRequest(body=await request.json())
#     result = await deleteUserController(req)
#
#     response.status_code = status.get(result.status_code)
#     return result.body