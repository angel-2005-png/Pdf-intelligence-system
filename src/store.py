from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from chunks import chunks

embedding_model=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
def store_with_chunks(allchunks):
     vectordb=Chroma.from_documents(documents=allchunks,embedding=embedding_model,persist_directory="./chroma_db")
     return vectordb

print("EVERYTHING DONE ANGEL!!")