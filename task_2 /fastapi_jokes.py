# simple_fastapi_jokes.py
# A very simple FastAPI app that fetches jokes from JokeAPI and saves them in a SQLite database

from fastapi import FastAPI
import requests
import sqlite3

app = FastAPI()

# create the database table if it doesn't exist  
def create_database():
    connection = sqlite3.connect("jokes.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            type TEXT,
            joke TEXT,
            setup TEXT,
            delivery TEXT,
            nsfw BOOLEAN,
            political BOOLEAN,
            sexist BOOLEAN,
            safe BOOLEAN,
            lang TEXT
        )
    """)

    connection.commit()
    connection.close()


# Fetch jokes from JokeAPI  
def fetch_jokes():
    all_jokes = []
    jokes_needed = 100
    jokes_got = 0

    while jokes_got < jokes_needed:
        # JokeAPI supports fetching up to 10 jokes at once
        response = requests.get("https://v2.jokeapi.dev/joke/Any?amount=10")
        data = response.json()

        jokes = data.get("jokes", [])
        all_jokes.extend(jokes)
        jokes_got += len(jokes)

    return all_jokes[:100]

# Save jokes into SQLite database  
def save_jokes(jokes):
    connection = sqlite3.connect("jokes.db")
    cursor = connection.cursor()

    for joke in jokes:
        category = joke.get("category", "")
        type_ = joke.get("type", "")
        nsfw = joke.get("flags", {}).get("nsfw", False)
        political = joke.get("flags", {}).get("political", False)
        sexist = joke.get("flags", {}).get("sexist", False)
        safe = joke.get("safe", False)
        lang = joke.get("lang", "")

        if type_ == "single":
            joke_text = joke.get("joke", "")
            setup = ""
            delivery = ""
        else:
            joke_text = ""
            setup = joke.get("setup", "")
            delivery = joke.get("delivery", "")

        cursor.execute("""
            INSERT INTO jokes (category, type, joke, setup, delivery, nsfw, political, sexist, safe, lang)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (category, type_, joke_text, setup, delivery, nsfw, political, sexist, safe, lang))

    connection.commit()
    connection.close()


# Create an endpoint to fetch and store jokes  
@app.get("/fetch_jokes")
def fetch_and_store_jokes():
    create_database()
    jokes = fetch_jokes()
    save_jokes(jokes)
    return {"message": f"Heey got {len(jokes)} memes bro!"}


#  Create an endpoint to show a few jokes from the database 
@app.get("/show_jokes")
def show_jokes():
    connection = sqlite3.connect("jokes.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, category, type, joke, setup, delivery FROM jokes LIMIT 5")
    rows = cursor.fetchall()

    jokes_list = []
    for row in rows:
        jokes_list.append({
            "id": row[0],
            "category": row[1],
            "type": row[2],
            "joke": row[3],
            "setup": row[4],
            "delivery": row[5],
        })

    connection.close()
    return {"sample_jokes": jokes_list}
