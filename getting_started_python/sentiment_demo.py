from typing import Literal

from pydantic import BaseModel, Field
from ollama import Client


class SocialMessage(BaseModel):
    sentiment: Literal[
        "positive",
        "neutral",
        "negative"
    ] = Field(
        description="Provide the sentiment of the statement"
    )

    department: Literal[
        "customer_support",
        "online_ordering",
        "product_quality",
        "shipping_and_delivery",
        "other_off_topic"
    ] = Field(
        description="Department the statement should be routed to"
    )

    reply: str = Field(
        description="Recommend a reply to the statement"
    )


client = Client(host="http://ollama:11434")


def analyze_sentiment(message: str)->SocialMessage:
    return client.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": """
You are an online customer feedback expert. Analyze the provided statement
carefully and respond with the sentiment, department, and reply.
"""}
            {
                "role": "user",
                "content": message,
            }
        ],
        format=SocialMessage.model_json_schema(),
        options={
        "temperature": 0
       }
    )

print(SocialMessage.model_json_schema)

response = analyze_sentiment(
    "Don't trust @AcmeCorp. It's been weeks and I never received my order."
)

social_message = SocialMessage.model_validate_json(
    response.message.content
)

print("\nPython Object:")
print(social_message)

print("\nPetty Json")
print(social_message.model_dump_json(indent=2))