from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse

from calculate_deposit import calculate_deposit
from dto import PostDepositInput, PostDepositOutput

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(dir(exc), exc.errors())
    return PlainTextResponse(str(exc), status_code=400)


@app.post("/calculate-deposit", response_model=PostDepositOutput, status_code=200)
async def calculate_deposit_method(data: PostDepositInput) -> PostDepositOutput:
    return await calculate_deposit(data)
