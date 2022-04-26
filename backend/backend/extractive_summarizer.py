import scipy
from sentence_transformers import SentenceTransformer
import numpy as np
from nltk.tokenize import sent_tokenize
import logging


class ExtractiveSummariser():
    def __init__(self, threshold, embeddings_path="backend/models/extractive/embeddings.npz", model="all-mpnet-base-v2"):
        self.sentence_model = SentenceTransformer(model)
        self.embeddings = np.load(embeddings_path)["arr_0"]
        self.threshold = threshold

    def _get_embeddings(self, sentences: list[str]) -> list[list[int]]:
        """Returns the embeddings for a given list of sentences

        Args:
            sentences (list[str]): The sentences to create embeddings for

        Returns:
            list[list[int]]: The embeddings for each sentence
        """
        return self.sentence_model.encode(sentences)

    def _classify(self, embedding: list[int]) -> bool:
        """Takes a sentence as returns whether or not it should be kept

        Args:
            sent (str): The sentence to classify
            embedding (list[int]): The embedding for the sentence

        Returns:
            bool: Whether the sentence should be kept in the summary
        """
        distances = scipy.spatial.distance.cdist(
            [embedding], self.embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        return True if 1 - results[0][1] > self.threshold else False

    def summarise(self, doc: str) -> list[str]:
        """Summarises a document using the extractive summariser

        Args:
            doc (str): The document to be summarised, as a string

        Returns:
            list[str]: The resulting sentences, in a list
        """
        sent_tokens = sent_tokenize(doc)

        classified: list[str] = []
        for text, embdg in zip(sent_tokens, self._get_embeddings(sent_tokens)):
            if self._classify(embdg):
                classified.append(text)

        return classified
