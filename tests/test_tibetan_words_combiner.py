from word_aligner.tibetan_words_combiner import (
    combine_compound_words_MONLAM2020,
    load_MONLAM_2020_word_dict,
)


def test_combine_compound_words_MONLAM2020():
    MONLAM_2020 = load_MONLAM_2020_word_dict()
    test_sentence = "ང་ ས་ ཆེན་ ཀུན་དགའ་ བློ་གྲོས་ ཡིན་"
    combined_words_sentence = combine_compound_words_MONLAM2020(
        MONLAM_2020, test_sentence
    )
    expected_sentence = "ང་ ས་+ཆེན་+ཀུན་དགའ་+བློ་གྲོས་ ཡིན་"

    assert combined_words_sentence == expected_sentence
