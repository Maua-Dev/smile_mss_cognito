import os
from typing import List

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from src.adapters.controllers.check_token_controller import CheckTokenController
from src.adapters.controllers.create_user_controller import CreateUserController
from src.adapters.controllers.delete_user_controller import DeleteUserController
from src.adapters.controllers.get_all_users_controller import GetAllUsersController
from src.adapters.controllers.get_user_by_cpfrne_controller import GetUserByCpfRneController
from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.refresh_token_controller import RefreshTokenController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import HttpRequest, HttpResponse
from src.domain.entities.user import User
from src.main.users.module import Modular
from src.main.helpers.status import status

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

@app.get("/user/all")
async def getAllusers(response: Response):
    getAllUsersController = Modular.getInject(GetAllUsersController)
    req = HttpRequest(query=None)
    result = await getAllUsersController(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.get("/user/{cpfRne}")
async def getUser(cpfRne: int, response: Response):
    getAllUserByCpfRne = Modular.getInject(GetUserByCpfRneController)
    req = HttpRequest(query={'cpfRne': cpfRne})
    result = await getAllUserByCpfRne(req)

    response.status_code = status.get(result.status_code)
    return result.body


@app.post("/user")
async def createUser(request: Request, response: Response):
    createUserController = Modular.getInject(CreateUserController)
    req = HttpRequest(body=await request.json())
    result = await createUserController(req)

    response.status_code = status.get(result.status_code)
    return result.body

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

@app.post("/login")
async def login(request: Request, response: Response):
    loginUserController = Modular.getInject(LoginUserController)
    req = HttpRequest(body=await request.json())
    result = await loginUserController(req)


    response.status_code = status.get(result.status_code)
    return result.body


@app.post("/checkToken")
async def checkToken(request: Request, response: Response):
    checkTokenController = Modular.getInject(CheckTokenController)
    req = HttpRequest(body=await request.json())
    result = await checkTokenController(req)


    response.status_code = status.get(result.status_code)
    return result.body

@app.post("/refreshToken")
async def refreshToken(request: Request, response: Response):
    refreshTokenController = Modular.getInject(RefreshTokenController)
    req = HttpRequest(body=await request.json())
    result = await refreshTokenController(req)

    response.status_code = status.get(result.status_code)
    return result.body

