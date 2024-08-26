from openai import OpenAI
from  time import sleep

OPENAI_API_KEY = 'Here have to be ACCESS KEY'

client = OpenAI(api_key=OPENAI_API_KEY)

def ai_response(task):
    goal = f"Breakdown this problem on small 3 steps as for ADHD or  OCD for me, and less text as possible {task}. And return as plain text"
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {f"role": "user", "content": goal}
    ]
)
    sleep(1)
    return completion.choices[0].message.content
    
    

