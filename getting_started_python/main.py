from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import Client
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

client = Client(
    host="http://ollama:11434"
)

class ChatRequest(BaseModel):
 question: str

def generate_stream(question: str):
 result = client.generate(stream=True, model="llama3.2", prompt=question)
 for chunk in result:
  if chunk.response:
   yield chunk.response

@app.post("/")
def chat(chatRequest: ChatRequest):
  return StreamingResponse(
  generate_stream(chatRequest.question), media_type="text/plain")







from typing import List, Literal

from pydantic import BaseModel


class ChatRequestMessage(BaseModel):

    role: Literal["user", "assistant"]

    content: str


class ChatRequest(BaseModel):

    history: List[ChatRequestMessage] = []

    question: str





from typing import List, Dict


Message = Dict[str, str]
Messages = List[Message]


class ConversationHistory:

    def __init__(self, system_message: Message):

        self.system_message = system_message

        self.message_history: Messages = []

    def add_messages(
        self,
        messages: Messages,
    ):

        self.message_history.extend(messages)

    def add_message(
        self,
        message: Message,
    ):

        self.message_history.append(message)

    def get_messages(self) -> Messages:

        messages = [self.system_message]

        messages.extend(self.message_history)

        return messages