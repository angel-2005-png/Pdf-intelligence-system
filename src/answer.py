from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from retrieval import retrieval
from dotenv import load_dotenv
import os

load_dotenv()

os.environ.get("GROQ=API-KEY")
llm=ChatGroq(model="llama-3.1-8b-instant",temperature=0)

prompt=PromptTemplate(
    input_variables=["context","question"],
    template="""
You are a helpful assistant answering questions about a technical manual.
Use ONLY the context below to answer. If the answer is not in the context,
say "I could not find this in the manual."

context={context}
question={question}
answer=
"""
)

def ask(question):
    chunks=retrieval(question)

    if not chunks:
        print("No answers found for question")
        return None,[]

    context="\n\n".join(chunk.page_content for chunk in chunks)
    prompt_template=prompt.format(context=context,question=question)
    response=llm.invoke(prompt_template)
    answer=response.content

    return answer,chunks
