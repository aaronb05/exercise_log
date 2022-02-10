import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


def post_workout(workout):
    nutrition_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "content-type": "application/json"
    }
    params = {
        "query": workout,
        "gender": "male",
        "weight_kg": 78.02,
        "height_cm": 1.88,
        "age": 31
    }
    post = requests.post(url=nutrition_endpoint, json=params, headers=headers)
    post.raise_for_status()
    response = post.json()
    return response


def add_to_sheet(exercise, calories, duration):
    today = datetime.now().date().strftime("%m/%d/%Y")
    current_time = datetime.now().time().strftime("%I:%M %p")
    add_endpoint = "https://api.sheety.co/f1d4d46bfaa887c14bc9043c594ef651/workoutTracking/sheet1"
    data = {
        "sheet1": {
            "date": today,
            "time": current_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }
    auth = (USER, PASSWORD)
    post = requests.post(url=add_endpoint, json=data, auth=auth)
    post.raise_for_status()
    print(post.text)


