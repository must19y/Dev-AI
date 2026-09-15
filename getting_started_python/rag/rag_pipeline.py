from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from ollama import Client

from document_vector_store import DocumentVectorStore
from FastAPI import fastapi

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

##print()


app = FastAPI()


@app.post("/")
def handle_post(chat_request:ChatRequest):
    question = chat_request.question

    conversation_history = Conversation_history({
        role: "system",
        content: system_message.render()
    })


    for msg in chat_request.history:
        conversation_history.add_message({
            role:msg.role,
            content:msg.content
        })


    documents = vector_store.query(question)

    conversation_history.add_message({
        role:"user",
        content:user_message.render(documents=documents,question=question)
    })

    return StreamingResponse(generate_stream(conversation_history))
    






    ##api service for multidocument

    from FastAPI import fastapi
    from document_vector_store import MultiDocumentVectorStore
    from conversation_history import ConversationHistory
    from main import ChatRequest


    client = Client()

    env = Environment(
        FileSystemLoader(

        )
    )

    readme_filenameas=[

    ]

    readme_documents:List[Documents] = []

    for readme_filename in readme_filenames:
        readme_documents.append(
            download_remote_document(filename=readme_filename)
        )

    document= MultiDocumentVectorStore(readme_documents)

    system_message = env.get_template("basic_support_system")
    user_message=env.get_template("basic_support_user")
    

    response = client.chat(
        model="llama-3.2b",
        messages= messages,
        stream= True,
        options={
            temperature: 0
        }
    )

    for chunk in response:
        if chunk.message.content:

            ##snip 

## till here is the way we printwithoutha service jsut that
app = FastAPI()

@app.post("/")
def user_query(chat:ChatRequest)
    conversation_history= Conversation_history({
        role:"system",
        content:system_message.render()
    })

    for message in chat:
        conversation_history.add_message({
            role: message.role,
            content: message.content
        })

    documents = document.query(question,3)

    conversation_history.add_message({
        role: "user",
        content: user_message.render(
            documents=documents,
            question= question
        )
    })
    
    return StreamingResponse(
        generate_stream(conversation_history)
    )

     