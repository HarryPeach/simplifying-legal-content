from nltk import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer as Summarizer


def lsa_infer(text, language="english", perc_limit=0.1):
    assert(isinstance(text, str))

    # This code is only for calculation of the sentence limit for summary.
    sentences = [s.strip() for s in sent_tokenize(text)]
    sent_limit = round(len(sentences) * perc_limit)

    parser = PlaintextParser.from_string(text, Tokenizer(language))
    stemmer = Stemmer(language)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)

    sentences = summarizer(parser.document, sent_limit)

    return " ".join([str(s).strip() for s in sentences])
