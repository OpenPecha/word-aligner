from word_aligner.mgiza_word_aligner import execute_mgiza, tokenize_and_merge_files


def pipeline(
    split_affix=True,
    tibetan_lemma=False,
    combine_tibetan_compound_words=False,
    english_lemma=False,
    combine_english_compound_words=False,
    num_files_to_train=1,
    threshold_frequency=1,
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
    execute_mgiza(threshold_frequency=threshold_frequency)


if __name__ == "__main__":
    pipeline(
        split_affix=True,
        tibetan_lemma=False,
        combine_tibetan_compound_words=False,
        english_lemma=True,
        combine_english_compound_words=True,
        num_files_to_train=1,
        threshold_frequency=3,
    )
