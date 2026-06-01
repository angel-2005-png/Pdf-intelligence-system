from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunks(file_path):
    reader=PdfReader(file_path)

    splitter=RecursiveCharacterTextSplitter(chunk_size=512,chunk_overlap=100,separators=["\n\n","\n","."," ",""])

    allchunks=[]

    for page_num,page in enumerate(reader.pages):
        text=page.extract_text()

        if not text.strip():
            continue

        chunks=splitter.create_documents(texts=[text],metadatas=[{"page Number":page_num+1,"Source":file_path,"Total Pages":len(reader.pages)}])

        allchunks.extend(chunks)

    return allchunks













