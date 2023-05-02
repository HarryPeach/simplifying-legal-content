from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from nltk.tokenize import sent_tokenize, word_tokenize


class AbstractiveSummariser():
    def __init__(self, model_name: str = "google/bigbird-pegasus-large-arxiv"):
        ...

    def summarise(self, doc: list[str], length: int) -> str:
        """Takes a list of sentences and creates an abstractive simplification

        Args:
            doc (list[str]): The list of sentences

        Returns:
            str: The simplification as a string
        """
        rejoined = " ".join(doc)
        words = word_tokenize(rejoined)
        print(len(words))

        percent_length = length * 0.01
        max_length = int(len(words) * percent_length)

        tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-pegasus")
        model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-pegasus")

        input_tokenized = tokenizer.encode(
            rejoined, return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(input_tokenized,
                                     num_beams=9,
                                     no_repeat_ngram_size=3,
                                     length_penalty=.2,
                                     min_length=150,
                                     max_length=max_length,
                                     early_stopping=True)

        summary = [tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids][0]

        print(summary)
        return summary.replace("<n>", "\n")
