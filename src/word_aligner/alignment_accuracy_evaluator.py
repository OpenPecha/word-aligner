import json
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


def write_dictionary_to_json(dictionary, file_path):
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(dictionary, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Example usage:
    RESOURCES_FOLDER_DIR = Path(__file__).parent / "resources"
    file_path = RESOURCES_FOLDER_DIR / "Illuminator.xlsx"
    tibetan_english_dict = read_excel_tibetan_to_english(file_path)
    json_output_file_path = RESOURCES_FOLDER_DIR / "tibetan_english_dict.json"
    write_dictionary_to_json(tibetan_english_dict, json_output_file_path)
