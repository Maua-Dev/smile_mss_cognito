from http_lambda import HttpResponse


class LambdaApp:
    paths = []

    def __init__(self):
        pass

    def get(self, path):
        def wrapper(func):
            self.paths.append(
                {
                    "path": path,
                    "func": func,
                }
            )
        return wrapper

    def __call__(self, event, context):
        for path in self.paths:
            if event["rawPath"] == path["path"]:
                return HttpResponse(path["func"]()).toDict()
        return HttpResponse({"status_code": 404, "body": {"message": "Not Found"}}).toDict()



