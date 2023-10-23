from antx import transfer


def newline_annotations_transfer(source_text, target_text):
    annotations = [
        ["new_line", r"(\n)"],
    ]
    target_text = remove_newlines(target_text)
    target_text += " "
    annotated_text = transfer(source_text, annotations, target_text, output="txt")
    return annotated_text


def remove_newlines(text: str) -> str:
    return text.replace("\n", " ")
