## User Social Media Metrics

This app utilizes FastAPI, Pandas and SQLAlchemy(ORM) to make an API to calculate, store and fetch user's social media metrics.

## Running Instructions

### Run Locally

Switch to the python environment:

```
source env/bin/activate
```

Run the server locally:

```
fastapi dev app/main.py
```

### Run on containers

Run the containers using `docker-compose`:

```
docker-compose up --build
```
