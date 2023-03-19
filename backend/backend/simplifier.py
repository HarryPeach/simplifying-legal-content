import torch
from transformers import pipeline


# text = """To provide the Meta Products, we must process information about you. The type of information that we collect depends on how you use our Products. You can learn how to access and delete information that we collect by visiting the Facebook settings and Instagram settings. Things that you and others do"""


class SimplificationModel():
    def __init__(self):
        ...

    def simplify(self, input: str):
        model_path = 'mayankb96/bert-base-uncased-finetuned-lexglue'
        pl = pipeline(model=model_path)
        mask = pl.tokenizer.mask_token

        print(mask)

        print(pl("This is a [MASK] phrase"))

        # tokenizer = BertTokenizer.from_pretrained(bert_model)
        # model = BertForMaskedLM.from_pretrained(bert_model)
        # model.eval()

        # text = "To provide the Meta Products, we must process information about you. The type of information that we collect depends on how you use our Products."

        # encoded_input = tokenizer(input, return_tensors="pt")
        # output = model(**encoded_input)

        # print(output)
