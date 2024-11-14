
Asynchronous Client using aiohttp for the Deribit Cryptocurrency Exchange

In this project, the client retrieves the current price of btc_usd and eth_usd from the exchange every minute and then saves the currency ticker, the current price and the timestamp in a PostgreSQL database.

REST API for working with saved data:

Retrieve all saved data for a specified currency (the currency name must be input as a mandatory parameter "ticker" in Swagger UI).
Retrieve the latest price for a currency (the currency name must be input as a mandatory parameter "ticker").
Retrieve the currency price with a date filter (the currency name must be input as a mandatory parameter "ticker", and the date must be entered in the format year-month-day hours-minutes).

Running the Application:

Activate the virtual environment with the command: . \venv\Scripts\Activate
Start the application with the command: uvicorn app.main:app --reload
Go to the website: http://127.0.0.1:8000/docs
Running the Database (from the virtual environment):

Create a new database in PostgreSQL.
In the database.py file, set the DB_NAME field to the name of the created database.
Input the command alembic revision --autogenerate -m "Initial migration" in the terminal.
Then, input the command alembic upgrade head in the terminal.
