import utils
import unittest
from rouge_score import rouge_scorer


class TestEval(unittest.TestCase):

    def test(self):
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        reference_text = utils.text
        processed_text = utils.text
        scores = scorer.score(reference_text, processed_text)
        print(scores)
