from ninja import NinjaAPI
from ninja.security import HttpBearer


class GlobalAuth(HttpBearer):
    openapi_scheme: str = "token"

    def authenticate(self, request, token):
        if token == "mGuYBIJLbvSo":
            return token


api = NinjaAPI(auth=GlobalAuth())


@api.get("/hello")
def hello(request):
    return {"message": "Hello world"}
