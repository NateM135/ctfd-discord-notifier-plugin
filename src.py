from functools import wraps
from flask import (
    abort,
    request,
    render_template,
    redirect,
    jsonify,
    Blueprint,
    url_for,
    Response
)

from CTFd.models import Challenges, Solves
from CTFd.utils import config as ctfd_config
from CTFd.utils.decorators import admins_only
from CTFd.utils.user import get_current_team, get_current_user

from discord_webhook import DiscordWebhook, DiscordEmbed

def load(app):
    print("Loading discord webhook extension...")

    config_webhook = Blueprint('config_webhook', __name__, template_folder='templates')

    @config_webhook.route('/admin/config_webhook', methods=['GET', 'POST'])
    @admins_only
    def config_webhook_route():
        if request.method == 'GET':
            return render_template('webhook_config.html')
        elif request.method == 'POST':
            return '', 200

    app.register_blueprint(config_webhook)

    print("Creating challenge decorators...")
    def challenge_attempt_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Run function first so we know result of submission
            result = f(*args, **kwargs)

            # Check result, check is submission is correct
            current_response = result.json
            if "success" in current_response and current_response["success"] and current_response.get("data").get("status") == "correct":
                print("Correct Attempt")

            TEAMS_MODE = ctfd_config.is_teams_mode()
            current_request = request.get_json()

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
            if TEAMS_MODE:
                solvers = solvers.filter(Solves.team.has(hidden=False))
            else:
                solvers = solvers.filter(Solves.user.has(hidden=False))
            num_solves = solvers.count()
            print(f"Solve Count: {num_solves}")

            webhook = DiscordWebhook("")
            embed = DiscordEmbed(description=f"🩸 {get_current_user().name} has gotten solve # {num_solves} on challenge {challenge.name}")
            webhook.add_embed(embed)
            webhook.execute()

            return result
        return wrapper

    app.view_functions['api.challenges_challenge_attempt'] = challenge_attempt_decorator(app.view_functions['api.challenges_challenge_attempt'])