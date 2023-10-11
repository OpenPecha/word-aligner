from word_aligner.tibetan_words_combiner import (
    load_tibetan_word_dictionary,
    merge_tibetan_compound_words,
)


def test_combine_compound_words_MONLAM2020():
    TIBETAN_WORD_DICT = load_tibetan_word_dictionary()
    test_sentence = "ང་ ས་ ཆེན་ ཀུན་དགའ་ བློ་གྲོས་ ཡིན་"
    combined_words_sentence = merge_tibetan_compound_words(
        TIBETAN_WORD_DICT, test_sentence
    )
    expected_sentence = "ང་ ས་+ཆེན་+ཀུན་དགའ་+བློ་གྲོས་ ཡིན་"

    assert combined_words_sentence == expected_sentence
