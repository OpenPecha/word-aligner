from pathlib import Path
from typing import Dict, List

from botok import TSEK

from word_aligner.config import RESOURCE_FOLDER_DIR
from word_aligner.data_processor import add_tsek_if_missing_in_list, normalise_tsek


def load_MONLAM_2020_word_list():
    MONLAM_2020 = Path(RESOURCE_FOLDER_DIR / "སྨོན་2020-headwords.csv").read_text(
        encoding="utf-8"
    )
    MONLAM_2020_word_list = normalise_tsek(MONLAM_2020).splitlines()
    MONLAM_2020_word_list = add_tsek_if_missing_in_list(MONLAM_2020_word_list)
    return MONLAM_2020_word_list


def load_mahavyutpatti_word_list():
    mahavyutpatti = Path(RESOURCE_FOLDER_DIR / "mahavyutpatti.csv").read_text(
        encoding="utf-8"
    )
    mahavyutpatti_word_list = normalise_tsek(mahavyutpatti).splitlines()
    # Filtering only tibetan words
    mahavyutpatti_word_list = [
        line.split(",")[0].strip() for line in mahavyutpatti_word_list
    ]
    mahavyutpatti_word_list = add_tsek_if_missing_in_list(mahavyutpatti_word_list)
    return mahavyutpatti_word_list


def load_all_word_list():
    word_list = load_MONLAM_2020_word_list() + load_mahavyutpatti_word_list()
    word_list = list(set(word_list))
    return word_list


def load_tibetan_word_dictionary(word_list: List[str] = load_all_word_list()):
    word_dict = group_words_by_first_character(word_list)
    return word_dict


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


def merge_tibetan_compound_words(word_dict: Dict, sentence: str):
    # Input:> sentence = "ས་ ཆེན་ ཀུན་དགའ་ བློ་གྲོས་ ཡིན་པ ས་"
    # output:> sentence = "ས་+ཆེན་+ཀུན་དགའ་+བློ་གྲོས་ ཡིན་པ ས་"
    words = sentence.split()
    i = 0
    while i < len(words):
        first_char = words[i][0]
        if first_char in word_dict:
            for j in range(len(words) - 1, -1, -1):
                current_phrase = "".join(words[i : j + 1])  # noqa
                is_end_tsek = current_phrase[-1] in ["་", "ཿ"]
                if current_phrase in word_dict[first_char]:
                    # Replace the phrase with the joined form using "+"
                    words[i] = "+".join(words[i : j + 1])  # noqa
                    del words[i + 1 : j + 1]  # noqa
                    break
                elif not is_end_tsek and current_phrase + TSEK in word_dict[first_char]:
                    # If is_end_tsek is False, check for current_phrase + "་"
                    words[i] = "+".join(words[i : j + 1])  # noqa
                    del words[i + 1 : j + 1]  # noqa
                    break
        i += 1
    return " ".join(words)


if __name__ == "__main__":
    # Example usage:
    word_list = load_all_word_list()
    word_list = "\n".join(word_list)
    Path(RESOURCE_FOLDER_DIR / "all_words.txt").write_text(word_list)
