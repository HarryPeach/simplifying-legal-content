import gc
import unittest
from os.path import join, dirname

from rouge_score import rouge_scorer
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.tosdr5 import iter_tosdr5_texts
from src.lsa_infer import lsa_infer
from src.lexrank_init import lexrank_init, lexrank_infer
from src.abstract_infer import infer
from src.extractive import TestExtractiveSummariser


class TestTOSDR5(unittest.TestCase):

    cache_dir = "./cache"

    def pred_texts_extractor(self, raw_texts):
        return

    def abstract(self, hf_model_name, texts, max_length):
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, cache_dir=TestTOSDR5.cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name, cache_dir=TestTOSDR5.cache_dir)
        for t in texts:
            yield infer(model, tokenizer, text=t, max_length=max_length)
        gc.collect()

    def score(self, pred_texts, summ_texts):

        scores = []
        metrics = ['rouge1', 'rouge2', 'rougeL']
        scorer = rouge_scorer.RougeScorer(metrics, use_stemmer=True)
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

        for m in metrics:
            print("{}/{}/{} &".format(
                round(sum(r[m]["p"]) / len(r[m]["p"]), 3),
                round(sum(r[m]["r"]) / len(r[m]["r"]), 3),
                round(sum(r[m]["f"]) / len(r[m]["f"]), 3)))

    def test_gpt(self):
        summ_texts_orig = list(iter_tosdr5_texts(type="summ"))
        summ_texts_pred = list(iter_tosdr5_texts(type="summ", dataset_filename="tos-dr-chatgpt4.zip"))
        self.score(pred_texts=summ_texts_pred, summ_texts=summ_texts_orig)

    def test(self):

        summarizer = TestExtractiveSummariser(
            embeddings_path="../backend/backend/models/extractive/embeddings.npz",
            cache_folder=TestTOSDR5.cache_dir)

        raw_texts = list(iter_tosdr5_texts(type="raw"))
        summ_texts = list(iter_tosdr5_texts(type="summ"))

        lxr = lexrank_init(corpus_path=join(dirname(__file__), "data/bbc/politics"))

        models = {
            # Extractive
            "lsa": lambda texts: [lsa_infer(t, perc_limit=0.1) for t in tqdm(texts, desc="LSA")],
            "ex": lambda texts: [summarizer.summarise(t, perc_limit=0.5) for t in tqdm(texts, desc="Extractive")],
            "lexrank": lambda texts: [lexrank_infer(lxr, text=t, perc_limit=0.5) for t in tqdm(texts, desc="LexRank")],
            # Abstractive.
            "legal-pegasus": lambda texts: tqdm(self.abstract(hf_model_name="nsi319/legal-pegasus", texts=texts, max_length=512), desc="Abstract (Legal-PEGASUS)"),
            "t5": lambda texts: tqdm(self.abstract(hf_model_name="mrm8488/t5-base-finetuned-summarize-news", texts=texts, max_length=512), desc="Abstract (T5)"),
            "longt5": lambda texts: tqdm(self.abstract(hf_model_name="pszemraj/long-t5-tglobal-base-16384-book-summary", texts=texts, max_length=1020), desc="Abstract (LongT5-TGlobal)"),
            "distilbart": lambda texts: tqdm(self.abstract(hf_model_name="ml6team/distilbart-tos-summarizer-tosdr", texts=texts, max_length=512), desc="Abstract (distil-BART)"),
            # Hybrid
            "ex-legal-pegasus": lambda texts: models["legal-pegasus"](models["ex"](texts)),
            "ex-t5": lambda texts: models["t5"](models["ex"](texts)),
            "ex-longt5": lambda texts: models["longt5"](models["ex"](texts)),
            "ex-distilbart": lambda texts: models["distilbart"](models["ex"](texts)),
            # Hybrid based on lexrank.
            "lexrank-legal-pegasus": lambda texts: models["legal-pegasus"](models["lexrank"](texts)),
            "lexrank-t5": lambda texts: models["t5"](models["lexrank"](texts)),
            "lexrank-longt5": lambda texts: models["longt5"](models["lexrank"](texts)),
            "lexrank-distilbart": lambda texts: models["distilbart"](models["lexrank"](texts)),
        }

        for m_name in [#"lsa",
                       #"lexrank",
                       #"ex",
                       #"legal-pegasus", "t5", "longt5",
                       # "distilbart",
                       # "ex-t5", "ex-longt5","ex-legal-pegasus",
                       "ex-distilbart",
                       #"lexrank-t5",
                       #"lexrank-longt5",
                       #"lexrank-legal-pegasus",
                       "lexrank-distilbart"]:
            if m_name in models:
                m = models[m_name]
                self.score(pred_texts=m(raw_texts), summ_texts=summ_texts)
