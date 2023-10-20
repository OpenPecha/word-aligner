from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
TOP_LEVEL_DIR = PARENT_DIR.parent
DATA_FOLDER_DIR = TOP_LEVEL_DIR / "data"
TMs_4006 = DATA_FOLDER_DIR / "input" / "TMs_4006"
RESOURCE_FOLDER_DIR = CURRENT_DIR / "resources"
LOG_FOLDER_DIR = CURRENT_DIR / "logs"

OPENING_PUNCTS = [
    "༁",
    "༂",
    "༃",
    "༄",
    "༅",
    "༆",
    "༇",
    "༈",
    "༉",
    "༊",
    "༑",
    "༒",
    "༺",
    "༼",
    "༿",
    "࿐",
    "࿑",
    "࿓",
    "࿔",
    "࿙",
]
CLOSING_PUNCTS = ["།", "༎", "༏", "༐", "༔", "༴", "༻", "༽", "༾", "࿚"]
CLOSING_PUNCTS_CHAR_SET = "[།༎༏༐༔༴༻༽༾࿚]"
PUNCTS = OPENING_PUNCTS + CLOSING_PUNCTS
