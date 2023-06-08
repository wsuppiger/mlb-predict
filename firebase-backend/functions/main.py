import requests
from datetime import datetime, date
from flask import jsonify, make_response
from firebase_admin import firestore, initialize_app, credentials
from firebase_functions import scheduler_fn, https_fn, options

options.set_global_options(max_instances=10)

# Initialize the Firebase app
cred = credentials.ApplicationDefault()
initialize_app(cred, {"projectId": "mlb-predict-19054"})


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

    # Get a reference to the Firestore database
    db = firestore.client()

    # Get a reference to the "mlb_games" collection
    games_ref = db.collection("mlb_games")

    # Create a new document with the requested date as the document ID
    doc_ref = games_ref.document(date_str)

    # Store or update the MLB games data in the Firestore document
    doc_ref.set({"games": games})

    # Get a reference to the "game_live" collection
    game_live_ref = db.collection("game_live").document("live")

    # Filter the games with a status of "Live"
    live_games = [game for game in games if game.get("status") == "Live"]

    # Update the live games list
    game_live_ref.set({"live_games": live_games})

    # Log the completion of the task
    print(f"MLB games data stored in Firestore for date: {date_str}")

    return jsonify({"message": "MLB games data stored successfully"})


@https_fn.on_call()
def store_mlb_games_endpoint(request: https_fn.CallableRequest) -> https_fn.Response:
    # Get the date parameter from the request query string
    date_str = request.data["date"]

    # Call the store_mlb_games function with the provided date
    store_or_update_mlb_games(date_str)

    return ""


@scheduler_fn.on_schedule(schedule="every 5 minutes")
def update_mlb_games_scheduled(event: scheduler_fn.ScheduledEvent) -> None:
    # Get the current date
    current_date = date.today()

    # Convert the date to string format
    date_str = current_date.strftime("%Y-%m-%d")

    # Call the store_mlb_games function with the provided date
    store_or_update_mlb_games(date_str)

    return ""
