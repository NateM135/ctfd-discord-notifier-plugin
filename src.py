from functools import wraps
from flask import request

from CTFd.models import Challenges, Solves
from CTFd.utils import config as ctfd_config
from CTFd.utils.decorators import admins_only
from CTFd.utils.user import get_current_team, get_current_user

from discord_webhook import DiscordWebhook, DiscordEmbed

from .config import config
from .utils import get_ordinal

def load(app):
    print("Loading discord webhook extension...")
    print("Creating challenge decorators...")
    def challenge_attempt_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # dont break challenge creation, teehee
            if request.method != "POST":
                return f(*args, **kwargs)

            # Run function first so we know result of submission
            result = f(*args, **kwargs)

            # Check result, check is submission is correct
            current_response = result.json
            if "success" in current_response and current_response["success"] and current_response.get("data").get("status") == "correct":
                TEAMS_MODE = ctfd_config.is_teams_mode()
                current_request = request.get_json()
        
                challenge_id = current_request.get('challenge_id')
                correctness = current_response.get("data").get("status")
                challenge = Challenges.query.filter_by(id=challenge_id).first()
                solvers = Solves.query.filter_by(challenge_id=challenge.id)

                webhook = DiscordWebhook(config["discord_webhook_url"])

                if TEAMS_MODE:
                    num_solvers = solvers.filter(Solves.team.has(hidden=False)).count()
                else:
                    num_solvers = solvers.filter(Solves.user.has(hidden=False)).count()

                if num_solvers > config["max_reported_solves"]:
                    return result

                if TEAMS_MODE:
                    # Special message for first blood
                    if num_solvers == 1:
                        embed = DiscordEmbed(description=f"🩸 {get_current_user().name} has gotten first blood on challenge {challenge.name}!")
                    else:
                        embed = DiscordEmbed(description=f"🚩 {get_current_user().name} has gotten the {get_ordinal(num_solvers)} solve on challenge {challenge.name}!")
                else:
                    if num_solvers == 1:
                        embed = DiscordEmbed(description=f"🩸 {get_current_user().name} has gotten first blood on challenge {challenge.name}!")
                    else:
                        embed = DiscordEmbed(description=f"🚩 {get_current_user().name} has gotten the #{get_ordinal(num_solvers)} on challenge {challenge.name}!")

                webhook.add_embed(embed)
                webhook.execute()

            return result
        return wrapper

    app.view_functions['api.challenges_challenge_attempt'] = challenge_attempt_decorator(app.view_functions['api.challenges_challenge_attempt'])