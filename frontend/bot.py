import os
import sys

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from openai import OpenAI


def bot(file_path, user_input):
    #كود الشات
    os.environ["OPENAI_API_KEY"] = "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"

    # Enable to save to disk & reuse the model (for repeated queries on the same data)
    PERSIST = False

    query = user_input
    if len(sys.argv) > 1:
        query = sys.argv[1]

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = TextLoader(file_path)  # Use this line if you only need data.txt
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )

    chat_history = []
    while True:

        if query in ['quit', 'q', 'exit']:
            sys.exit()

        result = chain({"question": query, "chat_history": chat_history})

        if result['answer'] and "I don't know" not in result['answer'] and "I don't have " not in result['answer'] and "I'm sorry" not in result['answer']and "There is no mention" not in result['answer']:
            # If there is a valid answer from the file, use it
            chat_history.append((query, result['answer']))
            query = None
            return result['answer']
        else:
            # If the response is still "I don't have enough information," try GPT external
            client = OpenAI()
            gpt_response_external = response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=query
                )


            result['answer'] = gpt_response_external.choices[0].text
            chat_history.append((query, result['answer']))
            query = None
            return result['answer']

