from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from services import service
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

origins = ["http://localhost:3000"]


class UserCredentials(BaseModel):
    username: str
    password: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.post("/login")
def post_user(credentials: UserCredentials):
    username = credentials.username
    password = credentials.password
    service.auto_mri(username, password)
    return {"message": "forwarded from mri login efficiently"}
    # page.locator("xpath = //*[@id='btnSave']").click() #save


# @app.exception_handler(CustomException)
# def custom_exception_handler(request: Request, exc: CustomException):
#     return JSONResponse(
#         status_code=404,
#         content={"message": f"Invalid credentials"},
#     )