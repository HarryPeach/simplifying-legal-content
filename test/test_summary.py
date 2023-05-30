import unittest

from backend.extractive_summarizer import ExtractiveSummariser
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from src.abstract_infer import infer
from src.lsa_infer import lsa_infer
from src.lexrank_init import lexrank_infer, lexrank_init


class TestSummary(unittest.TestCase):

    cache_dir = "./cache"

    text = "The people of the State of California do enact as follows:\n\n\nSECTION 1.\nSection 10295." \
           "35 is added to the Public Contract Code, to read:\n10295.35.\n(a) (1) Notwithstanding any other " \
           "law, a state agency shall not enter into any contract for the acquisition of goods or services in the " \
           "amount of one hundred thousand dollars ($100,000) or more with a contractor that, in the provision of " \
           "benefits, discriminates between employees on the basis of an employee’s or dependent’s actual or " \
           "perceived gender identity, including, but not limited to, the employee’s or dependent’s identification " \
           "as transgender.\n(2) For purposes of this section, “contract” includes contracts with a cumulative " \
           "amount of one hundred thousand dollars ($100,000) or more per contractor in each fiscal year.\n(3) " \
           "For purposes of this section, an employee health plan is discriminatory if the plan is not consistent " \
           "with Section 1365.5 of the Health and Safety Code and Section 10140 of the Insurance Code.\n(4) "

    def test_abstract_pegasus_summary(self):
        hf_model_name = "nsi319/legal-pegasus"
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        summary = infer(tokenizer=tokenizer, model=model, text=TestSummary.text, max_length=510)

        print(summary)

    def test_abstract_t5_summary(self):
        hf_model_name = "mrm8488/t5-base-finetuned-summarize-news"
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        summary = infer(tokenizer=tokenizer, model=model, text=TestSummary.text, max_length=510)

        print(summary)

    def test_abstract_longt5_summary(self):
        hf_model_name = "pszemraj/long-t5-tglobal-base-16384-book-summary"
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name, cache_dir=TestSummary.cache_dir)
        summary = infer(tokenizer=tokenizer, model=model, text=TestSummary.text, max_length=1024)

        print(summary)

    def test_extractive(self):
        summarizer = ExtractiveSummariser(embeddings_path="../backend/backend/models/extractive/embeddings.npz",
                                          cache_folder=TestSummary.cache_dir)
        sentences = summarizer.summarise(TestSummary.text, threshold=0.8)
        print(sentences)

    def test_lsa(self):
        summary = lsa_infer(text=TestSummary.text)
        print(summary)

    def test_lexrank(self):
        lxr = lexrank_init(corpus_path="data/bbc/politics")
        summary = lexrank_infer(lxr, text=TestSummary.text)
        print(summary)

