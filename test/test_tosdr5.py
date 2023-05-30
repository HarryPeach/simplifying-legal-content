import unittest
from backend.extractive_summarizer import ExtractiveSummariser
from rouge_score import rouge_scorer
from tqdm import tqdm

from src.tosdr5 import iter_tosdr5_texts


class TestTOSDR5(unittest.TestCase):

    cache_dir = "./cache"

    def test(self):

        summarizer = ExtractiveSummariser(
            embeddings_path="../backend/backend/models/extractive/embeddings.npz",
            cache_folder=TestTOSDR5.cache_dir)

        raw_texts = iter_tosdr5_texts(type="raw")
        summ_texts = iter_tosdr5_texts(type="summ")

        pred_texts = [" ".join(summarizer.summarise(raw_text, threshold=0.725))
                      for raw_text in tqdm(raw_texts, desc="Extractive model")]

        # Score.
        scores = []
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        for t_pred, t_sum in zip(pred_texts, summ_texts):
            scores.append(scorer.score(target=t_sum, prediction=t_pred))

        r = {}

        for s in scores:
            for v in s:
                if v not in r:
                    r[v] = {"p": [], "r": [], "f": []}
                r[v]["p"].append(s[v][0])
                r[v]["r"].append(s[v][1])
                r[v]["f"].append(s[v][2])

        for m in ["rouge1", "rouge2", "rougeL"]:
            print(sum(r[m]["p"])/len(r[m]["p"]),
                  sum(r[m]["r"])/len(r[m]["r"]),
                  sum(r[m]["f"])/len(r[m]["f"]))
