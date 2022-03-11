from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from src.adapters.controllers.get_all_users_controller import GetAllUsersController
from src.adapters.controllers.get_user_by_cpfrne_controller import GetUserByCpfRneController
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

@app.get("/")
async def getAllusers(response: Response):
    getAllUsersController = Modular.getInject(GetAllUsersController)
    req = HttpRequest(query=None)
    result = await getAllUsersController(req)
    response.status_code = status.get(result.status_code)
    return result.body


@app.get("/user/{cpfRne}")
async def geUser(cpfRne: int, response: Response):
    getAllUserByCpfRne = Modular.getInject(GetUserByCpfRneController)
    req = HttpRequest(query={'cpfRne': cpfRne})
    print(req)
    print(getAllUserByCpfRne)
    result = await getAllUserByCpfRne(req)
    response.status_code = status.get(result.status_code)
    return result.body

