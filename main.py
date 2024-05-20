from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chat import query_chatbot_with_prompt, load_model

app = FastAPI()

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
