from telegram import Bot
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
import re

load_dotenv()

TELEGRAM_BOT_PYTHON_GUIDANCE_API_KEY = os.getenv("TELEGRAM_BOT_PYTHON_GUIDANCE_API_KEY")
TELEGRAM_BOT_SAAS_CREATION_API_KEY = os.getenv("TELEGRAM_BOT_SAAS_CREATION_API_KEY")


py_bot = Bot(token=TELEGRAM_BOT_PYTHON_GUIDANCE_API_KEY)
saas_bot = Bot(token=TELEGRAM_BOT_SAAS_CREATION_API_KEY)

def escape_html(text):
    """
    Escape special characters for HTML formatting in Telegram.
    """
    return re.sub(r'([&<>])', lambda x: {'&': '&amp;', '<': '&lt;', '>': '&gt;'}.get(x.group(), x.group()), text)

async def send_to_telegram(chat_id, extracted_data, category):
    """
    Sends a formatted HTML message to the specified Telegram chat using the extracted_data object.
    """
    title = escape_html(extracted_data.get('title', 'N/A'))
    topics = escape_html(', '.join(extracted_data.get('topics_discussed', [])))
    sentiment = escape_html(', '.join(extracted_data.get('sentiment', [])))
    action_to_take = escape_html(', '.join(extracted_data.get('actions_next_steps', [])))
    suggested_response = escape_html(extracted_data.get('suggested_responses', ['No response available'])[0])
    summary = escape_html(extracted_data.get('summary', 'No summary available'))
    post_url = f"https://www.reddit.com/r/{extracted_data["subreddit"]}/comments/{escape_html(extracted_data.get('reddit_post_id', ''))}"

    message = (
        f"<b>Title</b>: {title}\n"
        f"<b>Topics</b>: {topics}\n"
        f"<b>Sentiment</b>: {sentiment}\n"
        f"<b>Action To Take</b>: {action_to_take}\n"
        f"<b>Suggested Response</b>: {suggested_response}\n"
        f"<b>Summary</b>: {summary}\n"
        f"<b>Post URL</b>: {post_url}"
    )
    if category == "Teaching Python":
        await py_bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
    elif category == "SaaS Development":
        await saas_bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)

# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        chat_id = "5871291837"  # Replace with your chat_id
        chat_id2 = "5871291837"
        extracted_data = {
            "title": "Example Post",
            "topics_discussed": ["Topic 1", "Topic 2"],
            "sentiment": ["positive"],
            "actions_next_steps": ["Engage with community"],
            "suggested_responses": ["This is a helpful response."],
            "summary": "This post discusses AI and ML trends.",
            "reddit_post_id": "t3_abc123"
        }
        await send_to_telegram(chat_id, extracted_data)

    asyncio.run(main())
