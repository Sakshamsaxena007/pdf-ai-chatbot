from pypdf import PdfReader

def load_pdf(file_path):
    reader = PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append({
                "page": i + 1,
                "text": text
            })
    return pages

# What this does simply to help understand the assessment :-
# This file just reads the PDF and pulls out text from every page. 
