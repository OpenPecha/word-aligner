import re
from pathlib import Path

from botok.tokenizers.wordtokenizer import WordTokenizer

from .config import DATA_FOLDER_DIR


def botok_word_tokenizer(text: str, split_affixes=True) -> str:
    # tibetan word tokenizer
    wt = WordTokenizer()
    tokens = wt.tokenize(text, split_affixes=split_affixes)
    tokens_text = " ".join([token.text for token in tokens])
    return tokens_text


def english_word_tokenizer(text) -> str:
    text = re.sub(r'([a-zA-Z])([!?,.":;])', r"\1 \2", text)
    text = re.sub(r'([!?,.":;])([a-zA-Z])', r"\1 \2", text)
    return text


if __name__ == "__main__":
    test_sen = "དེའི་བདག་ཉིད་སྡུག་བསྔལ་བའི་འགྲོ་བ་ལ་སྙིང་རྗེ་བ་གང་ཡིན་པའི་སྙིང་རྗེ་དེའི་ཕྱིར་རོ།།"
    test_sen = Path(DATA_FOLDER_DIR / "test_bo_merged.txt").read_text(encoding="utf-8")
    tokenized = botok_word_tokenizer(test_sen, True)
    print(tokenized)
