import PyPDF2
import docx
from typing import List, Dict, Optional, Any
import streamlit as st


class DocumentProcessor:
    """Classe pour traiter les documents PDF et DOCX"""

    @staticmethod
    def extract_text_from_pdf(file) -> tuple[str, int]:
        """Extraire le texte d'un fichier PDF et retourner (texte, nombre_pages)"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            page_count = len(pdf_reader.pages)
            return text, page_count
        except Exception as e:
            st.error(f"Erreur lors de l'extraction du PDF : {e}")
            return "", 0

    @staticmethod
    def extract_text_from_docx(file) -> str:
        """Extraire le texte d'un fichier DOCX"""
        try:
            doc = docx.Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            st.error(f"Erreur lors de l'extraction du DOCX : {e}")
            return ""

    @staticmethod
    def process_document(file) -> Optional[Dict[str, Any]]:
        """Traiter un document et retourner les informations"""
        file_type = file.name.split(".")[-1].lower()
        page_count = 0

        if file_type == "pdf":
            text, page_count = DocumentProcessor.extract_text_from_pdf(file)
        elif file_type in ["docx", "doc"]:
            text = DocumentProcessor.extract_text_from_docx(file)
            # For DOCX, estimate pages (average 300 words per page)
            page_count = max(1, len(text.split()) // 300)
        else:
            st.error("Format de fichier non supporté")
            return None

        return {
            "name": file.name,
            "type": file_type,
            "text": text,
            "word_count": len(text.split()),
            "char_count": len(text),
            "page_count": page_count,
        }

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Diviser le texte en chunks pour le traitement AI"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            chunks.append(chunk)

        return chunks
