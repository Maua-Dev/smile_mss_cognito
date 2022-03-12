from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from src.adapters.controllers.check_token_controller import CheckTokenController
from src.adapters.controllers.create_user_controller import CreateUserController
from src.adapters.controllers.delete_user_controller import DeleteUserController
from src.adapters.controllers.get_all_users_controller import GetAllUsersController
from src.adapters.controllers.get_user_by_cpfrne_controller import GetUserByCpfRneController
from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import HttpRequest
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
    return result


@app.get("/user/{cpfRne}")
async def geUser(cpfRne: int, response: Response):
    getAllUserByCpfRne = Modular.getInject(GetUserByCpfRneController)
    req = HttpRequest(query={'cpfRne': cpfRne})
    print(req)
    print(getAllUserByCpfRne)
    result = await getAllUserByCpfRne(req)
    response.status_code = status.get(result.status_code)
    return result.body

@app.post("/user")
async def root(request: Request):
    createUserController = Modular.getInject(CreateUserController)
    req = HttpRequest(body=await request.json())
    result = await createUserController(req)
    return result

@app.put("/user")
async def root(request: Request):
    updateUserController = Modular.getInject(UpdateUserController)
    req = HttpRequest(body=await request.json())
    result = await updateUserController(req)
    return result

@app.delete("/user")
async def root(request: Request):
    deleteUserController = Modular.getInject(DeleteUserController)
    req = HttpRequest(body=await request.json())
    result = await deleteUserController(req)
    return result

@app.post("/login")
async def login(request: Request):
    loginUserController = Modular.getInject(LoginUserController)
    req = HttpRequest(body=await request.json())
    result = await loginUserController(req)
    return result

@app.post("/checkToken")
async def checkToken(request: Request):
    checkTokenController = Modular.getInject(CheckTokenController)
    req = HttpRequest(body=await request.json())
    result = await checkTokenController(req)
    return result



