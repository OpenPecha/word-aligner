from pathlib import Path
from typing import Dict, List

from word_aligner.config import PUNCTS, RESOURCE_FOLDER_DIR


def load_MONLAM_2020_word_list():
    MONLAM_2020 = (
        Path(RESOURCE_FOLDER_DIR / "སྨོན་2020-headwords.csv")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    MONLAM_2020_word_dict = group_words_by_first_character(MONLAM_2020)
    return MONLAM_2020_word_dict


def group_words_by_first_character(word_list: List[str]) -> dict:
    # Create a dictionary with the first character of each word as the key
    word_dict: Dict = {}
    for word in word_list:
        first_char = word[0]
        if first_char not in word_dict:
            word_dict[first_char] = []
        word_dict[first_char].append(word)

    # Sort the words within each group by length in descending order
    for _, words in word_dict.items():
        words.sort(key=lambda x: len(x), reverse=True)

    return word_dict


def tokenize_tibetan_word_list(text, word_dict: dict) -> str:
    tokens = []
    index = 0

    while index < len(text):
        match_found = False
        first_char = text[index]

        # Check if the first character of the text matches any key in the word_dict
        if first_char in word_dict:
            for word in word_dict[first_char]:
                if text.startswith(word, index):
                    tokens.append(word)
                    index += len(word)
                    match_found = True
                    break

        if match_found:
            continue

        # Check if the text starting at the current index matches any punctuation
        for punct in PUNCTS:
            if text.startswith(punct, index):
                tokens.append(punct)
                index += len(punct)
                match_found = True
                break

        if not match_found:
            tsek_next_occur = text.find("་", index)
            if tsek_next_occur == -1:
                tsek_next_occur = len(text)

            tokens.append(text[index : tsek_next_occur + 1])  # noqa
            index = tsek_next_occur + 1

    return " ".join(tokens)


if __name__ == "__main__":
    # Example usage:
    text = "དེའི་བདག་ཉིད་སྡུག་བསྔལ་བའི་འགྲོ་བ་ལ་སྙིང་རྗེ་བ་གང་ཡིན་པའི་སྙིང་རྗེ་དེའི་ཕྱིར་རོ།།"
    MONLAM_2020 = load_MONLAM_2020_word_list()
    tokens = tokenize_tibetan_word_list(text, MONLAM_2020)
    print(tokens)
