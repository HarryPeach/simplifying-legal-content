import scipy
from sentence_transformers import SentenceTransformer
import numpy as np
from nltk.tokenize import sent_tokenize


class ExtractiveSummarizer():
    def __init__(self):
        self.sentence_model = SentenceTransformer("all-mpnet-base-v2")
        self.embeddings = np.load("models/extractives/embeddings.npz")["arr_0"]

    def _get_embeddings(self, sentences: list[str]) -> list[list[int]]:
        """Returns the embeddings for a given list of sentences

        Args:
            sentences (list[str]): The sentences to create embeddings for

        Returns:
            list[list[int]]: The embeddings for each sentence
        """
        return self.sentence_model.encode(sentences)

    def _classify(self, sent: str) -> bool:
        """Takes a sentence as returns whether or not it should be kept

        Args:
            sent (str): The sentence to classify

        Returns:
            bool: Whether the sentence should be kept in the summary
        """
        ...

    def summarise(self, doc: str) -> list[str]:
        """Summarises a document using the extractive summariser

        Args:
            doc (str): The document to be summarised, as a string

        Returns:
            list[str]: The resulting sentences, in a list
        """
        sent_tokens = sent_tokenize(doc)
