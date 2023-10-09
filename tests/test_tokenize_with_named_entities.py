from word_aligner.word_tokenizer import (
    load_spacy_word_tokenizer,
    tokenize_english_with_named_entities,
)


def test_tokenize_english_with_named_entities():
    spacy_nlp = load_spacy_word_tokenizer()
    test_sentence = "Barack Obama has $3000 dollars."
    tokenized_text = tokenize_english_with_named_entities(spacy_nlp, test_sentence)
    expected_text = "Barack+Obama has $+3000+dollars . "

    assert tokenized_text == expected_text
