# 🎓 University ChatBot (RAG-Powered)

An AI-driven chatbot designed to assist students, faculty, and visitors with **university-related queries** such as admissions, courses, campus services, and general information.  
Built using **Retrieval-Augmented Generation (RAG)**, this project combines natural language understanding with document retrieval to deliver accurate, context-aware answers.

---

## 🚀 Features
- **Conversational AI**: Provides human-like responses to student queries.
- **RAG Pipeline**: Integrates vector search with LLMs for precise information retrieval.
- **Multi-Module Architecture**:
  - **Backend**: FastAPI-based services for query handling and pipeline orchestration.
  - **Frontend**: Simple web interface with HTML, CSS, and JavaScript.
  - **Vector Store**: FAISS index for efficient semantic search.
- **Document Support**: Handles university PDFs (courses, services, overview).
- **Extensible Design**: Easy to add new documents or expand functionality.

---

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Vector Store**: FAISS
- **Libraries**: 
  - LangChain / Hugging Face Transformers
  - PyPDF Loader
  - Custom RAG pipeline modules
- **Deployment**: GitHub + Local environment setup

---

## 📂 Folder Structure

```text
📦 rag-chatbot/
 ┣ 📂 backend/                 # FastAPI backend services
 ┃ ┣ 📜 app.py                 # Main application entry
 ┃ ┣ 📜 config.py              # Configuration settings
 ┃ ┣ 📜 pdf_loader.py          # PDF ingestion logic
 ┃ ┣ 📜 rag_pipeline.py        # RAG pipeline orchestration
 ┃ ┗ 📜 __init__.py
 ┣ 📂 data/pdfs/               # University documents (Admissions, Services, Overview)
 ┣ 📂 frontend/                # Web interface
 ┃ ┣ 📜 index.html             # Landing page
 ┃ ┣ 📜 login.html             # Authentication page
 ┃ ┣ 📜 script.js              # Client-side logic
 ┃ ┗ 📜 style.css              # Styling and layout
 ┣ 📂 vectorstore/faiss_index_hf/  # FAISS index files for semantic search
 ┣ 📜 requirements.txt         # Python dependencies
 ┗
```
---

## ⚙️ Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/VAMSISAKEPURAM/UNIVERSITY_CHATBOT.git
   cd UNIVERSITY_CHATBOT/rag-chatbot
Create a virtual environment:

bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
Install dependencies:

bash
pip install -r requirements.txt
Run the backend:

bash
uvicorn backend.app:app --reload
Open the frontend:
Launch index.html in your browser to interact with the chatbot.

📖 Example Use Cases
Admissions Queries: “What courses are available for undergraduates?”

Campus Services: “Tell me about hostel facilities.”

General Info: “Give me an overview of the university.”

🔒 Security Note
API keys and secrets must be stored in a local .env file (not committed to GitHub).

Ensure .env is listed in .gitignore to prevent accidental exposure.

🌟 Future Enhancements
Add authentication for student/faculty login.

Deploy on cloud (Azure/AWS/GCP).

Expand knowledge base with more university documents.

Integrate multilingual support.

👨‍💻 Author
Developed by Vamsi Sakepuram  
📍 Tirupati, India
🎯 Focused on AI-powered apps, consulting, and tech innovation.
