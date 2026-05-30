from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding_model=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store=Chroma(persist_directory="./chroma_db",embedding_function=embedding_model)

def retrieval(query,k=3,score_threshold=0.9):

    score_results=vector_store.similarity_search_with_score(query,k=k*2,)
    print("No of chunks after similarity search:",len(score_results))

    good_chunks=[]
    for result,score in score_results:
        print(f"result:{result.page_content[:60]} || score={score:.4f}")
        if score<score_threshold:
            good_chunks.append(result.page_content)

            print(f"After score filter: {len(good_chunks)} results kept")

    if not good_chunks:
            print("No confident results found. Try a different question.")
            return []

    final_chunks=vector_store.max_marginal_relevance_search(query,k=k,fetch_k=k*2)
    final_result=[]

    for r in final_chunks:
        if(r.page_content in good_chunks):
            final_result.append(r)

    return final_result








