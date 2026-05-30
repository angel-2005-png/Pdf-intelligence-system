from pypdf import PdfReader


def load_document(file_path):
    reader = PdfReader(file_path)

    text = " "

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text



