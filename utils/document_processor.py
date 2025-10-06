import PyPDF2
import docx
from typing import List, Dict
import streamlit as st


class DocumentProcessor:
    """Classe pour traiter les documents PDF et DOCX"""

    @staticmethod
    def extract_text_from_pdf(file) -> str:
        """Extraire le texte d'un fichier PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Erreur lors de l'extraction du PDF : {e}")
            return ""

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
    def process_document(file) -> Dict[str, any]:
        """Traiter un document et retourner les informations"""
        file_type = file.name.split(".")[-1].lower()

        if file_type == "pdf":
            text = DocumentProcessor.extract_text_from_pdf(file)
        elif file_type in ["docx", "doc"]:
            text = DocumentProcessor.extract_text_from_docx(file)
        else:
            st.error("Format de fichier non supporté")
            return None

        return {
            "name": file.name,
            "type": file_type,
            "text": text,
            "word_count": len(text.split()),
            "char_count": len(text),
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
