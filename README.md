# AI Usage Tracker

An AI-powered chatbot application built using Python, FastAPI, Groq API, HTML, CSS, and JavaScript.

The application allows users to ask AI questions, receive normal or streamed responses, and monitor API usage analytics.

## Features

- AI-powered question and answer system
- Normal AI response
- Streaming AI response
- Input token tracking
- Output token tracking
- Total token calculation
- Response latency measurement
- Estimated API cost calculation
- Simple and responsive frontend

## Technologies Used

**Backend**
- Python
- FastAPI
- OpenAI Python SDK (Groq-compatible API)

**AI Provider**
- Groq API
- GPT-OSS 120B model

**Frontend**
- HTML
- CSS
- JavaScript

**Other Tools**
- Uvicorn
- Python dotenv
- Pydantic
- Git and GitHub

## Project Structure

```text
ai_usage_tracker/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-usage-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=openai/gpt-oss-120b
INPUT_PRICE_PER_MILLION=0.15
OUTPUT_PRICE_PER_MILLION=0.60
```

Never upload your actual API key to GitHub.

### 6. Run the application

```bash
python -m uvicorn main:app --reload
```

### 7. Open the application

Frontend:

http://127.0.0.1:8000/ui

API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check application status |
| POST | `/ask` | Get a normal AI response |
| POST | `/stream` | Get a streamed AI response |
| GET | `/ui` | Open the frontend |

## Usage Analytics

The application calculates:

- Input tokens
- Output tokens
- Total tokens
- Response latency
- Estimated API cost

## Security

- API keys are stored in environment variables.
- The `.env` file is excluded from Git.
- Never commit secret credentials.

## Author

Alina Fatima

## Project Status

Completed basic AI integration, response streaming, and API usage analytics.
