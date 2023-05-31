import unittest

from backend.extractive_summarizer import ExtractiveSummariser
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.abstract_infer import infer
from src.lsa_infer import lsa_infer
from src.lexrank_init import lexrank_infer, lexrank_init
import utils


class TestSummary(unittest.TestCase):

    cache_dir = "./cache"

    def test_abstract_pegasus_summary(self):
        hf_model_name = "nsi319/legal-pegasus"
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        summary = infer(tokenizer=tokenizer, model=model, text=utils.text, max_length=510)

        print(summary)

    def test_abstract_t5_summary(self):
        hf_model_name = "mrm8488/t5-base-finetuned-summarize-news"
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        summary = infer(tokenizer=tokenizer, model=model, text=utils.text, max_length=510)

        print(summary)

    def test_abstract_longt5_summary(self):
        hf_model_name = "pszemraj/long-t5-tglobal-base-16384-book-summary"
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        summary = infer(tokenizer=tokenizer, model=model, text=utils.text, max_length=1024)

        print(summary)

    def test_extractive(self):
        summarizer = ExtractiveSummariser(embeddings_path="../backend/backend/models/extractive/embeddings.npz",
                                          cache_folder=TestSummary.cache_dir)
        sentences = summarizer.summarise(utils.text, threshold=0.8)
        print(sentences)

    def test_lsa(self):
        summary = lsa_infer(text=utils.text, perc_limit=0.1)
        print(summary)

    def test_lexrank(self):
        lxr = lexrank_init(corpus_path="data/bbc/politics")
        summary = lexrank_infer(lxr, text=utils.text, perc_limit=0.1)
        print(summary)

