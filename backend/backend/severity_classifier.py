import torch
from torch import nn
from torchtext.data.utils import get_tokenizer

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

    def get_classification(self, sentence):
        return CLASSIFICATION_LABEL[self.predict(sentence, self.text_pipeline)]
