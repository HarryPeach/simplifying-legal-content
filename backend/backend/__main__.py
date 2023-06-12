from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.simplifier import SimplificationModel
from backend.abstractive_summarizer import AbstractiveSummariser
from backend.severity_classifier import SeverityClassifier
from backend.extractive_summarizer import ExtractiveSummariser

import uvicorn
import lorem
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXTRACTIVE_SUMMARISER = ExtractiveSummariser()
ABSTRACTIVE_SUMMARISER = AbstractiveSummariser()
SEVERITY_CLASSIFER = SeverityClassifier()
SIMPLIFIER = SimplificationModel()


class ExtractiveInputItem(BaseModel):
    """The input body for an extractive summarisation request
    """
    text: str
    threshold: float


@app.post("/extractive/")
async def get_extractive(item: ExtractiveInputItem):
    return EXTRACTIVE_SUMMARISER.summarise(item.text, item.threshold)


class SeverityClassiferItem(BaseModel):
    """The input body for a severity classification
    """
    items: list[str]


@app.post("/severity/")
async def get_severity(item: SeverityClassiferItem):
    return SEVERITY_CLASSIFER.classify_document(item.items)


class AbstractiveSummaryItem(BaseModel):
    """The input body for an abstractive summary
    """
    text: list[str]
    length: int


@app.post("/abstractive/")
async def get_abstractive(item: AbstractiveSummaryItem):
    return ABSTRACTIVE_SUMMARISER.summarise(item.text, item.length)


class SimplificationModelItem(BaseModel):
    """The input body for a simplification
    """
    text: list[str]


@app.post("/simplify/")
async def get_simplified(item: SimplificationModelItem):
    return SIMPLIFIER.simplify(item.text)


@app.get("/")
async def read_root():
    return {
        "abstractive": lorem.paragraph(),
        "extractive": "This is an extractive simplification",
    }


def main():
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run("backend.__main__:app", host="0.0.0.0",
                port=8000, reload=True, workers=2)


if __name__ == "__main__":
    main()
