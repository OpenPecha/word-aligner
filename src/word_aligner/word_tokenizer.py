import warnings

import spacy
from botok.tokenizers.wordtokenizer import WordTokenizer


def load_botok_word_tokenizer():
    return WordTokenizer()


def load_spacy_word_tokenizer():
    return spacy.load("en_core_web_sm")


def tokenize_english_with_spacy(spacy_nlp: spacy, text: str) -> str:
    # english word tokenizer
    doc = spacy_nlp(text)
    tokens_text = " ".join([token.text for token in doc])
    return tokens_text


def tokenize_tibetan_with_botok(wt: WordTokenizer, text: str) -> str:
    # tibetan word tokenizer
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        tokens = wt.tokenize(text, split_affixes=True)
        tokens_text = " ".join([token.text for token in tokens])
        return tokens_text


if __name__ == "__main__":
    test_sen = "དེའི་བདག་ཉིད་སྡུག་བསྔལ་བའི་འགྲོ་བ་ལ་སྙིང་རྗེ་བ་གང་ཡིན་པའི་སྙིང་རྗེ་དེའི་ཕྱིར་རོ།།"
    wt = load_botok_word_tokenizer()
    tokenized = tokenize_tibetan_with_botok(wt, test_sen)
    print(tokenized)
