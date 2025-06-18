from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate



# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Use a strong secret key

# Dummy user store for example
users = {}  # You can use a DB or file later


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details. If the answer is not in
    the provided context, just say "answer is not available in the context". Don't guess.\n\n
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def get_response(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['user'] = uname
            return redirect(url_for('chatbot'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users:
            return "User already exists"
        users[uname] = pwd
        return redirect(url_for('login'))
    return render_template('register.html')
from markupsafe import Markup

def format_answer(text):
    formatted = ""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("*"):
            formatted += f"<li>{line[1:].strip()}</li>"
        elif line:
            formatted += f"<p>{line}</p>"
    if "<li>" in formatted:
        formatted = "<ul>" + formatted + "</ul>"
    return Markup(formatted)

def get_pdf_answer(question):
    raw_answer = get_response(question)
    return format_answer(raw_answer)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        question = request.form['question']
        answer = get_pdf_answer(question)


        session['chat_history'].append({'question': question, 'answer': answer})
        session.modified = True

    return render_template('chatbot.html', chat_history=session.get('chat_history', []))
@app.route('/clear_chat')
def clear_chat():
    session.pop('chat_history', None)  # Removes saved chat history from session
    return redirect(url_for('chatbot'))  # Redirects back to chatbot page


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
