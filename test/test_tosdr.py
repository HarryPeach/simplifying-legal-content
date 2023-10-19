import gc
import os
import unittest
from os.path import join, dirname

from rouge_score import rouge_scorer
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.tosdr_dataset import iter_tosdr_dataset_texts
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
        summ_texts_orig = list(iter_tosdr_dataset_texts(type="summ", dataset_filename="tos-dr-10.zip"))
        summ_texts_pred = list(iter_tosdr_dataset_texts(type="summ", dataset_filename="tos-dr-chatgpt4.zip"))
        self.score(pred_texts=summ_texts_pred, summ_texts=summ_texts_orig)

    def test_prepare_prompt_and_texts(self):
        raw_texts = list(iter_tosdr_dataset_texts(type="raw", dataset_filename="tos-dr-10.zip", return_name=True))

        if not os.path.exists("out"):
            os.makedirs("out")
            
        prompt = "Provide the raw text summary in a single paragraph for the following document: "

        for name, raw_text in raw_texts:
            raw_text = raw_text.replace("\n"," ")
            r = prompt + "\n" + raw_text
            content = r[:16000]
            with open(f"out/{name}", "w") as f:
                f.write(content)

    def test(self):

        summarizer = TestExtractiveSummariser(
            embeddings_path="../backend/backend/models/extractive/embeddings.npz",
            cache_folder=TestTOSDR5.cache_dir)

        raw_texts = list(iter_tosdr_dataset_texts(type="raw", dataset_filename="tos-dr-10.zip"))
        summ_texts = list(iter_tosdr_dataset_texts(type="summ", dataset_filename="tos-dr-10.zip"))

        lxr = lexrank_init(corpus_path=join(dirname(__file__), "data/bbc/politics"))

        models = {
            # Extractive
            "lsa": lambda texts: [lsa_infer(t, perc_limit=0.1) for t in tqdm(texts, desc="LSA")],
            "ex": lambda texts, perc=0.1: [summarizer.summarise(t, perc_limit=perc) for t in tqdm(texts, desc="Extractive")],
            "lexrank": lambda texts, perc=0.1: [lexrank_infer(lxr, text=t, perc_limit=perc) for t in tqdm(texts, desc="LexRank")],
            # Abstractive.
            "legal-pegasus": lambda texts: tqdm(self.abstract(hf_model_name="nsi319/legal-pegasus", texts=texts, max_length=512), desc="Abstract (Legal-PEGASUS)"),
            "t5": lambda texts: tqdm(self.abstract(hf_model_name="mrm8488/t5-base-finetuned-summarize-news", texts=texts, max_length=512), desc="Abstract (T5)"),
            "longt5": lambda texts: tqdm(self.abstract(hf_model_name="pszemraj/long-t5-tglobal-base-16384-book-summary", texts=texts, max_length=1020), desc="Abstract (LongT5-TGlobal)"),
            "distilbart": lambda texts: tqdm(self.abstract(hf_model_name="ml6team/distilbart-tos-summarizer-tosdr", texts=texts, max_length=512), desc="Abstract (distil-BART)"),
            # Hybrid
            "ex-legal-pegasus": lambda texts: models["legal-pegasus"](models["ex"](texts, perc=0.5)),
            "ex-t5": lambda texts: models["t5"](models["ex"](texts=texts, perc=0.5)),
            "ex-longt5": lambda texts: models["longt5"](models["ex"](texts=texts, perc=0.5)),
            "ex-distilbart": lambda texts: models["distilbart"](models["ex"](texts=texts, perc=0.5)),
            # Hybrid based on lexrank.
            "lexrank-legal-pegasus": lambda texts: models["legal-pegasus"](models["lexrank"](texts, perc=0.5)),
            "lexrank-t5": lambda texts: models["t5"](models["lexrank"](texts, perc=0.5)),
            "lexrank-longt5": lambda texts: models["longt5"](models["lexrank"](texts, perc=0.5)),
            "lexrank-distilbart": lambda texts: models["distilbart"](models["lexrank"](texts, perc=0.5)),
        }

        for m_name in [#"lsa",
                       #"lexrank",
                       #"ex",
                       #"legal-pegasus", "t5", "longt5",
                       # "distilbart",
                       # "ex-t5", "ex-longt5",
                       "ex-legal-pegasus",
                       #"ex-distilbart",
                       #"lexrank-t5",
                       #"lexrank-longt5",
                       #"lexrank-legal-pegasus",
                       #"lexrank-distilbart"
        ]:
            if m_name in models:
                m = models[m_name]
                self.score(pred_texts=m(raw_texts), summ_texts=summ_texts)
