from flask import Request, typing
import functions_framework

@functions_framework.http
def hello(request: Request) -> typing.ResponseReturnValue:
    return "Hello world!"