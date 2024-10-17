from dotenv import load_dotenv
from mongoengine import DoesNotExist
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, connect
import os, datetime

load_dotenv()

MONGODB_PWD = os.getenv("MONGODB_PWD")
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_CLUSTER_URL = os.getenv("MONGODB_CLUSTER_URL")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

connection_string = f"mongodb+srv://{MONGODB_USER}:{MONGODB_PWD}@{MONGODB_CLUSTER_URL}/?retryWrites=true&w=majority&appName=Cluster0"

# connect to db
def connect_to_db(): 
    
    # Connect to the database
    try:
        connect(MONGODB_DATABASE, host=connection_string)
        print("Connected to the MongoDB Atlas database!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

# Define the ORM models (collections) for MongoDB using mongoengine

class User(Document):
    """
    This class represents a Reddit user and will be stored in the 'users' collection.
    
    Attributes:
    ----------
    reddit_user_id : str
        The unique Reddit user ID (e.g., 'u/example_user').
    username : str
        The Reddit username.
    created_at : datetime
        Timestamp for when the user was first encountered.
    """
    reddit_user_id = StringField(required=True, unique=True)
    username = StringField(required=True)
    created_at = DateTimeField(required=True)

    meta = {'collection': 'users'}

class Post(Document):
    """
    This class represents a Reddit post and will be stored in the 'posts' collection.

    Attributes:
    ----------
    reddit_post_id : str
        The unique Reddit post ID (e.g., 't3_abc123').
    subreddit : str
        The subreddit where the post was made.
    created_at : datetime
        Timestamp for when the post was created.
    title : str
        Title of the Reddit post.
    reddit_user_id : str
        The Reddit user ID of the user who made the post.
    sentiment : str
        Sentiment label (e.g., 'positive', 'neutral', 'negative').
    action_type : str
        The action type (e.g., 'promoting', 'asking for help', 'sharing a story').
    keywords : list
        A list of keywords associated with the post (linked to the 'Keyword' collection).
    topics : list
        A list of topics associated with the post (linked to the 'Topic' collection).
    """
    reddit_post_id = StringField(required=True, unique=True)
    subreddit = StringField(required=True)
    created_at = DateTimeField(required=True)
    title = StringField(required=True)
    reddit_user_id = StringField(required=True)
    sentiment = StringField()
    action_type = StringField()
    
    # Many-to-One relationships with Keywords and Topics
    keywords = ListField(ReferenceField('Keyword'))
    topics = ListField(ReferenceField('Topic'))

    meta = {'collection': 'posts'}

class Topic(Document):
    """
    This class represents a topic associated with a Reddit post and is stored in the 'topics' collection.

    Attributes:
    ----------
    post : Post
        Reference to the post this topic is associated with.
    topic : str
        The extracted topic from the Reddit post.
    created_at : datetime
        Timestamp for when the topic was created.
    """
    post = ReferenceField(Post, reverse_delete_rule='CASCADE')
    topic = StringField(required=True)
    created_at = DateTimeField(required=True)

    meta = {'collection': 'topics'}

class Keyword(Document):
    """
    This class represents a keyword associated with a Reddit post and is stored in the 'keywords' collection.

    Attributes:
    ----------
    post : Post
        Reference to the post this keyword is associated with.
    keyword : str
        The extracted keyword from the Reddit post.
    created_at : datetime
        Timestamp for when the keyword was created.
    """
    post = ReferenceField(Post, reverse_delete_rule='CASCADE')
    keyword = StringField(required=True)
    created_at = DateTimeField(required=True)

    meta = {'collection': 'keywords'}


# Connect to the MongoDB database
def connect_to_db():
    try:
        connect(MONGODB_DATABASE, host=connection_string)
        print("Connected to the MongoDB Atlas database!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

def save_post_to_db(extracted_data, reddit_user_id):
    """
    Function to save the scraped post data to the MongoDB database.
    This function checks if the user already exists and if the post is already saved,
    then it saves the post, topics, and keywords.
    """

    # Check if user exists, otherwise create a new user
    try:
        user = User.objects.get(reddit_user_id=reddit_user_id)
    except DoesNotExist:
        user = User(
            reddit_user_id=reddit_user_id,
            username=reddit_user_id,  # Assumes you are using reddit_user_id as the username (you can modify this)
            created_at=datetime.datetime.now()
        )
        user.save()

    # Save the post
    post = Post(
        reddit_post_id=extracted_data['title'],  # You might have another ID for Reddit post, adjust if needed
        subreddit=extracted_data['subreddit'],
        created_at=extracted_data['time_scraped'],
        title=extracted_data['title'],
        reddit_user_id=user.reddit_user_id,
        sentiment=', '.join(extracted_data['sentiment']),
        action_type=', '.join(extracted_data['actions_next_steps']),
        keywords=[],  # Will add keywords separately
        topics=[]  # Will add topics separately
    )
    post.save()

    # Save associated topics
    for topic in extracted_data['topics_discussed']:
        topic_obj = Topic(
            post=post,
            topic=topic,
            created_at=datetime.datetime.now()
        )
        topic_obj.save()
        post.topics.append(topic_obj)

    # Save associated keywords
    for keyword in extracted_data['keywords']:
        keyword_obj = Keyword(
            post=post,
            keyword=keyword,
            created_at=datetime.datetime.now()
        )
        keyword_obj.save()
        post.keywords.append(keyword_obj)

    # Save the post again to update with references to topics and keywords
    post.save()

    
if __name__ == "__main__":
    connect_to_db()

