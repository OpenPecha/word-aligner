from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
TOP_LEVEL_DIR = PARENT_DIR.parent
DATA_FOLDER_DIR = TOP_LEVEL_DIR / "data"
SUB_INPUT_1 = DATA_FOLDER_DIR / "input" / "sub_input_1"
RESOURCE_FOLDER_DIR = CURRENT_DIR / "resources"
LOG_FOLDER_DIR = CURRENT_DIR / "logs"
