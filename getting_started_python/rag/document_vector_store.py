from pathlib import Path
from typing import List

import chromadb
from chromadb import Collection
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,
)

from pydantic import BaseModel

class DocumentVectorStore:

    def __init__(self, document_text: str):

        ollama_embedding_function = OllamaEmbeddingFunction(
            url="http://ollama:11434",
            model_name="mxbai-embed-large",
        )

        client = chromadb.Client()

        self.collection: Collection = client.create_collection(
            name="python_code_examples",
            embedding_function=ollama_embedding_function,
        )

        splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=1500,
        )

        chunks = splitter.split_text(document_text)

        print(f"Number of chunks: {len(chunks)}")

        self.collection.add(
            documents=chunks,
            ids=[
                f"code_chunk_{chunk_idx + 1}"
                for chunk_idx, chunk in enumerate(chunks)
            ],
        )

    def query(self, question: str, n_results: int = 3) -> List[str]:

        results = self.collection.query(
            query_texts=[question],
            n_results=n_results,
        )

        return results["documents"][0]
        ##or we can use results.get("documents")[0] means firstquery


document_path = Path("sample_code.py")

document_text = document_path.read_text()

python_vector_store = DocumentVectorStore(document_text)


question = "How does the code handle HTTP requests?"

documents = python_vector_store.query(
    question,
    n_results=2,
)

for idx, document in enumerate(documents, start=1):

    print(f"\n--- Result {idx} ---\n")
    print(document)


class Document:
    source_url: str,
    content: str 


class MultiDocumentVectorStore:
    def __init__(self,document:List[Document]):
        ollama_embedding_function = OllamaEmbeddingFunction(
            url="http://ollama:11434",
            model_name="mxbai-embed-large",
        )

        client = Client()

        self.collection = client.create_collection(
            name="examples_readme",
            embedding_function=ollama_embedding_function
        )

        chunks = splitter.split_text(documents)
        
        for doc_idx, document in enumerate(documents):
            splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MarkDown,
            chunk_size = 1500,
            chunk_overlap=0
        )
            chunks= splitter.split_text(document.content)

            for chunk_idx,chunk in enumerate(chunks):
               collection.add(
                documents=chunk,
                ids= [f"{doc_idx + 1} {chunk_idx + 1}"]
                metadata={
                    "source_url": document.source_url,
                }
            )

    def query(self,question,n_results):
        results= self.collection.query(
            question=[question],
            n_results= n_results
        )

        ##return results or results.get something

        document_chunk_results =results.get('documents')[0]
        document_chunk_metadatas=results.get('metadatas')[0]

        documents:List[Document] = []
        for idx,document_chunk in document_chunk_results:
            return documents.append(Document(
                source_url=document_chunk_metadatas[idx].get(
                    'source_url'
                ),##hereusedidxthengetcozidxindictwillnotgiveanything
                content=document_chunk
            ))
##veryimportant to note is that because [] is used for storing chunks
##so we don't do documednt_chunk[0] but if you see we must use [idx]
##for metadata or coz we used dict to add it
        return documents


readme_filenames = [
'README.md',
'part1/getting_started_python/README.md',
]

readme_documents= [] 

for readme_filename in readme_filenames:
    readme_documents.append(
        download_remote_document(filename=readme_filename)
    )

readme_vector_store= MultiDocumentVectorStore(readme_documents)

##question="" and then

#results = readme_vector_store(question=question)

#print(results)

## and here one more thing to note is that readme_documents is a list
##soif we providethatlistwithashapelikeList[Document] which the
##class expects so we can also use return or like shape making{
## } like this
