import torch
from torchtext.data.utils import get_tokenizer
from nltk.tokenize import sent_tokenize

CLASSIFICATION_LABEL = {
    0: "bad",
    1: "blocker",
    2: "good",
    3: "neutral"
}


class SeverityClassifier():
    def __init__(self):
        self.tokenizer = get_tokenizer("basic_english")
        self.vocab = torch.load("sev_vocab.pt")
        self.model = torch.jit.load("sev_scripted.pt")

        # Initialise model for evaluation mode
        self.model.eval()

    def text_pipeline(self, x):
        return self.vocab(self.tokenizer(x))

    def yield_tokens(self, data_iter):
        for _, text in data_iter:
            yield self.tokenizer(text)

    def predict(self, text, text_pipeline):
        with torch.no_grad():
            text = torch.tensor(text_pipeline(text)).to(torch.int64)
            output = self.model(text, torch.tensor([0]))
            return output.argmax(1).item()

    def classify_document(self, doc: str) -> list[tuple[str, dict]]:
        """Returns the classifications of each sentence in a document

        Args:
            doc (str): The document as a string

        Returns:
            list[tuple[str, dict]]: The list of sentences and their classifications as found in the CLASSIFICATION_LABEL dict
        """
        sent_tokens = sent_tokenize(doc)

        classifications = []
        for sentence in sent_tokens:
            classifications.append(
                (sentence, self.classify_sentence(sentence)))

        return classifications

    def classify_sentence(self, sentence: str):
        """Classifies a sentence

        Args:
            sentence (str): The sentence to be classified

        Returns:
            CLASSIFICATION_LABEL: The classification on the sentence
        """
        return CLASSIFICATION_LABEL[self.predict(sentence, self.text_pipeline)]
