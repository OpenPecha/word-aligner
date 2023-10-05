from word_aligner.word_list_tokenizer import tokenize_using_word_list


def test_tokenize_using_word_list():
    test_word_list = ["ཡོན་ཏན་", "མི་ཁྱབ"]
    text = "གནས་འདིའི་ཡོན་ཏན་བསམ་མི་ཁྱབ།།"
    tokenized_text = tokenize_using_word_list(text, test_word_list)
    expected_text = "གནས་ འདིའི་ ཡོན་ཏན་ བསམ་ མི་ཁྱབ ། །"
    assert tokenized_text == expected_text
