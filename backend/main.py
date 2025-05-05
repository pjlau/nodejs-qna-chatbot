from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import ollama

app = FastAPI()

# Enable CORS to allow Node.js frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Node.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expanded Q&A data (10 pairs)
qna_data = [
    {"question": "What is Python?", "answer": "Python is a high-level, interpreted programming language known for its readability and versatility."},
    {"question": "What is Node.js?", "answer": "Node.js is a JavaScript runtime built on Chrome's V8 engine, used for building scalable server-side applications."},
    {"question": "What is FastAPI?", "answer": "FastAPI is a modern, high-performance web framework for building APIs with Python."},
    {"question": "What is an LLM?", "answer": "An LLM (Large Language Model) is an AI model trained on vast text data to understand and generate human-like text."},
    {"question": "What is JavaScript?", "answer": "JavaScript is a programming language used primarily for adding interactivity to web pages."},
    {"question": "What is a REST API?", "answer": "A REST API is an architectural style for designing networked applications, relying on stateless, client-server communication."},
    {"question": "What is Express.js?", "answer": "Express.js is a minimal and flexible Node.js web application framework for building APIs and web servers."},
    {"question": "What is CORS?", "answer": "CORS (Cross-Origin Resource Sharing) is a mechanism that allows restricted resources on a web page to be requested from another domain."},
    {"question": "What is a database?", "answer": "A database is an organized collection of data, typically stored and accessed electronically from a computer system."},
    {"question": "What is Git?", "answer": "Git is a distributed version control system for tracking changes in source code during software development."},
]

@app.get("/qna")
async def get_qna():
    return qna_data

@app.post("/submit")
async def submit_question(question: str = Form(...)):
    # Combine Q&As into a context string
    context = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in qna_data])
    
    # Create prompt for LLM
    prompt = f"""You are a helpful assistant. Below is a list of Q&As:\n\n{context}\n\nUser question: {question}\n\nIf the user's question matches or is similar to a question in the Q&As, return the corresponding answer. If not, generate a concise, accurate answer based on your knowledge. Answer in plain text."""
    
    # Query the LLM
    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {"answer": response["message"]["content"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)