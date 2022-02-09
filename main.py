import api

query_text = input("What did you do today: ")

workout_results = config.post_workout(workout=query_text)
print(workout_results)

calories = float(workout_results["exercises"][0]["nf_calories"])
activity = str(workout_results["exercises"][0]["name"]).title()
duration = str(workout_results["exercises"][0]["duration_min"])
print(calories)
print(activity)
print(duration)
config.add_to_sheet(exercise=activity, calories=calories, duration=duration)





