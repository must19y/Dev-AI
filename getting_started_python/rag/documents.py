import requests

from document_vector_store import Document


SOURCE_BASE_URL = "https://github.com"
RAW_CONTENT_BASE_URL = "https://raw.githubusercontent.com"


def download_remote_document(
    owner="jorshali",
    repo="developers-guide-to-ai",
    branch="main",
    filename="README.md",
) -> Document:

    source_url = (
        f"{SOURCE_BASE_URL}/"
        f"{owner}/{repo}/blob/{branch}/{filename}"
    )

    raw_url = (
        f"{RAW_CONTENT_BASE_URL}/"
        f"{owner}/{repo}/{branch}/{filename}"
    )

    response = requests.get(raw_url)

    response.raise_for_status()

    return Document(
        source_url=source_url,
        content=response.text,
    )##i think here whenever we extract the docs we need to structure them
    