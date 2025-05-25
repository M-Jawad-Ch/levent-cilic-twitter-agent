import openai


def generate_tweet(articles: list[str], instructions: str):
    messages = [
        {
            "role": "system",
            "content": instructions,
        }
    ] + [{"role": "user", "content": article} for article in articles]

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
    )

    text = response.choices[0].message.content

    for _ in range(5):
        if len(text) < 240:
            break

        messages += [
            {"role": "assistant", "content": text},
            {
                "role": "user",
                "content": "This exceeds the character limit of 240 characters. Make it smaller.",
            },
        ]

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7,
        )

        text = response.choices[0].message.content

    return text


def summarise_page(html: str):
    
    return html

    messages = [
        {
            "role": "system",
            "content": "You summarise raw webpages and extract their text",
        },
        {"role": "user", "content": html},
    ]

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content
