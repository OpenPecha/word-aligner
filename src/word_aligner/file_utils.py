import re
from pathlib import Path
from typing import List

from word_aligner.config import DATA_FOLDER_DIR, RESOURCE_FOLDER_DIR

BO_EN_FILE_PATH = Path(RESOURCE_FOLDER_DIR / "bo_en_list.txt")


def count_files_in_folder(folder_path: Path) -> int:
    return len([item for item in folder_path.iterdir() if item.is_file()])


def get_bo_en_file_pairs(folder_path: Path):
    en_files = list(folder_path.glob("*-en.txt"))
    bo_files = list(folder_path.glob("*-bo.txt"))
    return bo_files, en_files


def merge_bo_en_files(folder_path: Path, output_folder_path: Path):
    # merge all bo files into one, and all en files into one
    bo_files, en_files = get_bo_en_file_pairs(folder_path)
    if len(bo_files) == len(en_files):
        bo_merged_file = Path(output_folder_path / "bo_merged.txt")
        en_merged_file = Path(output_folder_path / "en_merged.txt")

        with open(bo_merged_file, "a", encoding="utf-8") as bo_output_file, open(
            en_merged_file, "a", encoding="utf-8"
        ) as en_output_file:
            for bo_file, en_file in zip(sorted(bo_files), sorted(en_files)):
                bo_file_lines = bo_file.read_text(encoding="utf-8").splitlines()
                en_file_lines = en_file.read_text(encoding="utf-8").splitlines()
                if len(bo_file_lines) == len(en_file_lines):
                    bo_output_file.write("\n".join(bo_file_lines) + "\n")
                    en_output_file.write("\n".join(en_file_lines) + "\n")


def filter_bo_repo_names_from_file(file_content: str) -> List[str]:
    # Regex to extract the bo repo names from file
    BO_PATTERN = r"-\s([a-zA-Z\d_-]*)"
    bo_names = re.findall(BO_PATTERN, file_content)
    return bo_names


def get_tm_repo_names_from_bo_names(bo_names: List[str]) -> List[str]:
    # input: BO0791 Output:TM0791
    bo_ids = [bo_name[2:] for bo_name in bo_names]
    tm_names = [f"TM{bo_id}" for bo_id in bo_ids]
    return tm_names


def extract_tm_names_using_regex(file_path: Path = BO_EN_FILE_PATH):
    # the source for the file is described in README.md in resource folder
    bo_en_file_content = file_path.read_text(encoding="utf-8")
    bo_names = filter_bo_repo_names_from_file(bo_en_file_content)
    tm_names = get_tm_repo_names_from_bo_names(bo_names)
    tm_list_file_path = Path(RESOURCE_FOLDER_DIR / "tm_list.txt")
    tm_list_file_path.write_text("\n".join(tm_names), encoding="utf-8")


def count_lines(file_path: Path):
    return len(file_path.read_text(encoding="utf-8").splitlines())


def copy_bo_en_file_pairs(source_folder: Path, destination_folder: Path, count: int):
    bo_files, en_files = get_bo_en_file_pairs(source_folder)
    counter = 0
    for bo_file, en_file in zip(sorted(bo_files), sorted(en_files)):
        if counter >= count:
            break
        if count_lines(bo_file) != count_lines(en_file):
            continue
        bo_file_destination = destination_folder / bo_file.name
        en_file_destination = destination_folder / en_file.name
        bo_file_destination.write_text(
            bo_file.read_text(encoding="utf-8"), encoding="utf-8"
        )
        en_file_destination.write_text(
            en_file.read_text(encoding="utf-8"), encoding="utf-8"
        )
        counter += 2


def filter_unique_characters_in_file(file_path):
    with open(file_path) as file:
        content = file.read()
    from word_aligner.data_processor import keep_only_english_characters

    content = keep_only_english_characters(content)
    # Use a set to store unique characters
    unique_characters = set(content)

    # Convert the set of unique characters back to a string
    # unique_characters_str = ''.join(unique_characters)

    return unique_characters


if __name__ == "__main__":
    file_path = DATA_FOLDER_DIR / "en_merged.txt"
    unique_characters_str = filter_unique_characters_in_file(file_path)
    print(unique_characters_str)
