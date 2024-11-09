from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import db
from controller import MetricsController
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
from schemas import Metrics
from utils import parse_date
import numpy as np

# Create All Required MYSQL Tables.
db.create_tables()
app = FastAPI()


@app.post("/compute-metrics/")
async def compute_metrics(profile_file: UploadFile = File(...), posts_file: UploadFile = File(...), db: Session = Depends(db.get_db)):
    if profile_file.content_type != 'text/csv' or posts_file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload CSV files.")

    # Read CSV files
    profile_content=await profile_file.read()
    post_content= await posts_file.read()
    profile_df = pd.read_csv(StringIO(profile_content.decode('utf-8')))
    posts_df = pd.read_csv(StringIO(post_content.decode('utf-8')))
    # Tackling NaN and inf cases as the csv file can have some empty fields. This replaces that with 0.
    profile_df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    posts_df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    profile_data = profile_df.to_dict(orient="records")[0]
    posts_data = posts_df.to_dict(orient="records")

    # Filter posts from the last 3 months
    three_months_ago = datetime.now() - timedelta(days=90)
    recent_posts = [post for post in posts_data if parse_date(post['pub_date']) >= three_months_ago]

    # Initialize controller with DB session
    metrics_controller = MetricsController(db)

    # Calculate and store metrics
    active_reach = metrics_controller.calculate_active_reach(recent_posts)
    emv = metrics_controller.calculate_emv(profile_data['followers'], recent_posts)
    average_engagements = metrics_controller.calculate_average_engagements(recent_posts)
    average_video_views = metrics_controller.calculate_average_video_views(recent_posts)
    average_story_reach = metrics_controller.calculate_average_story_reach(recent_posts)
    average_story_engagements = metrics_controller.calculate_average_story_engagements(recent_posts)
    average_story_views = metrics_controller.calculate_average_story_views(recent_posts)
    average_saves = metrics_controller.calculate_average_saves(recent_posts)
    average_likes = metrics_controller.calculate_average_likes(recent_posts)
    average_comments = metrics_controller.calculate_average_comments(recent_posts)
    average_shares = metrics_controller.calculate_average_shares(recent_posts)
    followers=metrics_controller.get_total_followers(profile_data)
    country=metrics_controller.get_country(profile_data)
    username=metrics_controller.get_username(profile_data)
    profileURL=metrics_controller.get_profile_url(profile_data)
    postCount=metrics_controller.get_post_count(recent_posts)
    # Store all metrics at once
    metrics_controller.store_metrics(profile_data['sila_id'], {
        "id" : profile_data["user_id"],
        'active_reach': active_reach,
        "followers":followers,
        "country":country,
        "username":username,
        "profileUrl":profileURL,
        "postCount":postCount,
        'emv': emv,
        'average_engagements': average_engagements,
        'average_video_views': average_video_views,
        'average_story_reach': average_story_reach,
        'average_story_engagements': average_story_engagements,
        'average_story_views': average_story_views,
        'average_saves': average_saves,
        'average_likes': average_likes,
        'average_comments': average_comments,
        'average_shares': average_shares
    })

    # Calculate metrics by content category
    metrics_paid, metrics_organic = metrics_controller.compute_metrics_by_category(profile_data,posts_data)

    return {
        "metrics_paid": metrics_paid,
        "metrics_organic": metrics_organic,
    }

@app.get("/metrics/{username}", response_model=list[Metrics])
def read_metrics(username: str, db: Session = Depends(db.get_db)):
    metrics_controller = MetricsController(db)
    metrics = metrics_controller.get_metrics_by_username(username)
    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics