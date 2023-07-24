from functools import wraps
from flask import request

from CTFd.models import Challenges, Solves
from CTFd.utils import config as ctfd_config
from CTFd.utils.user import get_current_team, get_current_user

def load(app):
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")
    print("PLUGIN IS WORKING")

    def challenge_attempt_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)

            # Retrieve all needed information
            TEAMS_MODE = ctfd_config.is_teams_mode()
            current_request = request.get_json()
            current_response = result.json

            if TEAMS_MODE:
                print("Teams Mode")
                print(f"Team Name: {get_current_team().name}")
            else:
                print("Not Teams Mode")
            print(f"Current User: {get_current_user().name}")
    
            challenge_id = current_request.get('challenge_id')
            correctness = current_response.get("data").get("status")
            print(f"Challenge ID: {challenge_id}")
            print(f"Submission Correctness: {correctness}")

            challenge = Challenges.query.filter_by(id=challenge_id).first()
            solvers = Solves.query.filter_by(challenge_id=challenge.id)
            num_solves = solvers.count()
            print(f"Solve Count: {num_solves}")

            return result
        return wrapper

    app.view_functions['api.challenges_challenge_attempt'] = challenge_attempt_decorator(app.view_functions['api.challenges_challenge_attempt'])