import unittest

from backend.extractive_summarizer import ExtractiveSummariser

from src.tosdr5 import iter_tosdr5_texts


class TestTOSDR5(unittest.TestCase):

    cache_dir = "./cache"

    def test(self):

        summarizer = ExtractiveSummariser(
            embeddings_path="../backend/backend/models/extractive/embeddings.npz",
            cache_folder=TestTOSDR5.cache_dir)

        for text in iter_tosdr5_texts():
            print(text)
            sentences = summarizer.summarise(text, threshold=0.725)
            print(sentences)
