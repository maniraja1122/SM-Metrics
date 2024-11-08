from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import numpy as np

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