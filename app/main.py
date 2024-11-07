from fastapi import FastAPI, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pandas as pd
from io import StringIO
import db

db.create_tables()
app = FastAPI()


@app.post("/compute-metrics/")
async def compute_metrics(profile_file: UploadFile, posts_file: UploadFile, db: Session = Depends(db.get_db)):
    if profile_file.content_type != 'text/csv' or posts_file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload CSV files.")

    # Read CSV files
    profile_df = pd.read_csv(StringIO(str(profile_file.file.read(), 'utf-8')))
    posts_df = pd.read_csv(StringIO(str(posts_file.file.read(), 'utf-8')))

    # Filter posts from the last 3 months
    three_months_ago = datetime.now() - timedelta(days=90)
    recent_posts = posts_df[posts_df['pub_date'] >= three_months_ago]

    # Compute metrics
    metrics_data = crud.compute_and_store_metrics(profile_df, recent_posts, db)
    return {"message": "Metrics computed and stored", "data": metrics_data}

@app.get("/metrics/{username}", response_model=schemas.Metrics)
def read_metrics(username: str, db: Session = Depends(db.get_db)):
    db_metrics = crud.get_metrics_by_username(username, db)
    if db_metrics is None:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return db_metrics

