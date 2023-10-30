# from pathlib import Path

# from word_aligner.alignment_accuracy_evaluator import (
#     count_word_matches,
#     read_json_to_dictionary,
# )
from word_aligner.mgiza_word_aligner import execute_mgiza, tokenize_and_merge_files


def pipeline(
    split_affix=True,
    tibetan_lemma=False,
    combine_tibetan_compound_words=False,
    english_lemma=False,
    combine_english_compound_words=False,
    num_files_to_train=1,
    threshold_frequency=1,
    is_source_file_english=True,
):
    """
    Tibetan tokenizer options
    i)split_affix=True  སྒྲོལ་མ་ -འི་
    ii)split_affix=False སྒྲོལ་མའི་
    iii)tibetan_lemma=True སྒྲོལ་མ་
    """

    tokenize_and_merge_files(
        split_affix=split_affix,
        tibetan_lemma=tibetan_lemma,
        combine_tibetan_compound_words=combine_tibetan_compound_words,
        english_lemma=english_lemma,
        combine_english_compound_words=combine_english_compound_words,
        num_files_to_train=num_files_to_train,
    )
    execute_mgiza(
        threshold_frequency=threshold_frequency,
        is_source_file_english=is_source_file_english,
    )
    # RESOURCES_FOLDER_DIR = Path(__file__).parent / "resources"
    # json_file_path = RESOURCES_FOLDER_DIR / "tibetan_english_dict.json"
    # dict = read_json_to_dictionary(json_file_path)
    # matches = count_word_matches(word_alignment_result, dict)
    # print(f"Total matches with tibetan english dictionary: {matches}")


if __name__ == "__main__":
    pipeline(
        split_affix=True,
        tibetan_lemma=False,
        combine_tibetan_compound_words=True,
        english_lemma=True,
        combine_english_compound_words=False,
        num_files_to_train=3,
        threshold_frequency=3,
        is_source_file_english=False,
    )
