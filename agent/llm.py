import openai


def generate_tweet(articles: list[str]):
    messages = [
        {"role": "system", "content": "Generate a single tweet with the information provided."}
    ] + [{"role": "user", "content": article} for article in articles]

    client = openai.OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
    )


    return response.choices[0].message.content
