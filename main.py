from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import Response
from services import service
from fastapi.middleware.cors import CORSMiddleware

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
