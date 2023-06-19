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

        hard_words = None
        with open("backend/models/hard_words.txt", "r") as hard_words_list:
            data = hard_words_list.read()
            hard_words = data

        masked_list = []
        for line in input:
            line_copy = line
            for x in line.split(" "):
                if x in hard_words.split("\n"):
                    line_copy = line_copy.replace(x, f"<strong>{mask}</strong>")
                    line_copy = pl(line_copy)[0]["sequence"]
            masked_list.append(line_copy)

        print(masked_list)

        return masked_list
