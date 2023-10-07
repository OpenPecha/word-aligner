import re


def remove_number_emojis(text: str) -> str:
    # 1️⃣, 2️⃣, 3️⃣ annotations were used for machine translation evaluation
    return text.replace("1️⃣", "").replace("2️⃣", "").replace("3️⃣", "")


def keep_only_tibetan_characters(text: str) -> str:
    return re.sub(r"[^\u0F00-\u0FFF\s\n\t]+", r"", text)


def keep_only_english_characters(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s\n\t]+", r"", text)


def normalise_punctuation(text: str) -> str:
    text = re.sub(r"[\{\(\[]", " < ", text)
    text = re.sub(r"[\}\)\]]", " > ", text)
    return text


def clean_tibetan_text(text: str) -> str:
    text = clean_text(text)
    text = re.sub(r"[ ]+", "", text).strip()
    return text


def clean_english_text(text: str) -> str:
    text = clean_text(text)
    text = re.sub(r"[ ]+", " ", text).strip()
    return text


def clean_text(text: str, is_tibetan=False) -> str:
    text = remove_number_emojis(text)
    text = normalise_punctuation(text)
    return text


if __name__ == "__main__":

    # Example usage:
    input_text = "This is a བཀྲ་ཤིས་sample བདེ་ལེགས་ text."
    filtered_text = clean_tibetan_text(input_text)
    print(filtered_text)
