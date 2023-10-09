from word_aligner.mgiza_word_aligner import execute_mgiza, tokenize_and_merge_files


def pipeline(
    split_affix=True,
    tibetan_lemma=False,
    combine_tibetan_compound_words=False,
    english_lemma=False,
    combine_english_compound_words=False,
):
    """
    Tibetan tokenizer options
    i)split_affix=True  སྒྲོལ་མ་ -འི་
    ii)split_affix=False སྒྲོལ་མའི་
    iii)tibetan_lemma=True སྒྲོལ་མ་
    """

    tokenize_and_merge_files(
        split_affix=True,
        tibetan_lemma=False,
        combine_tibetan_compound_words=False,
        english_lemma=False,
        combine_english_compound_words=False,
    )
    execute_mgiza()


if __name__ == "__main__":
    pipeline(
        split_affix=True,
        tibetan_lemma=False,
        combine_tibetan_compound_words=False,
        english_lemma=False,
        combine_english_compound_words=False,
    )
