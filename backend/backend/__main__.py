from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import lorem
from backend.severity_classifier import get_sentence_classification

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "abstractive": lorem.paragraph(),
        "extractive": "This is an extractive simplification",
    }


def main():
    get_sentence_classification()

    # uvicorn.run("backend.__main__:app", host="127.0.0.1",
    # port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
