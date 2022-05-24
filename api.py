import os
import requests
from datetime import datetime
from smtplib import SMTP, SMTPResponseException, SMTPAuthenticationError
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("app_id")
APP_KEY = os.getenv("app_key")
USER = os.getenv("username")
PASSWORD = os.getenv("password")
GMAIL = os.getenv("gmail")
GMAIL_KEY = os.getenv("gmail_key")
AARON_G = "male"
AARON_W = 78.02
AARON_H = 188
AARON_A = 31
TORI_G = "female"
TORI_W = 58.51
TORI_H = 155
TORI_A = 28


def get_results(workout, user):
    nutrition_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "content-type": "application/json"
    }
    if user == "Aaron Boyles":
        params = {
            "query": workout,
            "gender": AARON_G,
            "weight_kg": AARON_W,
            "height_cm": AARON_H,
            "age": AARON_A
        }
    elif user == "Tori Boyles":
        params = {
            "query": workout,
            "gender": TORI_G,
            "weight_kg": TORI_W,
            "height_cm": TORI_H,
            "age": TORI_A
        }
    else:
        params = {
            "query": workout,
            "gender": AARON_G,
            "weight_kg": AARON_W,
            "height_cm": AARON_H,
            "age": AARON_A
        }
    post = requests.post(url=nutrition_endpoint, json=params, headers=headers)
    post.raise_for_status()
    response = post.json()
    return response


def add_to_sheet(exercise, calories, duration, user):
    today = datetime.now().date().strftime("%m/%d/%Y")
    current_time = datetime.now().time().strftime("%I:%M %p")
    add_endpoint = "https://api.sheety.co/f1d4d46bfaa887c14bc9043c594ef651/workoutTracking/sheet1"
    data = {
        "sheet1": {
            "date": today,
            "time": current_time,
            "person": user,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }
    auth = (USER, PASSWORD)
    post = requests.post(url=add_endpoint, json=data, auth=auth)
    post.raise_for_status()


def smtp_email(from_addr, email_message, name):
    try:
        with SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=GMAIL_KEY)
            connection.sendmail(
                from_addr=from_addr,
                to_addrs="aboyles05@gmail.com",
                msg=f"Subject: New Inquiry from {name} at {from_addr}!\n\n"
                    f"{email_message}"
            )
        return True
    except SMTPAuthenticationError as e:
        print(e)
        return "invalid credentials"
    except SMTPResponseException as e:
        print(e)
        return False

