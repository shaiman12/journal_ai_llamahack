from openai import OpenAI


def send_to_chatgpt(message):
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",  # or another model you prefer
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"