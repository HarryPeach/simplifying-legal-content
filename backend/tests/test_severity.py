from expects import expect, equal, contain
from backend.severity_classifier import SeverityClassifier, CLASSIFICATION_LABEL


def test_document_classify_format():
    """Test that a classified document contains the same number of sentences as the original document and each contains a classification
    """
    sample_document = [
        "By using our Products, you agree that we can show you ads that we think will be relevant to you and your interests.",
        "We use your personal data to help determine which ads to show you.",
        "We don't sell your personal data to advertisers.",
        "Our Data Policy explains how we collect and use your personal data to determine some of the ads that you see and provide all of the other services described below."
    ]

    classifier = SeverityClassifier()
    classified = classifier.classify_document(sample_document)

    expect(len(classified)).to(equal(len(sample_document)))

    for classification in classified:
        expect(CLASSIFICATION_LABEL.values()).to(
            contain(classification["classification"]))
