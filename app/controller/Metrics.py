from sqlalchemy.orm import Session
from datetime import datetime
import numpy as np
from models import Metrics as MetricsModel,Profile
from schemas import Metrics

class MetricsController:
    def __init__(self, db: Session):
        self.db = db

    def calculate_active_reach(self, posts):
        total_likes = sum(post['like_count'] for post in posts)
        total_comments = sum(post['comment_count'] for post in posts)
        total_views = sum(post['view_count'] for post in posts if 'view_count' in post)
        total_posts = len(posts)
        return (total_likes + total_comments + total_views) / total_posts if total_posts else 0

    def calculate_emv(self, followers, posts):
        comments = sum(post['comment_count'] for post in posts)
        likes = sum(post['like_count'] for post in posts)
        plays = sum(post['play_count'] for post in posts if 'play_count' in post)
        return (followers / 1000 * 2.1) + (comments * 4.19) + (likes * 0.09) + (plays * 0.11)

    def calculate_average_engagements(self, posts):
        total_engagements = sum(post['like_count'] + post['comment_count'] + post.get('share_count', 0) + post.get('save_count', 0) for post in posts)
        return total_engagements / len(posts) if posts else 0

    def calculate_average_video_views(self, posts):
        video_views = [post['view_count'] for post in posts if 'view_count' in post]
        return np.mean(video_views) if video_views else 0

    def calculate_average_story_reach(self, posts):
        story_reach = [post['story_reach'] for post in posts if 'story_reach' in post]
        return np.mean(story_reach) if story_reach else 0

    def calculate_average_story_engagements(self, posts):
        story_engagements = [post['story_engagements'] for post in posts if 'story_engagements' in post]
        return np.mean(story_engagements) if story_engagements else 0

    def calculate_average_story_views(self, posts):
        story_views = [post['story_views'] for post in posts if 'story_views' in post]
        return np.mean(story_views) if story_views else 0

    def calculate_average_saves(self, posts):
        saves = [post['saves'] for post in posts if 'saves' in post]
        return np.mean(saves) if saves else 0

    def calculate_average_likes(self, posts):
        likes = [post['like_count'] for post in posts]
        return np.mean(likes) if likes else 0

    def calculate_average_comments(self, posts):
        comments = [post['comment_count'] for post in posts]
        return np.mean(comments) if comments else 0

    def calculate_average_shares(self, posts):
        shares = [post['share_count'] for post in posts if 'share_count' in post]
        return np.mean(shares) if shares else 0

    def determine_content_type(self, posts):
        # Determine if content is paid or organic based on post description
        return ["Paid" if '@' in post['description'] or 'اعلان' in post['description'] else "Organic" for post in posts]

    def get_country(self, profile):
        return profile['country']

    def get_total_followers(self, profile):
        return profile['followers']

    def get_profile_url(self, profile):
        return profile['profile_url']

    def get_media_type(self, posts):
        return [post['product_type'] for post in posts if 'product_type' in post]

    def get_post_count(self, posts):
        return len(posts)

    def get_username(self, profile):
        return profile['username']

    def store_metrics(self, profile_id: int, metrics_dict: dict):
        # Create a new Metrics instance with all metric values from the dictionary
        new_metrics = Metrics(
            id=metrics_dict.get("id"),
            profile_id=profile_id,
            followers=metrics_dict.get("followers"),
            country=metrics_dict.get("country"),
            username=metrics_dict.get("username"),
            profileUrl=metrics_dict.get("profileUrl"),
            postCount=metrics_dict.get("postCount"),
            active_reach=metrics_dict.get('active_reach'),
            emv=metrics_dict.get('emv'),
            average_engagements=metrics_dict.get('average_engagements'),
            average_video_views=metrics_dict.get('average_video_views'),
            average_story_reach=metrics_dict.get('average_story_reach'),
            average_story_engagements=metrics_dict.get('average_story_engagements'),
            average_story_views=metrics_dict.get('average_story_views'),
            average_saves=metrics_dict.get('average_saves'),
            average_likes=metrics_dict.get('average_likes'),
            average_comments=metrics_dict.get('average_comments'),
            average_shares=metrics_dict.get('average_shares'),
            calculation_date=datetime.now()  # Record the time when the metrics were calculated
        )
        self.db.add(new_metrics)  # Add the new metrics record to the session
        self.db.commit()          # Commit the transaction to save the record to the database
        return new_metrics        # Return the newly created metrics record

    def classify_posts(self, posts):
        # Classify posts as 'Paid' or 'Organic'
        for post in posts:
            if '@' in post['description'] or 'اعلان' in post['description']:
                post['content_type'] = 'Paid'
            else:
                post['content_type'] = 'Organic'
        return posts

    def compute_metrics_by_category(self, posts):
        # Classify posts
        posts = self.classify_posts(posts)

        # Divide posts into categories
        paid_posts = [post for post in posts if post['content_type'] == 'Paid']
        organic_posts = [post for post in posts if post['content_type'] == 'Organic']

        # Calculate metrics for each category
        metrics_paid = self.calculate_all_metrics(paid_posts)
        metrics_organic = self.calculate_all_metrics(organic_posts)
        return metrics_paid, metrics_organic

    def get_metrics_by_username(self, username: str):
        # Query the Profile to get the profile ID based on the username
        profile = self.db.query(Profile).filter(Profile.username == username).first()
        if not profile:
            return None  # Return None if no profile is found

        # Use the profile ID to retrieve the associated metrics
        metrics = self.db.query(MetricsModel).filter(MetricsModel.profile_id == profile.id).all()
        return [Metrics.from_orm(metric) for metric in metrics] if metrics else []

    def calculate_all_metrics(self, posts):
        total_followers = self.get_total_followers()  # Adjust this to ensure it fetches the right number of followers
        return {
            'active_reach': self.calculate_active_reach(posts),
            'emv': self.calculate_emv(total_followers, posts),
            'average_engagements': self.calculate_average_engagements(posts),
            'average_video_views': self.calculate_average_video_views(posts),
            'average_story_reach': self.calculate_average_story_reach(posts),
            'average_story_engagements': self.calculate_average_story_engagements(posts),
            'average_story_views': self.calculate_average_story_views(posts),
            'average_saves': self.calculate_average_saves(posts),
            'average_likes': self.calculate_average_likes(posts),
            'average_comments': self.calculate_average_comments(posts),
            'average_shares': self.calculate_average_shares(posts),
            'content_type_distribution': self.determine_content_type(posts)  # This computes the distribution of content types
        }