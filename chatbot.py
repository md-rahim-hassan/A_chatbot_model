
from __future__ import annotations

import os
import re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import (
    GENERAL_PROMPT,
    MATH_PROMPT,
    PROGRAMMING_PROMPT,
)

from schemas import ChatbotResponse


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)


def get_gemini_client():

    api_key = os.getenv("GOOGLE_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is missing.")

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    ).strip()

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=120000)
    )

    return client, model_name


PROGRAMMING_PATTERN = re.compile(
    r"\b(python|java|javascript|typescript|code|debug|"
    r"function|class|algorithm|api|database|sql|html|css|"
    r"react|django|flask|streamlit)\b",
    re.IGNORECASE,
)

MATH_PATTERN = re.compile(
    r"\b(math|algebra|calculus|geometry|equation|integral|"
    r"derivative|matrix|probability|statistics|solve|factor|"
    r"simplify)\b|[0-9]+\s*[-+*/^]\s*[0-9]+",
    re.IGNORECASE,
)


def select_prompt(question):

    if PROGRAMMING_PATTERN.search(question):
        return PROGRAMMING_PROMPT, "programming"

    if MATH_PATTERN.search(question):
        return MATH_PROMPT, "mathematics"

    return GENERAL_PROMPT, "general"


def ask_chatbot(
    question: str,
    context: str = "No specific document context provided."
) -> ChatbotResponse:

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    question = question.strip()

    prompt_template, category = select_prompt(question)

    base_prompt = prompt_template.format(question=question)

    final_prompt = f"""
{base_prompt}

Document Context:
{context}

Return only valid JSON with these fields:
{{
    "answer": "Your answer",
    "summary": "Short summary",
    "confidence": 0.95,
    "category": "{category}",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "follow_up_questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
}}
"""

    client, model_name = get_gemini_client()

    print("Gemini request started...")
    print("Using model:", model_name)

    response = client.models.generate_content(
    model=model_name,
    contents=final_prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": ChatbotResponse,
        "max_output_tokens": 512,
        "temperature": 0.2,
    }
    )

    print("Gemini response received!")

    if not response.text:
        raise RuntimeError("Empty response from Gemini.")

    if response.parsed is not None:
        return ChatbotResponse.model_validate(response.parsed)

    import json

    return ChatbotResponse.model_validate(
        json.loads(response.text)
    )
