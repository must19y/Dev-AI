import instructor
from pydantic import BaseModel,Field
from typing import Literal

class SocialMessage(BaseModel):
    sentiment: Literal[
        "positive",
        "neutral",
        "negative",
    ] = Field(
        description="Provide the sentiment of the statement"
    )

    department: Literal[
        "customer_support",
        "online_ordering",
        "product_quality",
        "shipping_and_delivery",
        "other_off_topic",
    ] = Field(
        description="Department the statement should be routed to"
    )

    reply: str = Field(
        description="Recommend a reply to the statement"
    )


client = instructor.from_provider(
    "ollama/llama-3.2",
    base_url="http://ollama:11434/v1",
    mode=instructor.Mode.JSON,
)


def analyze_sentiment(statement: str) -> SocialMessage:
    return client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": """
                 You are an online customer feedback expert.
                 Analyze the provided statement carefully and
                 respond with the sentiment, department and reply.
                """,
            },
            {
                "role": "user",
                "content": "Statement: {{statement}}\n\nJSON:",
            },
        ],
        response_model=SocialMessage,
        context={
            "statement": statement,
        },
        temperature=0,
    )


social_message = analyze_sentiment(
    """
Don't trust @AcmeCorp.
It's been weeks.
I never received my order.
"""
)

print(social_message.model_dump_json(indent=2))