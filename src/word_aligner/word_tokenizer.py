import re

from botok.tokenizers.wordtokenizer import WordTokenizer


def botok_word_tokenizer(wt: WordTokenizer, text: str, split_affixes=True) -> str:
    # tibetan word tokenizer
    tokens = wt.tokenize(text, split_affixes=split_affixes)
    tokens_text = " ".join([token.text for token in tokens])
    return tokens_text


def english_word_tokenizer(text) -> str:
    text = re.sub(r'([a-zA-Z])([!?,.":;])', r"\1 \2", text)
    text = re.sub(r'([!?,.":;])([a-zA-Z])', r"\1 \2", text)
    return text


if __name__ == "__main__":
    test_sen = "དེའི་བདག་ཉིད་སྡུག་བསྔལ་བའི་འགྲོ་བ་ལ་སྙིང་རྗེ་བ་གང་ཡིན་པའི་སྙིང་རྗེ་དེའི་ཕྱིར་རོ།།"
    wt = WordTokenizer()
    tokenized = botok_word_tokenizer(wt, test_sen, True)
    print(tokenized)
