from lexrank import LexRank, STOPWORDS
from nltk import sent_tokenize
from path import Path


def lexrank_init(corpus_path=None, lang="en"):

    documents = []
    documents_dir = Path(corpus_path)

    for file_path in documents_dir.files('*.txt'):
        with file_path.open(mode='rt', encoding='utf-8') as fp:
            documents.append(fp.readlines())

    return LexRank(documents, stopwords=STOPWORDS[lang])


def lexrank_infer(lxr, text, sent_limit=10):
    assert(isinstance(lxr, LexRank))
    assert(isinstance(text, str))

    sentences = [s.strip() for s in sent_tokenize(text)]
    scores_cont = lxr.rank_sentences(sentences, threshold=None, fast_power_method=False)
    data = [(sentences[i], score) for i, score in enumerate(scores_cont)]
    ordered = sorted(data, key=lambda item: item[1], reverse=True)
    salient_sentences = [s for s, _ in ordered]

    return ' '.join(salient_sentences[:sent_limit])
