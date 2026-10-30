# LangChain AI Chatbot

A conversational AI chatbot built with **Python, LangChain, Groq, Streamlit, and Pydantic**. It uses LangChain's `RunnableBranch` and `RunnableParallel` to route questions and generate structured responses.

## Features

- **Intelligent Question Routing:** Routes programming, mathematics, and general questions to appropriate prompts.
- **Structured Responses:** Uses Pydantic schemas to organize answers into predictable fields.
- **Parallel Processing:** Generates an answer and a summary through `RunnableParallel`.
- **Follow-up Suggestions:** Provides relevant follow-up questions.
- **Interactive UI:** Chat interface built with Streamlit.
- **Groq LLM Integration:** Uses Groq-hosted language models for inference.

## Tech Stack

- Python
- LangChain
- LangChain-Groq
- Groq API
- Streamlit
- Pydantic
- python-dotenv

## Project Structure

```text
A_chatbot_model/
├── assets/
├── app.py
├── chatbot.py
├── prompts.py
├── schemas.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/phitron-rahim/A_chatbot_model.git
cd A_chatbot_model
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Add your own Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
GROQ_TEMPERATURE=0.2
```

Get an API key from [Groq Console](https://console.groq.com/keys).

**Security:** Never commit your `.env` file or publish your API key.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## How It Works

1. The user submits a question through the Streamlit interface.
2. The chatbot identifies whether the question relates to programming, mathematics, or general topics.
3. `RunnableBranch` routes the question to the appropriate prompt.
4. LangChain invokes the Groq-hosted language model and structures the response using Pydantic schemas.
5. `RunnableParallel` generates the answer and summary in parallel.
6. The application displays the response and relevant follow-up questions.

## Example Questions

- `What is Python?`
- `What is 25 × 16?`
- `Write a Python program to check whether a number is prime.`

## Future Improvements

- Conversation memory and persistent chat history
- Improved error handling and API status messages
- Deployment with a public demo URL
- Automated testing and evaluation

## Author

**MD Rahim Hassan Sarniabath**

- GitHub: [@phitron-rahim](https://github.com/phitron-rahim)
- Portfolio: [AI/ML Portfolio](https://rahim-ai-ml-portfolio.vercel.app/)
- Hugging Face: [rahimHassan09](https://huggingface.co/rahimHassan09)
- Kaggle: [rahimhassan](https://www.kaggle.com/rahimhassan)

---

If you find this project useful, consider giving the repository a star.
