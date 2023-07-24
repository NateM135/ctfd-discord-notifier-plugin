from functools import wraps
from flask import Flask, request, g
from CTFd.utils.user import get_current_team, get_current_user
from CTFd.utils import config as ctfd_config

def load(app):
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")

    def challenge_attempt_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            TEAMS_MODE = ctfd_config.is_teams_mode()
            result = f(*args, **kwargs)

            # Retrieve all needed information
            TEAMS_MODE = ctfd_config.is_teams_mode()
            current_request = request.get_json()
            current_response = result.json

            if TEAMS_MODE:
                print("Teams Mode")
                print(f"Team Name: {get_current_team().name}")

            print(f"Current User: {get_current_user().name}")
    
            challenge_id = current_request.get('challenge_id')
            correctness = current_response.get("data").get("status")

            print(f"Challenge ID: {challenge_id}")
            print(f"Submission Correctness: {correctness}")
            return result
        return wrapper

    app.view_functions['api.challenges_challenge_attempt'] = challenge_attempt_decorator(app.view_functions['api.challenges_challenge_attempt'])