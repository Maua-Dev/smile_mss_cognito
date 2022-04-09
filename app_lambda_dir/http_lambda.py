

# {
#   "statusCode": 200,
#   "body": {
#     "message": "Hello, world!"
#   },
#   "headers": {
#     "content-type": "application/json"
#   }
#   "isBase64Encoded": false,
# }

class HttpResponse:
    status_code: int = 200
    body: dict = {"message": "No response"}
    headers: dict = {"content-type": "application/json"}

    def __init__(self, response: any = None) -> None:
        if not response:
            return

        if isinstance(response, str):
            self.body = response

        elif isinstance(response, dict):
            self.body = response["body"] if "body" in response else HttpResponse.body
            self.headers = response["headers"] if "headers" in response else HttpResponse.headers
            self.status_code = response["status_code"] if "status_code" in response else HttpResponse.status_code



    def toDict(self) -> dict:
        return {
            "statusCode": self.status_code,
            "body": self.body,
            "headers": self.headers,
            "isBase64Encoded": False
        }

    def __repr__(self):
        return (
            f"HttpResponse (status_code={self.status_code}, body={self.body}, headers={self.headers})"
        )


