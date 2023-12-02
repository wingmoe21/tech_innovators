import os

from openai import OpenAI


def get_summary_gpt(file_path):

    os.environ["OPENAI_API_KEY"] = "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"
    client = OpenAI()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

    except FileNotFoundError:
        print(f"file not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

    prompt1 = """
I'm using you as an API with automated requests that only have text in them about a lecture and nothing else. And I want you  to generate a summary for the text.
And I want you to respond always, without fail, if a gave you a text then you will generate the summary as short as possible.
If you were able to generate summary, then I want you to always (with no exception) write it in the following way:
If I sent:  text
Your response should be just the summary
Meaning you should only respond with the summary
"""

    combined_prompt = f"{prompt1}\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": combined_prompt}
        ]
    )
    return response.choices[0].message.content