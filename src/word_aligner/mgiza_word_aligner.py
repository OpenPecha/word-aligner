import glob
import os
import re
import string
import subprocess
from collections import Counter
from typing import Dict

from botok import WordTokenizer

# botok
tok = WordTokenizer()

# Paths
data_dir = "data"
input_dir = os.path.join(data_dir, "input")
source_out_file = os.path.join(data_dir, "source.txt")
target_out_file = os.path.join(data_dir, "target.txt")
out_file = os.path.join(data_dir, "aligned_words.txt")


def syllable_tokenizer(text, lemmatize=False):
    tsek = "་"
    tokens = tok.tokenize(text)
    out = []
    for t in tokens:
        if t.chunk_type == "TEXT":
            if lemmatize:
                tt = tok.tokenize(t.lemma)
                syls = [["".join(s) for s in t.syls] for t in tt]
                for s in syls:
                    out.extend(s)
            else:
                syls = t.syls
                joined = ["".join(s) + tsek for s in syls]
                out.extend(joined)
        else:
            out.append(t.text)
    text = " ".join(out)
    return text


# 1. Inserting the regex tokenizers and clean-up functions
# def syllable_tokenizer(text):
#    text = re.sub(r'([ཀགཤ༔།])$', r'\1 ', text)
#    text = re.sub(r'།([^། ])', r'། \1', text)
#    text = re.sub(r'([ཀགཤ]) །', r'\1་ ། ', text)
#    text = text.replace('། །', '་ །། ')
#    text = text.replace('༔ ', '་ ༔ ')
#    text = re.sub(r'་+', '་', text)
#    text = text.replace('་', '་ ')
#    return text


def word_tokenizer(text):
    text = re.sub(r'([a-zA-Z])([!?,.":;])', r"\1 \2", text)
    text = re.sub(r'([!?,.":;])([a-zA-Z])', r"\1 \2", text)
    return text


def clean_text(text, is_tibetan=False):
    text = re.sub(r"[\{\(]", " < ", text)
    text = re.sub(r"[\}\)]", " > ", text)
    if not is_tibetan:
        text = re.sub(r"[^\x00-\x7F]+", "", text).strip()  # Only for English
    text = re.sub(r" +", " ", text).strip()
    return text


# Updated merging code with tokenization and ensuring non-empty pairs
with open(source_out_file, "w", encoding="utf-8") as source_out, open(
    target_out_file, "w", encoding="utf-8"
) as target_out:
    for subdir in os.listdir(input_dir):
        full_subdir_path = os.path.join(input_dir, subdir)
        if os.path.isdir(full_subdir_path):
            files_in_subdir = os.listdir(full_subdir_path)
            source_files = [f for f in files_in_subdir if f.endswith("-en.txt")]
            target_files = [f for f in files_in_subdir if f.endswith("-bo.txt")]

            if len(source_files) != len(target_files):
                print(
                    f"Warning: Mismatch in number of files in {full_subdir_path}. Skipping this folder."
                )
                continue

            for src_file, tgt_file in zip(sorted(source_files), sorted(target_files)):
                with open(
                    os.path.join(full_subdir_path, src_file), encoding="utf-8"
                ) as src, open(
                    os.path.join(full_subdir_path, tgt_file), encoding="utf-8"
                ) as tgt:
                    src_lines = src.readlines()
                    tgt_lines = tgt.readlines()

                    for src_line, tgt_line in zip(src_lines, tgt_lines):
                        src_line = word_tokenizer(clean_text(src_line))
                        tgt_line = syllable_tokenizer(
                            clean_text(tgt_line, is_tibetan=True)
                        )

                        if src_line and tgt_line:
                            source_out.write(src_line + "\n")
                            target_out.write(tgt_line + "\n")

print(f"Data merged into {source_out_file} and {target_out_file}.")


# Set paths
data_dir = "data"
source_path = os.path.join(data_dir, "source")
target_path = os.path.join(data_dir, "target")
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
for target_word, source_phrases in word_alignments.items():
    counter = Counter(source_phrases)
    ordered_phrases = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    word_alignments[target_word] = [
        f"{phrase}_{count}" for phrase, count in ordered_phrases
    ]

# Write results to output file
print("Writing to aligned_words.txt...")
with open(out_file, "w", encoding="utf-8") as out:
    for target_word in sorted(word_alignments.keys()):
        source_words = ", ".join(word_alignments[target_word])
        out.write(f"{target_word}: {source_words}\n")

print("Writing complete.")
print(f"Word alignments saved to {out_file}")
