from pathlib import Path
from typing import List, Tuple
import fitz  # PyMuPDF
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine

def find_text_coordinates(pdf_path: Path, search_texts: List[str]) -> List[Tuple[str, List[Tuple[float, float, float, float, int]]]]:
    results = [(text, []) for text in search_texts]
    
    pages = extract_pages(pdf_path)
    for page_num, page in enumerate(pages):
        find_text_in_object(page, results, page_num)
    
    return results

def find_text_in_object(obj, results, page_num):
    if isinstance(obj, (LTTextBox, LTTextLine)):
        text = obj.get_text().strip()
        for search_text, coords_list in results:
            if search_text in text:
                coords_list.append((*obj.bbox, page_num))
    
    if hasattr(obj, '__iter__'):
        for child in obj:
            find_text_in_object(child, results, page_num)

def annotate_pdf(pdf_path: Path, search_texts: List[str], output_path: Path = None):
    if output_path is None:
        output_path = pdf_path.with_suffix('.annotated.pdf')

    # Find coordinates of text
    text_coordinates = find_text_coordinates(pdf_path, search_texts)

    # Open the PDF with PyMuPDF
    doc = fitz.open(pdf_path)

    for text, coords in text_coordinates:
        for x1, y1, x2, y2, page_num in coords:
            page = doc[page_num]
            
            # Convert coordinates (PDF coordinates start from bottom-left)
            height = page.rect.height
            rect = fitz.Rect(x1, height - y2, x2, height - y1)
            
            # Add highlight annotation
            highlight = page.add_highlight_annot(rect)
            
            # Add text annotation (comment)
            text_annot = page.add_text_annot(rect.tl, text)
            
            # Set properties for better visibility
            text_annot.set_info(title="Comment", content=f"Highlighted text: {text}")
            text_annot.set_colors({"stroke": (1, 0, 0)})  # Red border
            text_annot.set_popup(rect.tl + (20, 20))
            text_annot.update()

    # Save the annotated PDF
    doc.save(output_path)
    doc.close()

    print(f"Annotated PDF saved as: {output_path}")

# Example usage
if __name__ == "__main__":
    pdf_path = Path('/Users/rasdani/git/ellamind/Printable-PDF-Annotations/die-wichtigsten-steuern-im-internationalen-vergleich-2022.pdf').expanduser()
    search_texts = ["Steuer"]
    
    annotate_pdf(pdf_path, search_texts)
