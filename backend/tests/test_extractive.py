import numpy as np
from torch import equal
from backend.extractive_summarizer import ExtractiveSummariser
from expects import expect, be_true, be_false, be


def test_initialisation():
    """Test that initialisation completes without any errors
    """
    _ = ExtractiveSummariser(
        0.7, embeddings_path="tests/resources/embeddings.npz")


def test_get_embeddings():
    """test that embeddings can be created without error
    """
    summariser = ExtractiveSummariser(
        0.7, embeddings_path="tests/resources/embeddings.npz",
        model="all-mpnet-base-v2")

    queries = [
        "regarding the website: if you visit the website your browser automatically transfers certain data so that it can access the website, in particular: the ip address, the date and time of the request, the browser type, the operating system, the language and version of the browser software",
        "for complaints, feedback or questions regarding the services, please contact our support team (see contact info on the websites or in the app).",
    ]

    _ = summariser._get_embeddings(queries)


def test_classify():
    """Test that a sentence is correctly classified
    """
    summariser = ExtractiveSummariser(
        0.7, embeddings_path="tests/resources/embeddings.npz",
        model="all-mpnet-base-v2")

    loaded = np.load("tests/resources/known_embeddings.npz")

    expect(summariser._classify(loaded["sent1"])).to(be_true)
    expect(summariser._classify(loaded["sent2"])).to(be_false)


def test_summarise():
    """Test that the summariser correctly removes sentences that are unneeded
    """
    summariser = ExtractiveSummariser(
        0.7, embeddings_path="tests/resources/embeddings.npz",
        model="all-mpnet-base-v2")

    doc = "Regarding the website: if you visit the website your browser automatically transfers certain data so that it can access the website, in particular: the ip address, the date and time of the request, the browser type, the operating system, the language and version of the browser software. For complaints, feedback or questions regarding the services, please contact our support team (see contact info on the websites or in the app)."

    summarised = summariser.summarise(doc)
    expect(len(summarised)).to(be(1))
