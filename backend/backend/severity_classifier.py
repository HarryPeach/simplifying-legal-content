import torch
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
        self.vocab = torch.load("backend/models/severity/vocab.pt")
        self.model = torch.jit.load(
            "backend/models/severity/scripted_model.pt")

        # Initialise model for evaluation mode
        self.model.eval()

    def _text_pipeline(self, x) -> None:
        return self.vocab(self.tokenizer(x))

    def _yield_tokens(self, data_iter) -> None:
        for _, text in data_iter:
            yield self.tokenizer(text)

    def _predict(self, text, text_pipeline) -> None:
        with torch.no_grad():
            text = torch.tensor(text_pipeline(text)).to(torch.int64)
            output = self.model(text, torch.tensor([0]))
            return output.argmax(1).item()

    def classify_document(self, sentences: list[str]) -> list[dict[str, str]]:
        """Returns the classifications of each sentence in a document

        Args:
            sentences (list[str]): The list of sentences to classify 

        Returns:
            list[dict[str, str]]: The list of sentences and their classifications as found in the CLASSIFICATION_LABEL dict
        """
        classifications = []
        for sentence in sentences:
            classifications.append(
                {
                    "text": sentence,
                    "classification": self.classify_sentence(sentence)
                }
            )

        return classifications

    def classify_sentence(self, sentence: str) -> str:
        """Classifies a sentence

        Args:
            sentence (str): The sentence to be classified

        Returns:
            CLASSIFICATION_LABEL: The classification on the sentence
        """
        return CLASSIFICATION_LABEL[self._predict(sentence, self._text_pipeline)]
