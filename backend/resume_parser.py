import pdfplumber
import docx


def extract_text(file_path):
    text = ""

    try:
        # 📄 Handle PDF files
        if file_path.lower().endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        # 📄 Handle DOCX files
        elif file_path.lower().endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        else:
            return ""

    except Exception as e:
        print("Error extracting text:", e)
        return ""

    return text.strip()