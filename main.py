from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
from openai import OpenAI

client = OpenAI(api_key="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDczNzFAZHMuc3R1ZHkuaWl0bS5hYy5pbiIsImlhdCI6MTc4Mzc3ODk3NSwiaXNzIjoiaHR0cHM6Ly9haXBpcGUub3JnIiwiYXVkIjoiYWlwaXBlLWFwaSIsImV4cCI6MTc4NDM4Mzc3NX0.VtaofHmHiVjZM5nW698OY-qanIgeiIivnKTz72el8Sg")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    image_base64: str
    question: str

@app.post("/answer-image")
def answer(req: Request):

    image_url = f"data:image/png;base64,{req.image_base64}"

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content":
                """Answer questions about images.

Rules:
- Return ONLY the answer.
- Never explain.
- If numeric, return only the number.
- No currency symbols.
- No units.
- Always return plain text."""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type":"text",
                        "text":req.question
                    },
                    {
                        "type":"image_url",
                        "image_url":{
                            "url":image_url
                        }
                    }
                ]
            }
        ]
    )

    ans = response.choices[0].message.content.strip()

    return {"answer": ans}