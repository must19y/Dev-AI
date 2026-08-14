from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


def generate_response(question: str):
    response = f"You asked: {question}"

    for word in response.split():
        yield word + " "


@app.get("/")
def home():
    return {"message": "FastAPI server is running"}


@app.post("/chat")
def chat(question: str):

    return StreamingResponse(
        generate_response(question),
        media_type="text/plain",
    )


def calculate_total(price: float, quantity: int) -> float:
    return price * quantity


def calculate_discount(price: float, discount: float) -> float:
    return price * (1 - discount)