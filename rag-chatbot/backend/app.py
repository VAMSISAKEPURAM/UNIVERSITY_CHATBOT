import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_pipeline import get_answer

# Initialize FastAPI app
app = FastAPI(title="University RAG Chatbot", version="1.0.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define request body model
class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    """Root endpoint to check if the server is running."""
    return {"message": "RAG Chatbot Running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint to process user queries and return structured answers.
    """
    query = request.query.strip()

    # 1. Validate query is not empty
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # 2. Logging incoming query
    print(f"\n[INCOMING] User Query: {query}")
    start_time = time.time()

    # 3. Call RAG pipeline
    try:
        answer = get_answer(query)
        
        # 4. Handle internal failure messages from get_answer
        if "Internal Error" in answer or "An error occurred" in answer:
            print(f"[ERROR] Pipeline Failure: {answer}")
            # Still returning the detailed message as requested, though you could throw a 500 here
            # But the user said: "If pipeline fails → return 500 error with message"
            # Since get_answer returns error strings, we check if they contain failure indicators.
            raise HTTPException(status_code=500, detail=answer)

        # 5. Calculate and log execution time
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"[RESPONSE] Time: {elapsed_time:.2f} seconds")

        return {"answer": answer}

    except HTTPException as http_ex:
        # Re-raise HTTP exceptions
        raise http_ex
    except Exception as e:
        # Catch unexpected pipeline crashes
        print(f"[FATAL] System Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")

# To run the server manually:
# uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
