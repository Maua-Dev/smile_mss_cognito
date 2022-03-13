
from src.main.main import app

from mangum import Mangum

app.root_path = "/dev/smile-mss-cognito"

handler = Mangum(app,
                 api_gateway_base_path='smile-mss-cognito')