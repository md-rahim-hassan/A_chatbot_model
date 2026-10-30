
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from chatbot import ask_chatbot
from schemas import ChatbotResponse
from rag import process_document


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="LangChain RAG Chatbot",
    page_icon="🤖",
    layout="centered",
)


# --------------------------------------------------
# Environment
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)


# --------------------------------------------------
# Display Response
# --------------------------------------------------

def display_response(response: ChatbotResponse):

    st.markdown(response.answer)

    with st.expander("View structured output"):
        st.json(response.model_dump())

    with st.expander("Summary"):
        st.write(response.summary)

        st.write("Confidence:", response.confidence)
        st.write("Category:", response.category)

        if response.keywords:
            st.write("Keywords:", ", ".join(response.keywords))

        if response.follow_up_questions:
            st.write("Related questions:")

            for question in response.follow_up_questions:
                st.markdown(f"- {question}")


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("AI Chatbot & RAG")

    st.caption("Gemini + LangChain + ChromaDB")

    st.divider()

    st.subheader("Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload a PDF or Text file",
        type=["pdf", "txt"]
    )

    if uploaded_file is not None:

        if st.session_state.uploaded_filename != uploaded_file.name:

            os.makedirs(BASE_DIR / "temp", exist_ok=True)

            file_path = BASE_DIR / "temp" / uploaded_file.name

            with open(file_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

            try:
                with st.spinner("Processing document..."):

                    st.session_state.retriever = process_document(
                        str(file_path)
                    )

                    st.session_state.uploaded_filename = uploaded_file.name

                st.success("Document processed successfully!")

            except Exception as exc:
                st.error(f"Document processing failed: {exc}")

    else:
        st.info("Upload a PDF or TXT file to chat with your documents.")

        if st.session_state.uploaded_filename is not None:
            st.session_state.retriever = None
            st.session_state.uploaded_filename = None

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# Main Interface
# --------------------------------------------------

st.title("LangChain RAG Chatbot")

st.caption(
    "Ask programming, mathematics, general questions "
    "or upload a document to chat with it."
)


# --------------------------------------------------
# Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":
            st.markdown(message["content"])

        else:
            response = ChatbotResponse.model_validate(
                message["content"]
            )

            display_response(response)


# --------------------------------------------------
# User Input
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about your document or general topics..."
)


# --------------------------------------------------
# Generate Response
# --------------------------------------------------

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        try:

            with st.spinner("Thinking..."):

                # Retrieve document context

                context_text = ""

                if st.session_state.retriever is not None:

                    docs = st.session_state.retriever.invoke(question)

                    context_text = "\n\n".join(
                        doc.page_content for doc in docs
                    )

                # Generate Gemini response

                response = ask_chatbot(
                    question=question,
                    context=context_text or
                    "No specific document context provided."
                )

            display_response(response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response.model_dump(),
            })

        except Exception as exc:

            st.error(
                f"Failed to generate a response: "
                f"{type(exc).__name__}: {exc}"
            )

            st.caption("Check the VS Code terminal for details.")
