from typing import Any, Dict, Optional

class HttpRequest:
    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None, query: Optional[Dict[str, Any]] = None) -> None:
        self.query = query
        self.body = body
        self.headers = headers

    def __repr__(self):
        return (
            f"HttpRequest (body={self.body}, query={self.query}, header={self.header})"
        )


class HttpResponse:
    def __init__(self, status_code: int, body: Any) -> None:
        self.status_code = status_code
        self.body = body

    def __repr__(self):
        return f"HttpResponse (status_code={self.status_code}, body={self.body})"

class Ok(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(200, body)
class Create(HttpResponse):
    def __init__(self) -> None:
        super().__init__(201, None)
class NoContent(HttpResponse):
    def __init__(self) -> None:
        super().__init__(204, None)
class BadRequest(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(400, body)
class InternalServerError(HttpResponse):
    def __init__(self, body: Any) -> None:
        super().__init__(500, body)