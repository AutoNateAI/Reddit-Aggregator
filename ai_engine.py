from openai import OpenAI
from dotenv import load_dotenv
import os, json
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_post_info(title, content, subreddit, category):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an AI assistant tasked with extracting structured data from online Reddit posts.
                I will provide you with a title, the full text of a post, the subreddit, and the category of the subreddit.
                Please analyze the post and extract the following information:

                1. All topics discussed.
                2. All specific questions or requests made.
                3. Relevant keywords and phrases.
                4. Sentiment is a list of contextualized sentiments -> here are examples of some (positive, negative, neutral, looking_for_help, angry, confused, excited, afraid, promoting.).
                5. Any explicit actions or next steps based on the content in the post or the title that I can react to help?
                6. A 75-word max summary of the post given that the goal is to help them by providing a ChatGPT prompt that will guide them through their issue.
                7. Provide 3 optimal responses that help the user if the sentiment shows they are looking for help. These should create prompts that the user can use inside ChatGPT to walk them through their issue. Also give advice on how LLMs are perfect to explore questions and using YouTube as a guide will help tremendously.

                Return the information in the following JSON structure:
                
                {{
                    "title": "{title}",
                    "subreddit": "{subreddit}",
                    "category": "{category}",
                    "topics_discussed": [],
                    "questions_requests": [],
                    "keywords": [],
                    "sentiment": [],
                    "actions_next_steps": [],
                    "summary": "",
                    "suggested_responses": []
                }}
                """
            },
            {
                "role": "user",
                "content": f"Title: {title}\nContent: {content}\nSubreddit: {subreddit}\nCategory: {category}"
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "post_extraction_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "subreddit": {"type": "string"},
                        "category": {"type": "string"},
                        "topics_discussed": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "questions_requests": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "sentiment": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "actions_next_steps": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "summary": {"type": "string"},
                        "suggested_responses": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                    },
                    "additionalProperties": False
                }
            }
        }
    )

    # Get the json back from OpenAI in string format
    str_json = response.choices[0].message.content

    # Convert it to a Python object
    data_obj = json.loads(str_json)

    # Add the current time for when the data was scraped
    data_obj["time_scraped"] = datetime.now().isoformat()

    return data_obj

if __name__ == "__main__":
    import pprint
    # Example Usage
    title = "How to Learn Python Effectively"
    content = "I am trying to learn Python but I am not sure where to start. What are the best resources?"
    subreddit = "learnpython"
    category = "Education"
    json_output = extract_post_info(title, content, subreddit, category)
    pprint.pprint(json_output)
