from pathlib import Path
from typing import Iterable, Any, List, Tuple

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine, LTChar

def find_text_coordinates(pdf_path: Path, search_texts: List[str]) -> List[Tuple[str, List[Tuple[float, float, float, float, int]]]]:
    """
    Find the coordinates of given text in a PDF.

    Args:
        pdf_path (Path): Path to the PDF file.
        search_texts (List[str]): List of text strings to search for.

    Returns:
        List[Tuple[str, List[Tuple[float, float, float, float, int]]]]: 
            List of tuples containing the search text and a list of its occurrences.
            Each occurrence is represented by (x1, y1, x2, y2, page_number).
    """
    results = [(text, []) for text in search_texts]
    
    pages = extract_pages(pdf_path)
    for page_num, page in enumerate(pages):
        find_text_in_object(page, results, page_num)
    
    return results

def find_text_in_object(obj: Any, results: List[Tuple[str, List[Tuple[float, float, float, float, int]]]], page_num: int):
    """Recursively search for text in PDF objects."""
    if isinstance(obj, LTTextBox) or isinstance(obj, LTTextLine):
        text = obj.get_text().strip()
        for search_text, coords_list in results:
            if search_text in text:
                coords_list.append((*obj.bbox, page_num))
    
    if isinstance(obj, Iterable):
        for child in obj:
            find_text_in_object(child, results, page_num)

# Example usage
if __name__ == "__main__":
    pdf_path = Path('/Users/rasdani/git/ellamind/Printable-PDF-Annotations/die-wichtigsten-steuern-im-internationalen-vergleich-2022.pdf').expanduser()
    search_texts = ["Steuer"]
    
    results = find_text_coordinates(pdf_path, search_texts)
    
    for text, coords in results:
        print(f"Text: '{text}'")
        for x1, y1, x2, y2, page in coords:
            print(f"  Found on page {page+1} at coordinates: ({x1:.2f}, {y1:.2f}) to ({x2:.2f}, {y2:.2f})")
        print()