import scipy
from sentence_transformers import SentenceTransformer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import logging


class ExtractiveSummariser():
    def __init__(self, embeddings_path="backend/models/extractive/embeddings.npz", model="all-mpnet-base-v2"):
        nltk.download("punkt")
        self.sentence_model = SentenceTransformer(model)
        self.embeddings = np.load(embeddings_path)["arr_0"]

    def _get_embeddings(self, sentences: list[str]) -> list[list[int]]:
        """Returns the embeddings for a given list of sentences

        Args:
            sentences (list[str]): The sentences to create embeddings for

        Returns:
            list[list[int]]: The embeddings for each sentence
        """
        return self.sentence_model.encode(sentences)

    def _classify(self, embedding: list[int], threshold: float) -> bool:
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

        return True if 1 - results[0][1] > threshold else False

    def summarise(self, doc: str, threshold: float) -> list[str]:
        """Summarises a document using the extractive summariser

        Args:
            doc (str): The document to be summarised, as a string
            threshold (float): The threshold of similarity before dropping sentences

        Returns:
            list[str]: The resulting sentences, in a list
        """
        sent_tokens = sent_tokenize(doc)

        # The minimum amount of words to allow in a point
        min_words = 15
        fixed_tokens = []

        for sentence in sent_tokens:
            if len(word_tokenize(sentence)) > min_words:
                fixed_tokens.append(sentence)

        classified: list[str] = []
        for text, embdg in zip(fixed_tokens, self._get_embeddings(fixed_tokens)):
            if self._classify(embdg, threshold):
                classified.append(text)

        return classified
