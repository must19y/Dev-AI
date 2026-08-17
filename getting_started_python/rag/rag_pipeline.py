from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from ollama import Client

from document_vector_store import DocumentVectorStore

document = Path("sample_code").read_text()

vector_store = DocumentVectorStore(document)

env = Environment(
    loader = FileSystemLoader(seach_paths="")
)

system_message= env.get_template("basic_support_system_message.txt")
user_message= env.get_template("basic_support_user_message.txt")

client = Client(
    host= "http://ollama:11434"
)

messages=[
    {
        role: "system",
        content:system_message.render()
    },
    {
        role:"user",
        content:user_message.render(documents=documents,question:question)
    }
]


response = client.chat(
    model="llama-3.2b",
    messages=messages,
    stream = True 
    options={
        temperature: 0
    }
)

for chunk in response:
    if response.message.content:
        print(response.message.content,end="",flush=True)

print()
