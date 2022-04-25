import torch
from torch import nn
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

# class TextClassificationModel(nn.Module):

#     def __init__(self, vocab_size, embed_dim, num_class):
#         super(TextClassificationModel, self).__init__()
#         self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
#         self.fc = nn.Linear(embed_dim, num_class)
#         self.init_weights()

#     def init_weights(self):
#         initrange = 0.5
#         self.embedding.weight.data.uniform_(-initrange, initrange)
#         self.fc.weight.data.uniform_(-initrange, initrange)
#         self.fc.bias.data.zero_()

#     def forward(self, text, offsets):
#         embedded = self.embedding(text, offsets)
#         return self.fc(embedded)

tokenizer = get_tokenizer("basic_english")


def yield_tokens(data_iter):
    for _, text in data_iter:
        yield tokenizer(text)


def get_sentence_classification():
    vocab = torch.load("sev_vocab.pt")
    def text_pipeline(x): return vocab(tokenizer(x))

    def predict(text, text_pipeline):
        with torch.no_grad():
            text = torch.tensor(text_pipeline(text)).to(torch.int64)
            output = model(text, torch.tensor([0]))
            return output.argmax(1).item()

    model = torch.jit.load("sev_scripted.pt")
    model.eval()

    ag_news_label = {0: "bad",
                     1: "blocker",
                     2: "good",
                     3: "neutral"}

    ex_text_str = "there is no duty to keep that information confidential or to discontinue or forego any representation"

    print("This is a %s point" %
          ag_news_label[predict(ex_text_str, text_pipeline)])
