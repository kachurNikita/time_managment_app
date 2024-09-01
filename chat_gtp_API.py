from openai import OpenAI
from time import sleep
import requests
import openai

# Access key which is generated when account created 
OPENAI_API_KEY = 'Access key'

# OpenAI instance
client = OpenAI(api_key=OPENAI_API_KEY)

# Function which allows connect to chatgpt API and retrieve task breakdown in order to help us complete task
def chat_gpt_response(task):
    try:
        goal = f'''i have OCD! And i am asking you to breakdown each task on small steps to help me to start,
        do, and finish particular task. I want retreive just plain text without yours comments.
        And each response have to have same amount of charactres. Here is the task {task}'''
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
        {f"role": "user", "content": goal}
        ]
    )
        return completion.choices[0].message.content
    except openai.APIError as e:
  #Handle API error here, e.g. retry or log
        return f'OpenAI API returned an API Error: {e}'
        pass
    except openai.APIConnectionError as e:
  #Handle connection error here
        return f'Failed to connect to OpenAI API: {e}'
        pass
    except openai.RateLimitError as e:
        return f'OpenAI API request exceeded rate limit: {e}'
        pass