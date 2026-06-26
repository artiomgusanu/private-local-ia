import fitz
from pathlib import Path # trabalha com caminhos de ficheiros

def load_document(file_path: str) -> str:
    """Carrega PDF, TXT ou DOCX e retorna texto"""
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == '.pdf':
        doc = fitz.open(file_path)
        return "\n".join(page.get_text() for page in doc)
    
    elif suffix == '.txt':
        return path.read_text(encoding='utf-8')
    
    elif suffix == '.docx':
        from docx import Document
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    
    raise ValueError(f'Formato não suportado: {suffix}. Suportados: .pdf, .txt, .docx')
