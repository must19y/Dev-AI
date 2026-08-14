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