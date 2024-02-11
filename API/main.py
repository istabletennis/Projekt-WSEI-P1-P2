from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from passlib.context import CryptContext
from songs_utility import get_songs_from_release_range
from word_analysis import get_words_count_from_list_of_songs, \
    create_bar_chart_out_of_count_object, get_all_words_count_average_from_list_of_songs, \
    get_average_sentiment_polarity_from_list_of_songs, get_average_sentiment_subjectivity_from_list_of_songs
from fastapi.staticfiles import StaticFiles

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/2"
MONGO_DB_NAME = "2"
MONGO_USERS_COLLECTION_NAME = "users"
MONGO_SONGS_COLLECTION_NAME = "P2"

WORDS_COUNT_CHART_FILE = "static/words_chart.png"
WORDS_COUNT_CHART_SIZE = 30

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name='static')

mongo_client = MongoClient(MONGO_CONNECTION_STRING)
db = mongo_client[MONGO_DB_NAME]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

task_status = {}


def task_handler(db, collection_name, start_year, end_year):
    try:
        list_of_songs = get_songs_from_release_range(db, collection_name, start_year, end_year)

        songs_quantity = len(list_of_songs)

        words_count = get_words_count_from_list_of_songs(list_of_songs)
        word_chart_title = f"Top {WORDS_COUNT_CHART_SIZE} Words by Quantity"
        word_chart_y_axis_value = 'Word'
        create_bar_chart_out_of_count_object(word_chart_title, word_chart_y_axis_value, words_count,
                                             WORDS_COUNT_CHART_SIZE, WORDS_COUNT_CHART_FILE)

        task_status['word_count_average'] = get_all_words_count_average_from_list_of_songs(list_of_songs)

        task_status["average_subjectivity"] = get_average_sentiment_subjectivity_from_list_of_songs(list_of_songs)
        task_status["average_polarity"] = get_average_sentiment_polarity_from_list_of_songs(list_of_songs)

        task_status[
            'task_result'] = f"Results from period {start_year} - {end_year}. Based on data from {songs_quantity} songs"
    except Exception as e:
        task_status['task_result'] = f"Failed to create analysis. Problem occured: {e}"

    task_status['task_completed'] = True


def get_db():
    return db


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    user = db[MONGO_USERS_COLLECTION_NAME].find_one({"username": username})
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
    db[MONGO_USERS_COLLECTION_NAME].insert_one(user)
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
async def start_task(background_tasks: BackgroundTasks, start_year: int = Form(...), end_year: int = Form(...)):
    task_status['task_completed'] = False
    background_tasks.add_task(task_handler,
                              db=get_db(),
                              collection_name=MONGO_SONGS_COLLECTION_NAME,
                              start_year=start_year,
                              end_year=end_year)
    return RedirectResponse(url="/loading", status_code=status.HTTP_302_FOUND)


@app.get("/loading")
async def loading_page(request: Request):
    if task_status.get('task_completed'):
        return RedirectResponse(url="/result", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("loading.html", {"request": request})


@app.get("/result")
async def result_page(request: Request):
    return templates.TemplateResponse("result.html",
                                      {"request": request,
                                       "result": task_status["task_result"],
                                       "word_count_average": task_status["word_count_average"],
                                       "average_subjectivity": task_status["average_subjectivity"],
                                       "average_polarity": task_status["average_polarity"],
                                       "word_count_image": WORDS_COUNT_CHART_FILE})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
