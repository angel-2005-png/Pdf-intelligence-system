from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("pdf-intelligence")


def retrieval(query, k=3, score_threshold=0.5):
    # embed query using same model as stored vectors
    query_embedding = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[query],
        parameters={"input_type": "query"}
    )[0].values

    # search pinecone
    results = index.query(
        vector=query_embedding,
        top_k=k,
        include_metadata=True
    )

    # filter by score
    good_results = [r for r in results.matches if r.score > score_threshold]

    if not good_results:
        print("No confident results found.")
        return []

    return good_results




