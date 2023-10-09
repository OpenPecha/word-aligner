import warnings

import spacy
from botok.tokenizers.wordtokenizer import WordTokenizer


def load_botok_word_tokenizer():
    return WordTokenizer()


def load_spacy_word_tokenizer():
    return spacy.load("en_core_web_sm")


def tokenize_english_with_spacy(spacy_nlp: spacy, text: str, lemma=False) -> str:
    # english word tokenizer
    doc = spacy_nlp(text)
    if lemma:
        tokens_text = " ".join([token.lemma_ for token in doc])
    else:
        tokens_text = " ".join([token.text for token in doc])
    return tokens_text


def tokenize_english_with_named_entities(
    spacy_nlp: spacy, text: str, lemma=False
) -> str:
    # english word tokenizer
    doc = spacy_nlp(text)
    tokens_text = ""
    idx = 0
    while idx < len(doc):
        token = doc[idx]
        if token.ent_type_ == "":
            tokens_text += f"{token.lemma} "
            idx += 1
        else:
            curr_entity = token.ent_type_
            index = idx
            while index < len(doc) and doc[index].ent_type_ == curr_entity:
                index += 1
            curr_entity_word = [f"{doc[i].text}" for i in range(idx, index)]
            tokens_text += "+".join(curr_entity_word)
            idx = index
            tokens_text += " "
    return tokens_text


def tokenize_tibetan_with_botok(
    wt: WordTokenizer, text: str, split_affix=True, lemma=False
) -> str:
    # tibetan word tokenizer
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        tokens = wt.tokenize(text, split_affixes=split_affix)
        if lemma:
            tokens_text = " ".join([token.lemma for token in tokens])
        else:
            tokens_text = " ".join([token.text for token in tokens])
        return tokens_text


if __name__ == "__main__":
    spacy_nlp = load_spacy_word_tokenizer()
    test_sentence = "Barack Obama has $3000 dollars."
    print(tokenize_english_with_named_entities(spacy_nlp, test_sentence))
