🚀 ScrollBot — An intelligent PDF chatbot using RAG with Google GenAI, Flask, and FAISS.

ScrollBot is an AI-powered assistant that lets students interact with academic PDFs—like syllabus documents, past year question papers, and more—through natural language questions. Built using a Retrieval-Augmented Generation (RAG) approach, it transforms traditional, non-interactive PDFs into a smart, conversational experience. Whether you're preparing for exams or exploring your course structure, ScrollBot makes it easy to access the information you need—fast and effortlessly.


🗂️ Project Structure
bash
Copy
Edit
RAGBASED-PDFINTERACTION-CHATBOT/
│
├── faiss_index/         # Stores FAISS vector database
│   ├── index.faiss
│   └── index.pkl
│
├── templates/           # Flask HTML templates
│   ├── chatbot.html
│   ├── login.html
│   └── register.html
│
├── images/              # UI/branding screenshots (for README or UI assets)
│
├── .env                 # Environment variables (e.g., API keys)
├── app.py               # Main Flask application (routing + frontend logic)
├── fiass.py             # FAISS + PDF processing logic (backend intelligence)
├── test.py              # For debugging or testing routes
├── requirements.txt     # Python dependencies
└── README.md            # You're reading it!
🧠 How It Works
This RAG-based system uses the following workflow:

PDF Upload & Text Chunking
Documents are loaded and split into manageable chunks.

Semantic Vectorization
Each chunk is transformed using Google Gen AI Embeddings.

Indexing via FAISS
Vectors are stored in a FAISS vector store for fast similarity search.

User Interaction
User input is sent through the UI, and the system retrieves and responds using the most relevant document segments.

🌐 Web Interface (Frontend)
🔐 Login/Register
Your app starts with user authentication via clean and simple forms.

html
Copy
Edit
templates/
├── login.html
├── register.html
└── chatbot.html
💬 ScrollBot Chat Page
Once logged in, users can begin chatting with ScrollBot:

Welcome message, logout/clear options, and a smooth modern design using HTML/CSS.

🔧 Behind the Scenes (Backend)
Powered by:

fiass.py: Vector creation & document handling

app.py: Flask routing, user sessions, query/response management

.env: Stores API keys securely

index.faiss & index.pkl: Preprocessed data storage


## How to run this?

1.Clone the repository
git clone https://github.com/your-username/RagBased-pdfInteraction-chatbot.git

2.Change into the project directory
cd RagBased-pdfInteraction-chatbot

3.(Optional but recommended) Create a virtual environment
python -m venv .venv

4.Activate the virtual environment

On Windows: .venv\Scripts\activate

On macOS/Linux: source .venv/bin/activate

5.Install the required Python packages
pip install -r requirements.txt

6.Create a .env file in the root directory and add your API key
Example content:
GOOGLE_API_KEY=your_google_genai_api_key_here

7.Run the Flask app
python app.py

8.Open your browser and go to
http://localhost:5000


