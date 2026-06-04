from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

load_dotenv()

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def store_with_chunks(allchunks):
    # initialize pinecone
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    index_name = "pdf-intelligence"

    # create index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,  # all-MiniLM-L6-v2 outputs 384 dimensions
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    # store chunks in pinecone
    vectordb = PineconeVectorStore.from_documents(
        documents=allchunks,
        embedding=embedding_model,
        index_name=index_name
    )

    return vectordb

print("EVERYTHING DONE ANGEL!!")