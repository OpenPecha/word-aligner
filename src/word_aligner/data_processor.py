import re
from typing import List

from botok import TSEK

from word_aligner.config import CLOSING_PUNCTS_CHAR_SET


def remove_number_emojis(text: str) -> str:
    # 1️⃣, 2️⃣, 3️⃣ annotations were used for machine translation evaluation
    return text.replace("1️⃣", "").replace("2️⃣", "").replace("3️⃣", "")


def keep_only_tibetan_characters(text: str) -> str:
    return re.sub(r"[^\u0F00-\u0FFF\s\n\t]+", r"", text)


def keep_only_ascii_characters(text: str) -> str:
    # keep only ascii characters
    return re.sub(r"[^\x00-\x7F]", r"", text)


def keep_neccessary_english_characters(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s\n\t\.\,\?\!\'\$\&\+\%]+", r"", text)


def filter_for_english_dictionary_words(text: str) -> str:
    # if non neccessary ascii characters was in between
    text = re.sub(r"[*|+]{1}[^a-zA-Z0-9\-\$\*\+\']+[*|+]{1}", r"*", text)
    # if non neccessary ascii characters was in beginning or end
    text = re.sub(r"[*|+]{0,1}[^a-zA-Z0-9\-\$\*\+\']+[*|+]{0,1}", r"", text)
    return text


def filter_for_tibetan_dictionary_words(text: str) -> str:
    # if closing_puncts was in between
    pattern = r"[*|+]{1}" + CLOSING_PUNCTS_CHAR_SET + "+[*|+]{1}"
    text = re.sub(pattern, r"*", text)
    # if closing_puncts was in beginning or end
    pattern = r"[*|+]{0,1}" + CLOSING_PUNCTS_CHAR_SET + "+[*|+]{0,1}"
    text = re.sub(pattern, r"", text).strip()
    return text


def normalise_tsek(text: str) -> str:
    return re.sub(r"[་༌]", TSEK, text)


def clean_tibetan_text(text: str) -> str:
    text = clean_text(text)
    text = keep_only_tibetan_characters(text)
    text = normalise_tsek(text)
    text = re.sub(r"[ ]+", "", text).strip()
    return text


def clean_english_text(text: str) -> str:
    text = clean_text(text)
    text = keep_only_ascii_characters(text)
    text = keep_neccessary_english_characters(text)
    text = re.sub(r"[ ]+", " ", text).strip()
    return text


def clean_text(text: str) -> str:
    text = remove_number_emojis(text)
    return text


def add_tsek_if_missing_in_list(word_list: List) -> list:
    normalised_word_list = [
        word + TSEK if word[-1] not in ["་", "ཿ"] else word for word in word_list
    ]
    return normalised_word_list


if __name__ == "__main__":

    # Example usage:
    input_text = "This is a བཀྲ་ཤིས་sample བདེ་ལེགས་ text."
    filtered_text = clean_english_text(input_text)
    print(filtered_text)
