import json
import re
from pathlib import Path

import openpyxl
from ordered_set import OrderedSet


def extract_text_in_double_quotes(sentence):
    # Use regular expressions to find text in single quotes
    text_in_single_quotes = re.findall(r'"(.*?)"', sentence)
    return text_in_single_quotes


def read_excel_and_extract_tibetan_english_pair(file_path):
    data = {}
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    for row in sheet.iter_rows(values_only=True):
        tibetan_word, word_description = row[0], row[1]
        if not tibetan_word or not word_description:
            continue
        english_words = extract_text_in_double_quotes(word_description)
        english_words = list(OrderedSet(english_words))
        if english_words:
            data[tibetan_word] = english_words
    return data


def write_dictionary_to_json(dictionary, file_path):
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(dictionary, fp, indent=4, ensure_ascii=False)


def read_json_to_dictionary(file_path):
    with open(file_path, encoding="utf-8") as fp:
        dictionary = json.load(fp)
    return dictionary


def count_word_matches(word_alignment, tibetan_english_dict):
    total_matches = 0
    for tibetan_word, alignment_english_words in word_alignment.items():
        if tibetan_word in tibetan_english_dict:
            for alignment_english_word in alignment_english_words:
                alignment_english_word = alignment_english_word.replace(
                    "*", " "
                ).replace("+", " ")
                for dictionary_english_word in tibetan_english_dict[tibetan_word]:
                    if alignment_english_word in dictionary_english_word:
                        total_matches += 1
                        break
    return total_matches


if __name__ == "__main__":
    # Example usage:
    RESOURCES_FOLDER_DIR = Path(__file__).parent / "resources"
    json_file_path = RESOURCES_FOLDER_DIR / "tibetan_english_dict.json"
    dict = read_json_to_dictionary(json_file_path)
    print(dict)
