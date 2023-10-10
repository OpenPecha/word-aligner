from pathlib import Path
from typing import Dict, List

from word_aligner.config import RESOURCE_FOLDER_DIR


def load_MONLAM_2020_word_dict():
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


def combine_compound_words_MONLAM2020(word_dict: Dict, sentence: str):
    # Input:> sentence = "ས་ ཆེན་ ཀུན་དགའ་ བློ་གྲོས་ ཡིན་པ ས་"
    # output:> sentence = "ས་+ཆེན་+ཀུན་དགའ་+བློ་གྲོས་ ཡིན་པ ས་"
    words = sentence.split()
    i = 0
    while i < len(words):
        first_char = words[i][0]
        if first_char in word_dict:
            for j in range(len(words) - 1, -1, -1):
                current_phrase = "".join(words[i : j + 1])  # noqa
                if current_phrase in word_dict[first_char]:
                    # Replace the phrase with the joined form using "+"
                    words[i] = "+".join(words[i : j + 1])  # noqa
                    del words[i + 1 : j + 1]  # noqa
                    break
        i += 1
    return " ".join(words)


if __name__ == "__main__":
    # Example usage:
    text = "ང་ ས་ ཆེན་ ཀུན་དགའ་ བློ་གྲོས་ ཡིན་"
    MONLAM_2020 = load_MONLAM_2020_word_dict()
    print(combine_compound_words_MONLAM2020(MONLAM_2020, text))
