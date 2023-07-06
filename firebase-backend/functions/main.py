import json
import logging
import threading
import time
from typing import List
import requests
from datetime import datetime, date
from flask import jsonify
from firebase_admin import firestore, initialize_app, credentials
from firebase_functions import scheduler_fn, https_fn, options
from firebase_functions.firestore_fn import (
    on_document_updated,
    Event,
    DocumentSnapshot,
)

options.set_global_options(max_instances=10, timeout_sec=350)

HB_ITERATIONS, HB_DELAY = 30, 10
DECISION_SECS = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance
logger = logging.getLogger(__name__)


# Initialize the Firebase app
cred = credentials.ApplicationDefault()
initialize_app(cred, {"projectId": "mlb-predict-19054"})

# Get a reference to the Firestore database
db = firestore.client()


def extract_mlb_games(date):
    # Generate the MLB games API URL for the specified date
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={date}&endDate={date}&gameType=R&fields=dates,date,games,gamePk,status,abstractGameState,teams,away,home,team,id,name,gameDate"

    # Send a GET request to the MLB API
    response = requests.get(url)
    data = response.json()

    # Extract the games data
    dates = data.get("dates", [])
    if dates:
        games_data = dates[0].get("games", [])
        games = []
        for game_data in games_data:
            gamePk = game_data.get("gamePk")
            gameDate = game_data.get("gameDate")
            teams = game_data.get("teams", {})
            awayTeam = teams.get("away", {}).get("team", {}).get("name")
            homeTeam = teams.get("home", {}).get("team", {}).get("name")
            abstractGameState = game_data.get("status", {}).get("abstractGameState")
            status = abstractGameState if abstractGameState else "Unknown"
            if gamePk and gameDate and awayTeam and homeTeam:
                formatted_game = {
                    "gamePk": gamePk,
                    "gameDate": gameDate,
                    "awayTeam": awayTeam,
                    "homeTeam": homeTeam,
                    "status": status,
                }
                games.append(formatted_game)

        games.sort(key=lambda game: game["gameDate"])

        return games

    return []


def store_or_update_mlb_games(date_str: str):
    # Convert the date string to a datetime object
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Extract the MLB games data
    games = extract_mlb_games(date)

    # Get a reference to the "mlb_games" collection
    games_ref = db.collection("mlb_games")

    # Create a new document with the requested date as the document ID
    doc_ref = games_ref.document(date_str)

    # Store or update the MLB games data in the Firestore document
    doc_ref.set({"games": games})

    # Get a reference to the "game_live" collection
    game_live_ref = db.collection("game_live").document("live")

    # Filter the games with a status of "Live"
    live_games = [game.get("gamePk") for game in games if game.get("status") == "Live"]

    # Update the live games list
    game_live_ref.set({"live_games": live_games})

    # Log the completion of the task
    logger.info(f"MLB games data stored in Firestore for date: {date_str}")

    return jsonify({"message": "MLB games data stored successfully"})


@https_fn.on_call()
def store_mlb_games_endpoint(request: https_fn.CallableRequest) -> https_fn.Response:
    # Get the date parameter from the request query string
    date_str = request.data["date"]

    # Call the store_mlb_games function with the provided date
    store_or_update_mlb_games(date_str)

    return ""


@scheduler_fn.on_schedule(schedule="every 5 minutes")
def heartbeat_scheduled(event: scheduler_fn.ScheduledEvent) -> None:
    current_date = date.today()
    date_str = current_date.strftime("%Y-%m-%d")
    store_or_update_mlb_games(date_str)

    backend_heartbeat()

    return


def fetch_play_data(gamepk):
    url = f"https://statsapi.mlb.com/api/v1.1/game/{gamepk}/feed/live"

    response = requests.get(url)
    data = response.json()

    play = data.get("liveData", {}).get("plays", {}).get("currentPlay", {})
    atBatIndex = play.get("about", {}).get("atBatIndex")
    isTopInning = play.get("about", {}).get("isTopInning")
    inning = play.get("about", {}).get("inning")
    count = play.get("count")
    batter = play.get("matchup", {}).get("batter")
    pitcher = play.get("matchup", {}).get("pitcher")
    postOnFirst = play.get("matchup", {}).get("postOnFirst")
    postOnSecond = play.get("matchup", {}).get("postOnSecond")
    postOnThird = play.get("matchup", {}).get("postOnThird")
    awayScore = play.get("result", {}).get("awayScore")
    homeScore = play.get("result", {}).get("homeScore")

    teams = data.get("gameData", {}).get("teams", {})
    homeTeam = teams.get("home", {}).get("name")
    awayTeam = teams.get("away", {}).get("name")

    play_by_play = []
    all_plays = data.get("liveData", {}).get("plays", {}).get("allPlays", [])
    for play in all_plays:
        atBatIndex = play.get("about", {}).get("atBatIndex")
        event = play.get("result", {}).get("event")
        eventType = play.get("result", {}).get("eventType")
        isOut = play.get("result", {}).get("isOut")
        description = play.get("result", {}).get("description")
        isComplete = play.get("about", {}).get("isComplete")

        play_data = {
            "atBatIndex": atBatIndex,
            "event": event,
            "eventType": eventType,
            "isOut": isOut,
            "description": description,
            "isComplete": isComplete,
        }
        play_by_play.append(play_data)

    return {
        "meta_data": {
            "homeTeam": homeTeam,
            "awayTeam": awayTeam,
        },
        "live": {
            "atBatIndex": atBatIndex,
            "isTopInning": isTopInning,
            "inning": inning,
            "count": count,
            "batter": batter,
            "pitcher": pitcher,
            "postOnFirst": postOnFirst,
            "postOnSecond": postOnSecond,
            "postOnThird": postOnThird,
            "awayScore": awayScore,
            "homeScore": homeScore,
        },
        "play_by_play": play_by_play,
    }


def backend_heartbeat():
    live_ref = db.collection("game_live").document("live")
    live_games = live_ref.get().to_dict().get("live_games", [])
    player_active_games = live_ref.get().to_dict().get("player_active_games", [])
    gamepks = list(set(live_games) & set(player_active_games))

    logger.info(f"backend heartbeat games active and live: {gamepks}")

    if gamepks:
        # Create a thread to run the async function
        thread = threading.Thread(
            target=process_play_data, args=(gamepks, HB_ITERATIONS, HB_DELAY)
        )
        thread.start()

    return ""


# The purpose of this function is to create a temporary heartbeat for games
# that are not included in the heartbeat every 5 minutes, but need to be
# kickstarted (like CPR for heart).  This is similar to `backend_heartbeat`.
@https_fn.on_call()
def backend_CPR_heartbeat(request: https_fn.CallableRequest) -> https_fn.Response:
    gamepk = int(request.data.get("gamepk"))

    game_live_ref = db.collection("game_live").document("live")
    game_live_ref.update({"player_active_games": firestore.ArrayUnion([gamepk])})

    # Create a thread to run the async function
    thread = threading.Thread(
        target=process_play_data, args=([gamepk], HB_ITERATIONS, HB_DELAY)
    )
    thread.start()

    return ""


def process_play_data(gamepks: List[int], iterations: int, delay: int) -> None:
    for i in range(iterations):
        for gamepk in gamepks:
            logger.info(f"process_play_data iteration {i} for gamepk {gamepk}")

            play_data = fetch_play_data(gamepk)
            doc_ref = db.collection("mlb_play_by_play").document(str(gamepk))
            doc_ref.set(play_data)

            at_bat_ref = db.collection("scoring_index").document(str(gamepk))
            current_ab_index = at_bat_ref.get().get("index")

            ab_index = str(play_data.get("live", {}).get("atBatIndex"))
            if current_ab_index is None or current_ab_index != ab_index:
                ten_secs_from_now = int(time.time() + DECISION_SECS) * 1000
                # handle case where first request is sent so no one can make a decision
                if current_ab_index is None:
                    ten_secs_from_now = 0
                at_bat_ref.set({"index": ab_index, "decisionTime": ten_secs_from_now})

        time.sleep(delay)


@https_fn.on_call()
def make_play_pick(request: https_fn.CallableRequest) -> https_fn.Response:
    # Extract request parameters
    uid = request.data.get("uid")
    gamepk = request.data.get("gamepk")
    atBatIndex = request.data.get("atBatIndex")
    pick = request.data.get("pick")
    name = request.data.get("name")

    if not uid or not gamepk or not atBatIndex or not pick or not name:
        return {"error": "Missing required parameters."}

    # ensure submitted in time
    at_bat_ref = db.collection("scoring_index").document(str(gamepk))
    current_decision_time = at_bat_ref.get().get("decisionTime")
    now = int(time.time()) * 1000
    if now > current_decision_time:
        return {
            "success": False,
            "message": 'Your prediction was submitted too late.  Watch for the gray timer under "Predict Play", and make the pick before it expires.',
        }

    # Access Firestore
    collection_ref = db.collection("mlb_play_by_play")
    doc_ref = collection_ref.document(gamepk)

    # Create the 'users' subcollection if it doesn't exist
    users_collection_ref = doc_ref.collection("users")

    # Create the 'picks' document under the user's ID
    user_doc_ref = users_collection_ref.document(uid)
    user_doc_ref.set({"name": name}, merge=True)

    # Retrieve existing 'picks' field
    user_doc = user_doc_ref.get()
    existing_picks = user_doc.to_dict().get("picks", {})

    # Merge existing picks with the new pick
    existing_picks.update({atBatIndex: pick})

    logger.info(existing_picks)

    # Update the 'picks' field with the merged result
    user_doc_ref.update({"picks": existing_picks})

    return {"success": True}


def get_winner_map(points_data, lastAtBatEvent):
    winner_map = {}

    # Find the event in points_data matching lastAtBatEvent
    for option in points_data["options"].values():
        for suboption in option["suboptions"]:
            if lastAtBatEvent in points_data["suboptions"][suboption]["events"]:
                winner_map[suboption] = points_data["suboptions"][suboption]["points"]
                break

    # Find the corresponding option and add suboptions to winner_map
    for option, suboptions in points_data["options"].items():
        if any(suboption in winner_map for suboption in suboptions["suboptions"]):
            for suboption in suboptions["suboptions"]:
                winner_map[suboption] = (
                    winner_map.get(suboption, 0)
                    + points_data["options"][option]["points"]
                )
    return winner_map


@on_document_updated(document="scoring_index/{gamepk}")
def update_scores_on_at_bat_index_change(event: Event[DocumentSnapshot]) -> None:
    logger.info("running update_scores_on_at_bat_index_change")
    gamepk = event.params["gamepk"]
    new_values = event.data.before.to_dict()
    prev_atBatIndex = new_values["index"]

    # Access Firestore
    users_collection_ref = db.collection(f"mlb_play_by_play/{gamepk}/users")
    mlb_play_by_play_ref = db.document(f"mlb_play_by_play/{gamepk}")

    # Retrieve all users under mlb_play_by_play/{gamepk}/users
    users = users_collection_ref.get()

    # Retrieve the play_by_play data
    play_by_play = mlb_play_by_play_ref.get().to_dict().get("play_by_play", {})

    # Read the points_values.json file
    with open("point_values.json") as file:
        points_data = json.load(file)

    # Set lastAtBatEvent to play_by_play event at prev_atBatIndex
    lastAtBatEvent = play_by_play[int(prev_atBatIndex)].get("event", "")

    # Get the winner map
    winner_map = get_winner_map(points_data, lastAtBatEvent)

    # Iterate over each user
    for user_doc in users:
        user_id = user_doc.id
        user_data = user_doc.to_dict()
        picks = user_data.get("picks", {})
        score = user_data.get("score", 0)

        # Check if the previous atBatIndex in picks matches the winner_map
        if prev_atBatIndex in picks and picks[prev_atBatIndex] in winner_map:
            logger.info(f"added {winner_map[picks[prev_atBatIndex]]} to {user_id}")
            score += winner_map[picks[prev_atBatIndex]]

        # Update the score field for the user
        user_ref = users_collection_ref.document(user_id)
        user_ref.update({"score": score})

    return {"success": True}


# # Function to print eventType for all indexes in play_by_play array
# @on_document_updated(document="scoring_index/{gamepk}")
# def print_event_types(event: Event[DocumentSnapshot]) -> None:
#     db = firestore.client()
#     collection_ref = db.collection("mlb_play_by_play")

#     # Retrieve all documents in the collection
#     docs = collection_ref.get()

#     for doc in docs:
#         # Get the play_by_play array
#         play_by_play = doc.to_dict().get("play_by_play", [])

#         for index, play in enumerate(play_by_play):
#             # Get the eventType for each index
#             event_type = play.get("event")
#             logger.info(f"{event_type}")
