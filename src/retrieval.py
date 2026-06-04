from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = PineconeVectorStore(
    index_name="pdf-intelligence",
    embedding=embedding_model
)

def retrieval(query, k=3, score_threshold=0.9):

    scored_results = vector_store.similarity_search_with_score(query, k=k*2)
    print(f"No of chunks after similarity search: {len(scored_results)}")

    good_chunks = []
    for result, score in scored_results:
        print(f"result:{result.page_content[:60]} || score={score:.4f}")
        if score > score_threshold:    # ← Pinecone uses HIGHER = better (opposite of ChromaDB!)
            good_chunks.append(result.page_content)

    print(f"After score filter: {len(good_chunks)} results kept")

    if not good_chunks:
        print("No confident results found. Try a different question.")
        return []

    mmr_results = vector_store.max_marginal_relevance_search(query, k=k, fetch_k=k*2)
    final_result = [r for r in mmr_results if r.page_content in good_chunks]

    return final_result




