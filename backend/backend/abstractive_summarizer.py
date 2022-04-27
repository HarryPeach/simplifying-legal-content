from transformers import pipeline
import torch


class AbstractiveSummariser():
    def __init__(self, model_name: str = "google/bigbird-pegasus-large-arxiv"):
        ...

    def summarise(self, doc: list[str]) -> str:
        """Takes a list of sentences and creates an abstractive simplification

        Args:
            doc (list[str]): The list of sentences

        Returns:
            str: The simplification as a string
        """
        rejoined = " ".join(doc)
        summariser = pipeline(
            "summarization", model="t5-base")
        return summariser(rejoined)[0]["summary_text"]
