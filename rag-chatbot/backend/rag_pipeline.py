import os
import time
from pathlib import Path
from typing import List, Optional

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

from backend.pdf_loader import load_and_split_pdfs
from backend.config import GROQ_API_KEY

# Directories for vector store storage
BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_DIR = BASE_DIR / "vectorstore"
INDEX_PATH = VECTOR_STORE_DIR / "faiss_index_hf" # Changed name to avoid conflict with OpenAI index

# 1. Initialize HuggingFace Embeddings (Local)
print("LOG: Using HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)")

def initialize_embeddings():
    """
    Initializes HuggingFace embeddings with a retry mechanism for model download.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    retries = 2
    for attempt in range(retries):
        try:
            return HuggingFaceEmbeddings(model_name=model_name)
        except Exception as e:
            print(f"Error initializing HuggingFace embeddings (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Failed to initialize embeddings after multiple attempts.")
                raise e

embeddings_model = initialize_embeddings()

# 2. Initialize Groq LLM
print("LOG: Using Groq LLM (llama-3.3-70b-versatile)")
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

def create_vector_store() -> Optional[FAISS]:
    """
    Creates a new FAISS vector store from the PDF documents and saves it to disk.
    """
    print("LOG: Starting vector store creation process with HF embeddings...")
    
    docs = load_and_split_pdfs()
    
    if not docs:
        print("Warning: No documents found to create the vector store. Exiting...")
        return None

    print("LOG: Creating embeddings and FAISS index... (local processing)")
    try:
        # Pass the HF embeddings model to FAISS
        vector_store = FAISS.from_documents(docs, embeddings_model)
        print("Success: FAISS index created successfully.")
    except Exception as e:
        print(f"Error during FAISS index creation: {e}")
        return None

    try:
        if not VECTOR_STORE_DIR.exists():
            VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
            
        vector_store.save_local(str(INDEX_PATH))
        print(f"Success: Vector store saved locally at: {INDEX_PATH}")
        return vector_store
    except Exception as e:
        print(f"Error saving vector store: {e}")
        return None

def load_vector_store() -> Optional[FAISS]:
    """
    Loads an existing FAISS vector store from disk or creates it if not found.
    """
    print("LOG: Attempting to load existing HF vector store...")
    
    faiss_file = INDEX_PATH / "index.faiss"
    
    if INDEX_PATH.exists() and faiss_file.exists():
        try:
            vector_store = FAISS.load_local(
                str(INDEX_PATH), 
                embeddings_model,
                allow_dangerous_deserialization=True
            )
            print("Success: Vector store loaded successfully from disk.")
            return vector_store
        except Exception as e:
            print(f"Error loading vector store: {e}. Recreating...")
            return create_vector_store()
    else:
        print("Warning: Vector store index (HF) not found on disk. Creating new one...")
        return create_vector_store()

def get_answer(query: str) -> str:
    """
    Retrieves context from FAISS and generates an answer using Groq LLM.
    """
    print(f"\nLOG: Processing query with local RAG: '{query}'")
    
    # 1. Load vector store
    vector_db = load_vector_store()
    if not vector_db:
        return "Internal Error: Unable to access the knowledge base."

    # 2. Retrieve top 3 relevant chunks
    try:
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(query)
        print(f"LOG: Retrieved {len(relevant_docs)} chunks for context.")
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return "An error occurred while retrieving information."

    if not relevant_docs:
        print("Warning: No relevant content found in vector store.")
        return "I don't know (no relevant information found)."

    # 3. Combine content into context
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # 4. Prompt design
    prompt_template = """You are a helpful assistant.
Answer the question ONLY from the provided context.
If answer is not in context, say 'I dont know'.

Context:
{context}

Question:
{question}"""

    prompt = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )

    # 5. Generate Answer via Groq
    formatted_prompt = prompt.format(context=context, question=query)
    
    try:
        response = llm.invoke(formatted_prompt)
        return response.content.strip()
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return f"An error occurred while generating the answer via Groq: {e}"

# Test block
if __name__ == "__main__":
    print("-" * 30)
    print("Testing RAG Pipeline: Local HF Embeddings + Groq LLM")
    
    # 1. Rebuild vector store from scratch
    print("Rebuilding vector store for local embeddings...")
    vector_db = create_vector_store()
    
    # 2. Test sample query
    sample_query = "What is SVU admission process?"
    answer = get_answer(sample_query)
    
    print("\n--- Final Answer (Local RAG) ---")
    print(answer)
    print("-" * 30)
