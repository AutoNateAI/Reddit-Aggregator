import time
import praw  # Reddit API
from datetime import datetime
from ai_engine import extract_post_info 
from dotenv import load_dotenv
from db import connect_to_db, save_post_to_db
import os

load_dotenv()

# Reddit API setup
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Sample category and subreddit list
subreddit_categories = [
    {
        "category": "Education",
        "subreddits": ["learnpython", "MachineLearning", "python"]
    },
    {
        "category": "Technology",
        "subreddits": ["technology", "programming", "gadgets"]
    }
]

def fetch_and_aggregate_data(interval=3600):
    """
    Function that runs on a loop and grabs the most recent post from each subreddit.
    The interval can be set in seconds, default is 1 hour (3600 seconds).
    """
    while True:
        for category_obj in subreddit_categories:
            category = category_obj["category"]
            subreddits = category_obj["subreddits"]

            for subreddit_name in subreddits:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Grab the most recent post
                for post in subreddit.new(limit=1):
                    title = post.title
                    content = post.selftext
                    posted_time = datetime.fromtimestamp(post.created_utc)
                    reddit_user_id = post.author.name

                    # Call the AI function to extract relevant info
                    extracted_info = extract_post_info(title, content, subreddit_name, category)

                    # Add the posted time before uploading to the database
                    extracted_info["time_created"] = posted_time.isoformat()

                    extracted_info["category"] = category

                    # Save data to db
                    save_post_to_db(extracted_info, reddit_user_id)


        # Wait for the next iteration
        print(f"Waiting {interval} seconds for the next run...")
        time.sleep(interval)



if __name__ == "__main__":
    connect_to_db()
    fetch_and_aggregate_data()
