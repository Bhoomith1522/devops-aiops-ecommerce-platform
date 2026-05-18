from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_log(log_message):

    prompt = f"""
    Analyze this DevOps system log and explain:
    1. Possible issue
    2. Root cause
    3. Suggested fix

    Log:
    {log_message}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content