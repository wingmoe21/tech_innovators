import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

os.environ["OPENAI_API_KEY"] = "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"

def get_quiz(file_path):
    query = "Extract all info. Then, make three questions with three choices and their answers."
    loader = TextLoader(file_path)
    index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    chat_history = []
    result = chain({"question": query, "chat_history": chat_history})
    # Splitting the string into parts for each question
    questions = result['answer'].split("Question ")
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