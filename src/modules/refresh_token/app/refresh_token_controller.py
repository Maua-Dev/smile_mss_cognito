

class RefreshTokenController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._refreshTokenUsecase = RefreshTokenUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')

        try:
            token = req.headers.get('Authorization').split(' ')
            if len(token) != 2 or token[0] != 'Bearer':
                return BadRequest('Invalid token.')
            refreshToken = token[1]
            tokens = await self._refreshTokenUsecase(refreshToken)
            accessToken, refreshToken = tokens
            refreshTokenModel = RefreshTokenModel(
                accessToken=accessToken, refreshToken=refreshToken)
            return Ok(refreshTokenModel.toDict())

        except InvalidToken as e:
            return BadRequest(e.message)

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
