from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("pdf-intelligence")


def store_with_chunks(allchunks):
    vectors = []

    for i, chunk in enumerate(allchunks):
        # embed using llama-text-embed-v2
        embedding = pc.inference.embed(
            model="llama-text-embed-v2",
            inputs=[chunk.page_content],
            parameters={"input_type": "passage"}
        )[0].values

        vectors.append({
            "id": str(i),
            "values": embedding,
            "metadata": {
                "text": chunk.page_content,
                **chunk.metadata
            }
        })

    # upsert in batches of 100
    for i in range(0, len(vectors), 100):
        index.upsert(vectors=vectors[i:i + 100])
        print(f"Uploaded batch {i // 100 + 1}")

    print("All chunks stored in Pinecone ✅")
    return index