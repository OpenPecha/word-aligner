import re
from pathlib import Path

import openpyxl


def extract_text_in_double_quotes(sentence):
    # Use regular expressions to find text in single quotes
    text_in_single_quotes = re.findall(r'"(.*?)"', sentence)
    return text_in_single_quotes


def read_excel_tibetan_to_english(file_path):
    data = {}
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    for row in sheet.iter_rows(values_only=True):
        tibetan_word, word_description = row[0], row[1]
        if not tibetan_word or not word_description:
            continue
        english_words = extract_text_in_double_quotes(word_description)
        if english_words:
            data[tibetan_word] = english_words

    return data


if __name__ == "__main__":
    # Example usage:
    CURRENT_DIR = Path(__file__).parent
    file_path = CURRENT_DIR / "resources/Illuminator.xlsx"
    tibetan_english_dict = read_excel_tibetan_to_english(file_path)
    for key, value in tibetan_english_dict.items():
        print(f"Tibetan: {key}, English: {value}")
