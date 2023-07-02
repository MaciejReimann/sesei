from typing import List, Callable, Tuple


def clean_text(
    pages: List[Tuple[int, str]], clearnin_functions: List[Callable[[str], str]]
) -> List[Tuple[int, str]]:
    cleaned_pages = []
    for page_num, text in pages:
        for cleaning_function in clearnin_functions:
            text = cleaning_function(text)
        cleaned_pages.append((page_num, text))
    return cleaned_pages
