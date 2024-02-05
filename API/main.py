from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from passlib.context import CryptContext
import time
import subprocess

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/2"
MONGO_DB_NAME = "2"
MONGO_COLLECTION_NAME = "users"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

mongo_client = MongoClient(MONGO_CONNECTION_STRING)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

task_status = {}


def long_running_task():
    time.sleep(10)
    task_status['task_completed'] = True
    return "Task completed"


def get_db():
    return db


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    user = db[MONGO_COLLECTION_NAME].find_one({"username": username})
    if user:
        return user
    return None


async def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user["password_hash"]):
        return False
    return user


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    username = request.cookies.get("username")
    if username:
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    else:
        response = templates.TemplateResponse("index.html", {"request": request})
    return response


@app.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(get_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="username", value=user["username"])
    return response


@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    hashed_password = pwd_context.hash(password)
    user = {
        "username": username,
        "password_hash": hashed_password
    }
    db[MONGO_COLLECTION_NAME].insert_one(user)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="username", value=user["username"])
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    username = request.cookies.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please login first")
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})


@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("username")
    return response


@app.post("/start-task")
async def start_task(background_tasks: BackgroundTasks):
    task_status['task_completed'] = False
    background_tasks.add_task(long_running_task)
    return RedirectResponse(url="/loading", status_code=status.HTTP_302_FOUND)


@app.get("/loading")
async def loading_page(request: Request):
    if task_status.get('task_completed'):
        return RedirectResponse(url="/result", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("loading.html", {"request": request})


@app.get("/result")
async def result_page(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)