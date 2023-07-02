from dotenv import load_dotenv
from utils.parse_pdf import parse_pdf
from utils.clean_text import clean_text
from utils.text_to_docs import text_to_docs
from utils.cleaning_functions import (
    merge_hyphenated_words,
    fix_newlines,
    remove_multiple_newlines,
)
from langchain.embeddings.openai import OpenAIEmbeddings

if __name__ == "__main__":
    load_dotenv()

    # 1.Parse PDF
    file_path = ""  # TODO: add file path
    raw_pages, metadata = parse_pdf(file_path)
    print(metadata)

    # 2.Create text chunks
    cleaning_functions = [
        merge_hyphenated_words,
        fix_newlines,
        remove_multiple_newlines,
    ]
    cleaned_text_pdf = clean_text(raw_pages, cleaning_functions)
    document_chunks = text_to_docs(cleaned_text_pdf, metadata)

    document_chunks = document_chunks[:70]

    print(document_chunks)

    # 3. Create embeddings
    embeddings = OpenAIEmbeddings()

    # 4. Store them in a database sbp_bc1ef68c5eec72347dcae0109bc64333f429e6a2
