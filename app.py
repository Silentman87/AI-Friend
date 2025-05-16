#############################################################################
#                      AI-Friend | Ai-powered health &                      #
#                          emotional support chatbot                        #
#                                                                           #             
#                                                                           #
#############################################################################


#############################################################################
#  Importing library
#
#############################################################################

from flask import Flask, render_template, redirect, url_for, request, flash, Response
import flask
from requests import session
from datetime import datetime, timedelta
from flask import jsonify
from flask import session
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from src.prompt import *
import os



app = Flask(__name__)

#############################################################################
#  setting the environment variables
#
#############################################################################


load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["HUGGINGFACE_API_KEY"] = HUGGINGFACE_API_KEY


#############################################################################
#  Download the embedding model
#
#############################################################################

embeddings = download_hugging_face_embeddings()

#############################################################################
#  Extracting the data from Pinecone vector DB
#
#############################################################################

index_name = "aifriend"
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type = "similarity", search_kwargs={"k":3})

#############################################################################
#  Load the large language model using groq api
#
#############################################################################
llm = ChatGroq(model="llama3-70b-8192", temperature=0.5, max_tokens=500)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


#############################################################################
#  Creating a chain
#
#############################################################################

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


#############################################################################
#  Setting up the routes
#
#############################################################################

@app.route('/', methods = ['GET', 'POST'])
def login():
    return render_template('index.html')



@app.route('/register', methods = ['GET'])
def register() :
    return render_template('register.html')


@app.route('/home', methods=['GET', 'POST'])
def home() :
    return render_template('home.html')



@app.route("/chat", methods = ["GET", "POST"])
def chat() :

    data = request.get_json()
    message = data.get("message", "No message")
    type_ = data.get("type", "No type")
    history = data.get("history", [])
    print("Message:", message)
    print("Type:", type_)
    print(history)

    # Join history into text format
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
    
    if not data or "message" not in data or "type" not in data:
        return jsonify({"error": "No message provided"}), 400
    
    # for friend mode 
    
    if data["type"] == "friend":
        try:
            # direct pass to the llm for input generation
            response = llm([
                SystemMessage(content=friend_prompt),
                HumanMessage(content=message)
            ])
            print("Friend response:", response.content)
            return jsonify({"response": response.content})
        except Exception as e:
            print("LLM Error (friend):", str(e))
            return jsonify({"error": "Sorry yaar, kuch gadbad ho gayi. Try again later."}), 500

    # for health-guide mode
    elif data["type"] == "health-guide":
        try:
            # first pass to the rag_chain() for input generation
            response = rag_chain.invoke({"input": message})
            print("Health response:", response["answer"])
            return jsonify({"response": response["answer"]})
        except Exception as e:
            print("RAG Error (health-guide):", str(e))
            return jsonify({"error": "Oops! Health guide is not responding right now."}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug = True)