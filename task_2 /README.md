### Install packages:
pip install fastapi uvicorn requests



### Run the app:
uvicorn simple_fastapi_jokes:app --reload



### Endpoints:


Fetch and save jokes: http://127.0.0.1:8000/fetch_jokes


Show saved jokes: http://127.0.0.1:8000/show_jokes


API docs: http://127.0.0.1:8000/docs




##### A SQLite file (jokes.db) is created automatically.


#### Files


simple_fastapi_jokes.py — main FastAPI app


jokes.db — database file

