import requests
import datetime as dt

import config

nutritionix_app_id = config.NUTRITIONIX_APP_ID
nutritionix_api_key = config.NUTRITIONIX_API_KEY
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

sheety_username = config.SHEETY_USERNAME
sheety_project_name = config.SHEETY_PROJECT_NAME
sheet_name = config.SHEET_NAME
sheety_token = config.SHEETY_TOKEN
sheety_endpoint = f"https://api.sheety.co/{sheety_username}/{sheety_project_name}/{sheet_name}"

sheety_headers = {
    "Authorization": config.SHEETY_BEARER,
}
nutritionix_headers = {
    "x-app-id": nutritionix_app_id,
    "x-app-key": nutritionix_api_key,
}
nutritionix_body = {
    "query": input("Tell me which exercises you did: "),
    "gender": "male",
    "weight_kg": config.WEIGHT,
    "height_cm": config.HEIGHT,
    "age": config.AGE,
}

nutritionix_response = requests.post(url=nutritionix_endpoint, json=nutritionix_body, headers=nutritionix_headers)
nutritionix_response.raise_for_status()
exercises = nutritionix_response.json()["exercises"]

now = dt.datetime.now()
sheety_body = {}

for exercise in exercises:
    sheety_body.update({
        "workout": {
            "date": now.strftime("%Y/%m/%d"),
            "time": now.strftime("%H:%M:%S"),
            "exercise": exercise["user_input"].capitalize(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    })
    response = requests.post(url=sheety_endpoint, json=sheety_body, headers=sheety_headers)
    response.raise_for_status()
    print(response.json())
