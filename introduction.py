from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def introduction(name, bio, response, availability):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    try:
        prompt = (
            f"Please format an introduction for a person based on the following details, it would be for introducing this person to someone else so they can plan to meet later. Keep it short and follow the general example that i have given you:\n"
            f"Name: {name}\n"
            f"Bio: {bio}\n"
            f"Current Situation: {response}\n"
            f"Availability: {availability}\n\n"
            f"Example:\n"
            f"I want to introduce you to Sarah. She's a 28-year-old software engineer who loves hiking and sci-fi movies. "
            f"Right now, she's thinking about changing careers and feeling a bit nervous but excited about it. "
            f"She's looking for guidance on career transitions. She usually likes to meet on weekends."
        )

        completion = client.chat.completions.create(
            model="gpt-4",  # You can adjust the model as needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates introductions."},
                {"role": "user", "content": prompt}
            ]
        )

        introduction_text = completion.choices[0].message.content
        print(introduction_text)
        return introduction_text
    except Exception as e:
        # Handle exceptions, e.g., API issues or connectivity problems
        return f"An error occurred: {str(e)}"