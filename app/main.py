from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.models.pydantic_models import RegForm, ApiResponse
from app.router import auth_routes, user_routes, pokemon_routes


app = FastAPI()

app.include_router(auth_routes.auth)
app.include_router(user_routes.user)
app.include_router(pokemon_routes.pokemon)

'''
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.
We need it here to process static files (CSS, JS, pics) which are connected to the main HTML file.
'''
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc = RegForm.change_user_answer(exc.errors()[0])
    err_ans = ApiResponse(success=False, error=exc['msg'])
    return JSONResponse(
        status_code=422,
        content=err_ans.model_dump()
    )