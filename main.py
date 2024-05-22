from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat import query_chatbot_with_prompt, load_model

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your Framer domain for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():
    load_model()

@app.post("/query/")
async def query_chatbot(request: QueryRequest):
    response = query_chatbot_with_prompt(request.question)
    if not response:
        raise HTTPException(status_code=500, detail="No response from the chatbot")
    return {"response": response}
