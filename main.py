from api import get_results, add_to_sheet, smtp_email
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


@app.route('/send_email', methods=["POST"])
def send_email():
    # Gather info from form
    from_email = request.form["email"]
    email_message = request.form["message"]
    name = request.form["name"]

    if from_email == "" or name == "" or email_message == "":
        return render_template("email_failure.html", email=from_email, name=name, message=email_message)

    email = smtp_email(name=name, from_addr=from_email, email_message=email_message)
    print(email)
    if email:
        return render_template('index.html', message="Email sent successfully!")
    elif email == "invalid credentials":
        return render_template('email_failure.html', message="Oops, looks there is a problem on our end! "
                                              "Please check back at a later time")
    elif not email:
        return render_template('email_failure', message="Sorry, we are unable to process your request at this time,"
                                              "Please try again later")


if __name__ == "__main__":
    app.run(debug=True)

