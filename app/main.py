from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from init_ollama import wait_for_ollama
from contextlib import asynccontextmanager
import requests
import logging
from config import OLLAMA_HOST, MODEL_NAME
from document_processor import DocumentProcessor


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create documents directory if it doesn't exist
DOCUMENTS_DIR = Path("/app/documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)

# Initialize document processor
document_processor = DocumentProcessor(DOCUMENTS_DIR)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI"""
    # Startup
    if not wait_for_ollama():
        raise Exception("Failed to initialize Ollama service")
    yield
    # Shutdown
    pass

app = FastAPI(title="Local Support Bot", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Local Support Bot API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = DOCUMENTS_DIR / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the new document
        document_processor.process_documents()
        
        return {"message": f"File {file.filename} uploaded and processed successfully"}
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/query")
async def query(question: str):
    try:
        # Get relevant context from documents
        context = document_processor.get_relevant_context(question)
        
        # Prepare the prompt with context
        if context:
            context_text = "\n\n".join([doc["content"] for doc in context])
            prompt = f"""Based on the following context, please answer the question. If the context doesn't contain relevant information, say so.

Context:
{context_text}

Question: {question}

Answer:"""
        else:
            prompt = question

        # Send request to Ollama
        ollama_url = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        logger.info(f"Sending request to Ollama API: {ollama_url}")
        logger.info(f"Payload: {payload}")
        
        response = requests.post(ollama_url, json=payload)
        logger.info(f"Ollama API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            return {"response": result.get("response", "No response generated")}
        else:
            logger.error(f"Failed to get response from AI. Status code: {response.status_code}, Response: {response.text}")
            raise HTTPException(status_code=500, detail="Failed to get response from AI")
            
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 