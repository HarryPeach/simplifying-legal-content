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


def lexrank_infer(lxr, text, perc_limit=0.1, keep_order=False):
    """ LexRank inference implementation.
        We keep the same order of the information in the result output.
        NOTE: keep_oridering=True performs worser.
    """
    assert(isinstance(lxr, LexRank))
    assert(isinstance(text, str))

    sentences = [s.strip() for s in sent_tokenize(text)]
    sent_limit = round(len(sentences) * perc_limit)
    scores_cont = lxr.rank_sentences(sentences, threshold=None, fast_power_method=False)
    data = [(sentences[i], score) for i, score in enumerate(scores_cont)]
    if keep_order:
        data = [(i, d[0], d[1]) for i, d in enumerate(data)]
        ordered = sorted(data, key=lambda item: item[2], reverse=True)
        salient_sentences = set([i for i, _, _ in ordered][:sent_limit])
        return ' '.join([s for i, s, _ in data if i in salient_sentences])
    else:
        # Most salient first.
        ordered = sorted(data, key=lambda item: item[1], reverse=True)
        salient_sentences = [s for s, _ in ordered]
        return ' '.join(salient_sentences[:sent_limit])
