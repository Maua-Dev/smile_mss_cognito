from app_lambda_dir.app_lambda import LambdaApp

app = LambdaApp()


@app.get("/checkToken")
def checkToken(request, response: Response):
    checkTokenController = Modular.getInject(CheckTokenController)
    req = HttpRequest(headers=request.headers)
    result = await checkTokenController(req)

    response.status_code = status.get(result.status_code)
    return result.body