from pathlib import Path
from typing import List

from .config import PUNCTS, RESOURCE_FOLDER_DIR

MONLAM_2020 = (
    Path(RESOURCE_FOLDER_DIR / "སྨོན་2020-headwords.csv")
    .read_text(encoding="utf-8")
    .splitlines()
)


def tokenize_tibetan_word_list(text, word_list: List["str"] = MONLAM_2020) -> str:
    tokens = []  # Initialize an empty list to store tokens

    while text:
        match_found = False
        # Check if the text ends with a punctuation mark
        for punct in PUNCTS:
            if text.endswith(punct):
                tokens.append(punct)
                text = text[: -len(punct)]
                match_found = True
                break
        if match_found:
            continue

        # Start with the longest possible word and try to find a match
        for word in reversed(word_list):
            if text.endswith(word):
                tokens.append(word)  # Add the matched word to the tokens list
                text = text[: -len(word)]  # Remove the matched word from the text
                match_found = True
                break  # Exit the loop and start over with the remaining text
        if match_found:
            continue
        # If no match is found,  a syllable is taken as a token
        if text:
            tsek_last_occur = text.rfind("་")
            if tsek_last_occur == len(text) - 1:
                tsek_last_occur = text[:tsek_last_occur].rfind("་")

            tokens.append(text[tsek_last_occur + 1 :])  # noqa
            text = text[: tsek_last_occur + 1]

    # Reverse the list to maintain the original order of tokens
    tokens.reverse()
    return " ".join(tokens)


if __name__ == "__main__":
    # Example usage:
    text = "དེའི་བདག་ཉིད་སྡུག་བསྔལ་བའི་འགྲོ་བ་ལ་སྙིང་རྗེ་བ་གང་ཡིན་པའི་སྙིང་རྗེ་དེའི་ཕྱིར་རོ།།"
    tokens = tokenize_tibetan_word_list(text)
    print(tokens)
