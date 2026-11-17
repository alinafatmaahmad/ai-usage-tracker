
import os
import time

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from openai import OpenAI, APIError, RateLimitError, APITimeoutError

load_dotenv()

app = FastAPI(title="AI Usage Tracker")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

@app.get("/ui")
def frontend():
    return FileResponse("static/index.html")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    timeout=30.0
)

MODEL = os.getenv("MODEL_NAME", "gpt-4.1-mini")

INPUT_PRICE = float(
    os.getenv("INPUT_PRICE_PER_MILLION", "1")
)

OUTPUT_PRICE = float(
    os.getenv("OUTPUT_PRICE_PER_MILLION", "4")
)


# Request validation
class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


# Cost calculation
def calculate_cost(input_tokens, output_tokens):

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_PRICE

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_PRICE

    return input_cost + output_cost


# Normal AI response
@app.post("/ask")
def ask_question(data: QuestionRequest):

    start = time.perf_counter()

    try:
        response = client.responses.create(
            model=MODEL,
            input=data.question,
            max_output_tokens=300
        )

        latency = time.perf_counter() - start

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        cost = calculate_cost(
            input_tokens,
            output_tokens
        )

        return {
            "answer": response.output_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "latency_seconds": round(latency, 3),
            "cost_usd": round(cost, 8)
        }

    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="API rate limit exceeded"
        )

    except APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="AI provider request timed out"
        )

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="AI provider error"
        )


# Streaming AI response
@app.post("/stream")
def stream_question(data: QuestionRequest):

    def generate():

        start = time.perf_counter()
        first_token = None

        try:
            stream = client.responses.create(
                model=MODEL,
                input=data.question,
                max_output_tokens=300,
                stream=True
            )

            for event in stream:

                if event.type == "response.output_text.delta":

                    if first_token is None:
                        first_token = time.perf_counter()

                    yield event.delta

                elif event.type == "response.completed":

                    end = time.perf_counter()

                    if first_token:
                        ttft = first_token - start
                    else:
                        ttft = None

                    print("TTFT:", ttft)
                    print("Total latency:", end - start)

        except Exception as error:
            print("Streaming error:", error)
            yield "\n[AI response interrupted]"

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )


@app.get("/")
def home():

    return {
        "message": "AI Usage Tracker is running"
    }
