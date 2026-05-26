from django.contrib.auth import authenticate, login, logout
from ninja import Router, Schema
from ninja.errors import HttpError
from ninja.security import django_auth

router = Router(tags=["Auth"])


class LoginIn(Schema):
    username: str
    password: str


class UserOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str


@router.post("/login/", response=UserOut, auth=None)
def api_login(request, payload: LoginIn):
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is None:
        raise HttpError(401, "Invalid credentials")
    login(request, user)
    return user


@router.post("/logout/", response={204: None}, auth=django_auth)
def api_logout(request):
    logout(request)
    return 204, None


@router.get("/me/", response=UserOut, auth=django_auth)
def me(request):
    return request.user
