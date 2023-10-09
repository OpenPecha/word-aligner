from word_aligner.word_list_tokenizer import (
    group_words_by_first_character,
    tokenize_tibetan_word_list,
)


def test_tokenize_tibetan_text_word_list():
    test_word_list = ["ཡོན་ཏན་", "མི་ཁྱབ"]
    test_word_dict = group_words_by_first_character(test_word_list)
    text = "གནས་འདིའི་ཡོན་ཏན་བསམ་མི་ཁྱབ།།"
    tokenized_text = tokenize_tibetan_word_list(text, test_word_dict)
    expected_text = "གནས་ འདིའི་ ཡོན་ཏན་ བསམ་ མི་ཁྱབ ། །"

    assert tokenized_text == expected_text


if __name__ == "__main__":
    test_tokenize_tibetan_text_word_list()
