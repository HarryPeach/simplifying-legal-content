def infer(model, tokenizer, text, max_length):
    input_tokenized = tokenizer.encode(
        text, return_tensors='pt', max_length=max_length, truncation=True)
    summary_ids = model.generate(input_tokenized,
                                 num_beams=9,
                                 no_repeat_ngram_size=3,
                                 length_penalty=.2,
                                 min_length=150,
                                 max_length=max_length,
                                 early_stopping=True)

    summary = [tokenizer.decode(
        g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids][0]

    return summary
