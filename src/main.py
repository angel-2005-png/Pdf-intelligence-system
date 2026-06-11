from fastapi import FastAPI,UploadFile,File
from loadingdocuments import load_document
from chunks import chunks
from store import store_with_chunks
from pydantic import BaseModel
from answer import ask

class Question_answer(BaseModel):
    question: str
app=FastAPI()

@app.get("/health")
def health():
    return {"status":"running"}


@app.post('/upload')
async def upload(file:UploadFile=File(...)):
    file_path = f"uploaded_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text_chunks=chunks(file_path)
    store_with_chunks(text_chunks)
    return{"messege":"done","No.of Chunks":len(text_chunks)}


@app.post('/ask')
def ask_question(request:Question_answer):
    answer,chunks=ask(request.question)
    if not answer:
        return {"answer":"I could not find this in the manual.","Sources":[]}

    sources = list(set([c.metadata["page Number"] for c in chunks]))


    return {"answer": answer, "sources": sources}








