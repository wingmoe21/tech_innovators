import os

from openai import OpenAI


def get_quiz(file_path):
    os.environ["OPENAI_API_KEY"] = "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"
    client = OpenAI()

    with open(file_path, 'r') as file:
        text_content = file.read()

    query = """I'm using you as an API with automated requests that primarily have text files contains lecture material in them and nothing else.  Your goal is to extract the info from them then, make three questions with three choices and their answers.

The input will always be of this form:
<long text>

And I want you to respond always, without fail, in this form:

Question 1:
<question 1>
A) <first choice>
B) <second choice>
C) <third choice>
Answer: <Correct answer>

Question 2:
<question 2>
A) <first choice>
B) <second choice>
C) <third choice>
Answer: <Correct answer>

Question 3:
<question 3>
A) <first choice>
B) <second choice>
C) <third choice>
Answer: <Correct answer>

Meaning you should only respond with the explained summarized text. There is no limit for how many words you write."""
    
    combined_prompt = f"{query}\n\n{text_content}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": combined_prompt}
        ]
    )
    result = response.choices[0].message.content

    # Splitting the string into parts for each question
    questions = result.split("Question ")
    # Processing each question to extract the desired parts
    sliced_parts = {}
    for q in questions[1:]:  # skipping the first split part as it's not a question
        lines = q.split("\n")
        question_number = lines[0].strip(":")
        question = lines[1]
        choices = lines[2:5]
        answer_line = lines[5].split(": ")
        answer = answer_line[1] if len(answer_line) > 1 else "Unknown"
        # Storing in a dictionary
        sliced_parts[f"Question {question_number}"] = question
        for i, choice in enumerate(choices):
            choice_parts = choice.split(") ")
            sliced_parts[f"q{question_number[-1]}c{i+1}"] = choice_parts[1] if len(choice_parts) > 1 else "Unknown"
        sliced_parts[f"q{question_number[-1]}ans"] = answer
        
    return sliced_parts