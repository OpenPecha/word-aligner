import glob
import os
import string
import subprocess
from collections import Counter
from typing import Dict

from word_aligner.data_processor import clean_english_text, clean_tibetan_text
from word_aligner.tibetan_words_combiner import (
    load_tibetan_word_dictionary,
    merge_tibetan_compound_words,
)
from word_aligner.word_tokenizer import (
    load_botok_word_tokenizer,
    load_spacy_word_tokenizer,
    tokenize_english_with_named_entities,
    tokenize_english_with_spacy,
    tokenize_tibetan_with_botok,
)


def tokenize_and_merge_files(
    split_affix=True,
    tibetan_lemma=False,
    combine_tibetan_compound_words=False,
    english_lemma=False,
    combine_english_compound_words=False,
    num_files_to_train=1,
):
    # Paths
    data_dir = "data"
    input_dir = os.path.join(data_dir, "input")
    english_out_file = os.path.join(data_dir, "english.txt")
    tibetan_out_file = os.path.join(data_dir, "tibetan.txt")

    botok_tokenizer_obj = load_botok_word_tokenizer()
    spacy_tokenizer_obj = load_spacy_word_tokenizer()
    TIBETAN_WORD_DICTIONARY = load_tibetan_word_dictionary()

    # Updated merging code with tokenization and ensuring non-empty pairs
    with open(english_out_file, "w", encoding="utf-8") as english_out, open(
        tibetan_out_file, "w", encoding="utf-8"
    ) as tibetan_out:
        for subdir in os.listdir(input_dir):

            full_subdir_path = os.path.join(input_dir, subdir)
            if os.path.isdir(full_subdir_path):
                files_in_subdir = os.listdir(full_subdir_path)
                english_files = [f for f in files_in_subdir if f.endswith("-en.txt")]
                tibetan_files = [f for f in files_in_subdir if f.endswith("-bo.txt")]

                english_files = sorted(english_files)[:num_files_to_train]
                tibetan_files = sorted(tibetan_files)[:num_files_to_train]

                if len(english_files) != len(tibetan_files):
                    print(
                        f"Warning: Mismatch in number of files in {full_subdir_path}. Skipping this folder."
                    )
                    continue

                for english_file, tibetan_file in zip(
                    sorted(english_files), sorted(tibetan_files)
                ):
                    with open(
                        os.path.join(full_subdir_path, english_file), encoding="utf-8"
                    ) as eng, open(
                        os.path.join(full_subdir_path, tibetan_file), encoding="utf-8"
                    ) as bo:
                        en_lines = eng.readlines()
                        bo_lines = bo.readlines()

                        for en_line, bo_line in zip(en_lines, bo_lines):
                            if combine_english_compound_words:
                                en_line = tokenize_english_with_named_entities(
                                    spacy_tokenizer_obj,
                                    clean_english_text(en_line),
                                    english_lemma,
                                )
                            else:
                                en_line = tokenize_english_with_spacy(
                                    spacy_tokenizer_obj,
                                    clean_english_text(en_line),
                                    english_lemma,
                                )
                            bo_line = tokenize_tibetan_with_botok(
                                botok_tokenizer_obj,
                                clean_tibetan_text(bo_line),
                                split_affix,
                                tibetan_lemma,
                            )
                            if combine_tibetan_compound_words:
                                bo_line = merge_tibetan_compound_words(
                                    TIBETAN_WORD_DICTIONARY, bo_line
                                )

                            if en_line and bo_line:
                                english_out.write(en_line + "\n")
                                tibetan_out.write(bo_line + "\n")

    print(f"Data merged into {english_out_file} and {tibetan_out_file}.")


# Function to read vcb files and return a dictionary
def read_vcb(vcb_file):  # noqa
    vocabulary = {}
    with open(vcb_file, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            index = int(parts[0])
            word = parts[1]
            vocabulary[index] = word
    return vocabulary


def group_consecutive_indices(indices):
    """Group consecutive indices."""
    if not indices:
        return []

    groups = []
    current_group = [indices[0]]

    for i in range(1, len(indices)):
        if indices[i] == indices[i - 1] + 1:
            current_group.append(indices[i])
        else:
            groups.append(current_group)
            current_group = [indices[i]]
    groups.append(current_group)

    return groups


def execute_mgiza(threshold_frequency=1):

    # Set paths
    data_dir = "data"
    source_path = os.path.join(data_dir, "english")
    target_path = os.path.join(data_dir, "tibetan")
    out_file = os.path.join(data_dir, "aligned_words.txt")

    # Convert plain text data to the snt format expected by mgiza++
    subprocess.run(["plain2snt", source_path + ".txt", target_path + ".txt"])

    # Set paths for co-occurrence files
    cooc_file_source_target = os.path.join(data_dir, "source-target.cooc")
    cooc_file_target_source = os.path.join(data_dir, "target-source.cooc")

    # Generate co-occurrence files using snt2cooc
    subprocess.run(
        [
            "snt2cooc",
            cooc_file_source_target,
            source_path + ".vcb",
            target_path + ".vcb",
            source_path + "_" + target_path.split("/")[-1] + ".snt",
        ]
    )
    subprocess.run(
        [
            "snt2cooc",
            cooc_file_target_source,
            target_path + ".vcb",
            source_path + ".vcb",
            target_path + "_" + source_path.split("/")[-1] + ".snt",
        ]
    )

    # Run mgiza with co-occurrence files
    subprocess.run(
        [
            "mgiza",
            "-S",
            source_path + ".vcb",
            "-T",
            target_path + ".vcb",
            "-C",
            source_path + "_" + target_path.split("/")[-1] + ".snt",
            "-o",
            os.path.join(data_dir, "alignment"),
            "-CoocurrenceFile",
            cooc_file_source_target,
        ]
    )

    # Read vocabularies
    src_vocabulary = read_vcb(source_path + ".vcb")
    tgt_vocabulary = read_vcb(target_path + ".vcb")

    # Check that vocabularies are correctly read
    print(f"First 5 source vocab entries: {list(src_vocabulary.items())[:5]}")
    print(f"First 5 target vocab entries: {list(tgt_vocabulary.items())[:5]}")

    # Define the word_alignments dictionary
    word_alignments: Dict = {}  # noqa

    # Extract word alignments from the alignment files
    alignment_files = glob.glob(os.path.join(data_dir, "alignment.A3.final.part*"))
    print(f"Found {len(alignment_files)} alignment files.")

    # Loop over alignment files
    for alignment_file in alignment_files:
        print(f"Processing {alignment_file}")
        with open(alignment_file, encoding="utf-8") as af:
            lines = af.readlines()
            for i in range(1, len(lines), 3):
                source_tokens = lines[i].strip().split()

                # Extract the part of the line that contains the alignments
                alignment_info = lines[i + 1].strip().split("NULL")[1]

                # Split the line based on closing brace to get individual alignments
                alignments = alignment_info.split("}")
                for align in alignments:
                    if "{" not in align:
                        continue
                    target_word = align.split("{")[0].strip().strip(string.punctuation)
                    indices = [int(idx) for idx in align.split("{")[1].split()]

                    grouped_indices = group_consecutive_indices(indices)
                    grouped_source_words = [
                        "".join(source_tokens[idx - 1] for idx in group)
                        for group in grouped_indices
                    ]

                    if target_word not in word_alignments:
                        word_alignments[target_word] = []
                    word_alignments[target_word].extend(grouped_source_words)

        # Debug print to check how many alignments have been captured after processing each file
        print(
            f"Number of alignments captured after processing {alignment_file}: {len(word_alignments)}"
        )

    # Process word alignments to get unique strings with frequencies and order them
    filtered_word_alignments = {}
    for target_word, source_phrases in word_alignments.items():
        counter = Counter(source_phrases)

        # Filter phrases based on the threshold
        filtered_phrases = {
            phrase: count
            for phrase, count in counter.items()
            if count >= threshold_frequency
        }

        if not filtered_phrases:
            continue
        ordered_phrases = sorted(
            filtered_phrases.items(), key=lambda x: x[1], reverse=True
        )
        filtered_word_alignments[target_word] = [
            f"{phrase}_{count}" for phrase, count in ordered_phrases
        ]

    # Write results to output file
    print("Writing to aligned_words.txt...")
    with open(out_file, "w", encoding="utf-8") as out:
        for target_word in sorted(filtered_word_alignments.keys()):
            source_words = ", ".join(filtered_word_alignments[target_word])
            out.write(f"{target_word}: {source_words}\n")

    print("Writing complete.")
    print(f"Word alignments saved to {out_file}")


if __name__ == "__main__":
    tokenize_and_merge_files()
    execute_mgiza()
