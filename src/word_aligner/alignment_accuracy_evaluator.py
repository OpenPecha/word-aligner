from pathlib import Path

import openpyxl


def read_excel_tibetan_to_english(file_path):
    data = {}
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        for row in sheet.iter_rows(values_only=True):
            if len(row) >= 2:
                tibetan_word, english_word = row[0], row[1]
                data[tibetan_word] = english_word

        return data
    except Exception as e:
        print(f"File: {file_path} An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    CURRENT_DIR = Path(__file__).parent
    file_path = CURRENT_DIR / "resources/Illuminator.xlsx"
    tibetan_english_dict = read_excel_tibetan_to_english(file_path)
    for key, value in tibetan_english_dict.items():
        print(f"Tibetan: {key}, English: {value}")
