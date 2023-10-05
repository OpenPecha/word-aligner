from botok.tokenizers.wordtokenizer import WordTokenizer


def botok_word_tokenizer(text: str, split_affixes=True) -> str:
    wt = WordTokenizer()
    return wt.tokenize(text, split_affixes=split_affixes)


if __name__ == "__main__":
    test_sen = "དེའི་བདག་ཉིད་སྡུག་བསྔལ་བའི་འགྲོ་བ་ལ་སྙིང་རྗེ་བ་གང་ཡིན་པའི་སྙིང་རྗེ་དེའི་ཕྱིར་རོ།།"
    tokenized = botok_word_tokenizer(test_sen, False)
    print(tokenized)
