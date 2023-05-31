import scipy
from sentence_transformers import SentenceTransformer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


class TestExtractiveSummariser():
    def __init__(self, embeddings_path="backend/models/extractive/embeddings.npz",
                 model="all-mpnet-base-v2", cache_folder=None):
        nltk.download("punkt")
        self.sentence_model = SentenceTransformer(model, cache_folder=cache_folder)
        self.embeddings = np.load(embeddings_path)["arr_0"]

    def _get_embeddings(self, sentences: list[str]) -> list[list[int]]:
        """Returns the embeddings for a given list of sentences

        Args:
            sentences (list[str]): The sentences to create embeddings for

        Returns:
            list[list[int]]: The embeddings for each sentence
        """
        return self.sentence_model.encode(sentences)

    def _get_simiarity(self, embedding):
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

        return 1 - results[0][1]

    def summarise(self, doc, perc_limit=0.1):
        """Summarises a document using the extractive summariser

        Args:
            doc (str): The document to be summarised, as a string

        Returns:
            list[str]: The resulting sentences, in a list
        """
        sent_tokens = sent_tokenize(doc)
        sent_limit = round(len(sent_tokens) * perc_limit)

        # The minimum amount of words to allow in a point
        min_words = 15
        fixed_tokens = []

        for sentence in sent_tokens:
            if len(word_tokenize(sentence)) > min_words:
                fixed_tokens.append(sentence)

        assessed = []
        for text, embdg in zip(fixed_tokens, self._get_embeddings(fixed_tokens)):
            assessed.append((text, self._get_simiarity(embdg)))

        sorted_sentences = sorted([s for s, _ in assessed], key=lambda item: item[1], reverse=True)

        return " ".join(sorted_sentences[:sent_limit])

