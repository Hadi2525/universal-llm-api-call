from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from src.utils import get_api_client, get_api_async_client
from dotenv import load_dotenv
import os
from typing import AsyncGenerator
import json

_ = load_dotenv()

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")


app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a simple route
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/generate/response")
def generate_text(prompt: str, vendor: str = "openai", model: str = "gpt-4"):
    """
    Generate text using the specified model.
    """
    try:
        client = get_api_client(vendor=vendor)
        response = client.chat.completions.create(
            model=model,
            n=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}


@app.post("/stream/response")
async def stream_text(prompt: str, vendor: str = "openai", model: str = "gpt-4"):
    """
    Stream text using the specified model.
    """
    try:
        client = await get_api_async_client(vendor=vendor)
        response = await client.chat.completions.create(
            model= model,
            n=1,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True)
        async def stream() -> AsyncGenerator[str, None]:
            async for chunk in response:
                if hasattr(chunk, "choices") and chunk.choices:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        yield f"{json.dumps({'response': delta.content})}\n"
        return StreamingResponse(stream(), media_type="application/json")
    except Exception as e:
        return {"error": str(e)}