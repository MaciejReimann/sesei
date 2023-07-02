from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def text_to_docs(text: List[str], metadata: Dict[str, str]) -> List[Document]:
    """Convert a list of strings to a list of Documents with metadata"""
    doc_chunks = []

    for page_num, page_text in text:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            separators=["\n\n", "\n", ".", "?", "!", ", ", "", " "],
            chunk_overlap=200,
        )
        chunks = text_splitter.split_text(page_text)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "page_num": page_num,
                    "chunk_num": i,
                    "source": f"p{page_num}-{i}",
                    **metadata,
                },
            )
            doc_chunks.append(doc)
    return doc_chunks
