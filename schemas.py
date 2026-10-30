from typing import Literal

from pydantic import BaseModel


class AnswerPayload(BaseModel):
    answer: str
    category: Literal["programming", "mathematics", "general"]
    confidence: float
    keywords: list[str]


class SummaryPayload(BaseModel):
    summary: str
    follow_up_questions: list[str]


class ChatbotResponse(BaseModel):
    answer: str
    summary: str
    confidence: float
    category: Literal["programming", "mathematics", "general"]
    keywords: list[str]
    follow_up_questions: list[str]