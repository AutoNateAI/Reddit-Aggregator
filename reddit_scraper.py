import praw
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Step 1: Setup Reddit API Client using PRAW
def reddit_client():
    """
    Creates a Reddit API client using PRAW.

    Returns:
    -------
    praw.Reddit
        The authenticated Reddit client object.
    """
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,  # Replace with your Reddit API client ID
        client_secret=REDDIT_CLIENT_SECRET,  # Replace with your Reddit API client secret
        user_agent=REDDIT_USER_AGENT,  # Replace with your user agent
    )

# Step 2: Function to Extract Data from Reddit Posts with Filter Options
def extract_post_data(subreddit_name, limit=10, filter_type='new'):
    """
    Extracts title, text, time posted, and poster ID from Reddit posts based on a filter type.

    Parameters:
    ----------
    subreddit_name : str
        The name of the subreddit to extract data from (e.g., 'python').
    limit : int, optional
        The number of posts to extract (default is 10).
    filter_type : str, optional
        The type of filtering for subreddit posts: 'new', 'hot', 'top', 'rising' (default is 'new').

    Returns:
    -------
    pd.DataFrame
        A pandas DataFrame containing the extracted post data.
    """
    reddit = reddit_client()
    subreddit = reddit.subreddit(subreddit_name)

    # Initialize an empty list to store post data
    post_data = []

    # Filter posts based on the filter_type parameter
    if filter_type == 'new':
        posts = subreddit.new(limit=limit)
    elif filter_type == 'hot':
        posts = subreddit.hot(limit=limit)
    elif filter_type == 'top':
        posts = subreddit.top(limit=limit)
    elif filter_type == 'rising':
        posts = subreddit.rising(limit=limit)
    else:
        raise ValueError("Invalid filter_type. Use 'new', 'hot', 'top', or 'rising'.")

    # Loop through the filtered posts and extract the necessary information
    for post in posts:
        post_info = {
            'title': post.title,
            'text': post.selftext,  # This is the post body
            'time_posted': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'poster_id': post.author.name if post.author else 'N/A'  # Some posts may have deleted users
        }
        post_data.append(post_info)
    return post_data

# Example Usage
if __name__ == "__main__":
    import pprint
    subreddit_name = 'python'  # Replace with the subreddit you want to scrape
    data = extract_post_data(subreddit_name, limit=10, filter_type='hot')  # Change filter_type as needed
    pprint.pprint(data)
