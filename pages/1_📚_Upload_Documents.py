import streamlit as st
from utils.document_processor import DocumentProcessor
from utils.ai_generator import AIGenerator
from config import Config
import time

st.set_page_config(page_title="Upload Documents", page_icon="📚", layout="wide")


def main():
    st.title("📚 Upload et Analyse de Documents")

    # Vérifier le profil
    if not st.session_state.get("profile"):
        st.warning("⚠️ Veuillez d'abord sélectionner votre profil sur la page d'accueil")
        if st.button("← Retour à l'accueil"):
            st.switch_page("app.py")
        return

    st.markdown(
        f"**Profil:** {st.session_state.profile} | "
        f"**Discipline:** {st.session_state.discipline} | "
        f"**Niveau:** {st.session_state.niveau}"
    )

    st.divider()

    # Upload de fichiers
    st.markdown("### 📤 Uploadez vos documents")

    uploaded_files = st.file_uploader(
        "Formats acceptés : PDF, DOCX",
        type=["pdf", "docx", "doc"],
        accept_multiple_files=True,
        help=f"Taille maximale : {Config.MAX_FILE_SIZE} MB par fichier",
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} fichier(s) uploadé(s)")

        col1, col2 = st.columns([3, 1])

        with col2:
            if st.button(
                "🔄 Analyser tous les documents",
                type="primary",
                use_container_width=True,
            ):
                process_documents(uploaded_files)

        st.divider()

        # Afficher les documents uploadés
        st.markdown("### 📄 Documents uploadés")

        for idx, file in enumerate(uploaded_files):
            with st.expander(f"📄 {file.name}"):
                col1, col2, col3 = st.columns(3)

                file_info = DocumentProcessor.process_document(file)

                if file_info:
                    col1.metric("Type", file_info["type"].upper())
                    col2.metric("Mots", f"{file_info['word_count']:,}")
                    col3.metric("Caractères", f"{file_info['char_count']:,}")

                    # Aperçu du texte
                    st.text_area(
                        "Aperçu du contenu",
                        file_info["text"][:500] + "...",
                        height=150,
                        key=f"preview_{idx}",
                    )

    # Afficher les documents déjà traités
    if st.session_state.documents:
        st.divider()
        st.markdown("### 📚 Bibliothèque de documents")

        for idx, doc in enumerate(st.session_state.documents):
            with st.expander(f"📖 {doc['name']}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    if "summary" in doc:
                        st.markdown("#### 📝 Résumé")
                        st.write(doc["summary"].get("resume_general", ""))

                        if doc["summary"].get("concepts_cles"):
                            st.markdown("**🎯 Concepts clés:**")
                            for concept in doc["summary"]["concepts_cles"]:
                                st.markdown(f"- {concept}")

                with col2:
                    if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                        st.session_state.documents.pop(idx)
                        st.rerun()


def process_documents(files):
    """Traiter et analyser les documents uploadés"""
    ai_gen = AIGenerator()
    processor = DocumentProcessor()

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, file in enumerate(files):
        status_text.text(f"Traitement de {file.name}...")

        # Extraire le texte
        doc_info = processor.process_document(file)

        if doc_info:
            # Générer le résumé avec AI
            status_text.text(f"Génération du résumé pour {file.name}...")
            summary = ai_gen.generate_summary(
                doc_info["text"], st.session_state.discipline, st.session_state.niveau
            )

            doc_info["summary"] = summary

            # Ajouter à la session
            st.session_state.documents.append(doc_info)

        progress_bar.progress((idx + 1) / len(files))

    status_text.text("✅ Tous les documents ont été traités!")
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()
    st.rerun()


if __name__ == "__main__":
    main()
