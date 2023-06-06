import requests
from datetime import datetime
from firebase_admin import firestore, initialize_app
from firebase_functions import https_fn

def extract_mlb_games(date):
    # Generate the MLB games API URL for the specified date
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={date}&endDate={date}&gameType=R&fields=dates,date,games,gamePk,status,abstractGameState,teams,away,home,team,id,name,gameDate"

    # Send a GET request to the MLB API
    response = requests.get(url)
    data = response.json()

    # Extract the games data
    games = data.get("dates", [])[0].get("games", [])

    return games

def store_mlb_games(date_str: str) -> None:
    # Convert the date string to a datetime object
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Extract the MLB games data
    games = extract_mlb_games(date)

    # Initialize the Firebase app
    initialize_app()

    # Get a reference to the Firestore database
    db = firestore.client()

    # Get a reference to the "mlb_games" collection
    games_ref = db.collection("mlb_games")

    # Create a new document with the requested date as the document ID
    doc_ref = games_ref.document(date_str)

    # Check if the document already exists
    if doc_ref.get().exists:
        print(f"MLB games data already stored for the requested date {date_str}")
        return

    # Store the MLB games data in the Firestore document
    doc_ref.set({"games": games})

    # Log the completion of the task
    print(f"MLB games data stored in Firestore for date: {date_str}")

@https_fn.on_request()
def store_mlb_games_endpoint(request) -> None:
    # Get the date parameter from the request query string
    date_str = request.args.get("date")
    
    # Call the store_mlb_games function with the provided date
    store_mlb_games(date_str)