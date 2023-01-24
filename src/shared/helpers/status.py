from enum import Enum
from fastapi import status

status = {
    200: status.HTTP_200_OK,
    201: status.HTTP_201_CREATED,
    204: status.HTTP_204_NO_CONTENT,
    400: status.HTTP_400_BAD_REQUEST,
    401: status.HTTP_401_UNAUTHORIZED,
    500: status.HTTP_500_INTERNAL_SERVER_ERROR
}