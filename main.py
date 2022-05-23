from api import get_results, add_to_sheet
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/post_workout', methods=["POST"])
def post_workout():

    # Get workout data
    workout = request.form["work_out"]
    user = request.form["user"]
    workout_results = get_results(workout=workout, user=user)

    # Parse workout details
    calories = float(workout_results["exercises"][0]["nf_calories"])
    activity = str(workout_results["exercises"][0]["name"]).title()
    duration = str(workout_results["exercises"][0]["duration_min"])

    # Add workout to google sheet
    add_to_sheet(user=user, exercise=activity, calories=calories, duration=duration)
    return redirect("https://docs.google.com/spreadsheets/d/1MtPsT8bg-GZpLnHVlCNj5YKAwRsliFeCOcghJAuZ8C8/edit#gid=0")


if __name__ == "__main__":
    app.run(debug=True)

