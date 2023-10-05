import re
from pathlib import Path
from typing import List

from .config import RESOURCE_FOLDER_DIR, SUB_INPUT_1

BO_EN_FILE_PATH = Path(RESOURCE_FOLDER_DIR / "bo_en_list.txt")


def count_files_in_folder(folder_path: Path) -> int:
    return len([item for item in folder_path.iterdir() if item.is_file()])


def compare_number_of_bo_en_files_in_subdir(subdir_path: Path) -> bool:
    bo_files = [
        item
        for item in subdir_path.iterdir()
        if item.is_file() and item.name.endswith("-bo.txt")
    ]
    en_files = [
        item
        for item in subdir_path.iterdir()
        if item.is_file() and item.name.endswith("-en.txt")
    ]
    print(f"Number of bo files: {len(bo_files)}")
    print(f"Number of en files: {len(en_files)}")
    return len(bo_files) == len(en_files)


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


if __name__ == "__main__":
    # extract_tm_names_using_regex()
    print(count_files_in_folder(SUB_INPUT_1))
    print(compare_number_of_bo_en_files_in_subdir(SUB_INPUT_1))
