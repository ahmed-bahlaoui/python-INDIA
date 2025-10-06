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

    # Afficher les documents déjà traités avec résumés intelligents
    if st.session_state.documents:
        st.divider()
        st.markdown("### 📚 Bibliothèque de documents")

        for idx, doc in enumerate(st.session_state.documents):
            with st.expander(f"📖 {doc['name']}", expanded=False):
                
                if "summary" in doc and doc["summary"]:
                    summary = doc["summary"]
                    
                    # Bouton de suppression en haut
                    col_del1, col_del2 = st.columns([5, 1])
                    with col_del2:
                        if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                            st.session_state.documents.pop(idx)
                            st.rerun()
                    
                    # Tabs pour organiser l'information
                    tabs = st.tabs([
                        "📊 Analyse",
                        "📝 Résumé",
                        "🗺️ Mind Map",
                        "📅 Timeline",
                        "📖 Glossaire",
                        "🎴 Flashcards"
                    ])
                    
                    # Tab 1: Analyse de document
                    with tabs[0]:
                        if "analyse" in summary:
                            analyse = summary["analyse"]
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Type de document", analyse.get("type_document", "N/A"))
                            with col2:
                                st.metric("Niveau de difficulté", analyse.get("niveau_difficulte", "N/A"))
                            with col3:
                                st.metric("Temps de lecture", f"{analyse.get('temps_lecture_min', 0)} min")
                            
                            st.divider()
                            
                            # Statistiques
                            if "statistiques" in analyse:
                                stats = analyse["statistiques"]
                                st.markdown("#### 📊 Statistiques")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Pages estimées", stats.get("nb_pages_estime", 0))
                                with col2:
                                    st.metric("Nombre de mots", f"{stats.get('nb_mots', 0):,}")
                                with col3:
                                    st.metric("Concepts uniques", stats.get("nb_concepts_uniques", 0))
                            
                            # Mots-clés principaux
                            if analyse.get("mots_cles"):
                                st.markdown("#### 🔑 Mots-clés principaux")
                                keywords_html = " ".join([
                                    f'<span style="background-color: #1f77b4; color: white; padding: 5px 10px; border-radius: 15px; margin: 3px; display: inline-block;">{kw}</span>'
                                    for kw in analyse["mots_cles"][:10]
                                ])
                                st.markdown(keywords_html, unsafe_allow_html=True)
                            
                            # Concepts connexes suggérés
                            if analyse.get("concepts_connexes"):
                                st.markdown("#### 🔗 Concepts connexes suggérés")
                                for concept in analyse["concepts_connexes"][:5]:
                                    st.markdown(f"- {concept}")
                    
                    # Tab 2: Résumé par section
                    with tabs[1]:
                        st.markdown("#### 📝 Résumé général")
                        st.write(summary.get("resume_general", "Résumé non disponible"))
                        
                        if summary.get("sections"):
                            st.divider()
                            st.markdown("#### 📑 Résumé par section")
                            for section in summary["sections"]:
                                with st.container():
                                    st.markdown(f"**{section.get('titre', 'Section')}**")
                                    st.write(section.get('contenu', ''))
                                    st.divider()
                        
                        # Concepts clés
                        if summary.get("concepts_cles"):
                            st.markdown("#### 🎯 Concepts clés à retenir")
                            cols = st.columns(2)
                            for i, concept in enumerate(summary["concepts_cles"]):
                                with cols[i % 2]:
                                    st.info(f"✓ {concept}")
                    
                    # Tab 3: Mind Map Visuel
                    with tabs[2]:
                        if "mindmap" in summary:
                            mindmap = summary["mindmap"]
                            st.markdown("#### 🗺️ Diagramme des concepts principaux")
                            
                            if mindmap.get("concepts_principaux"):
                                st.markdown("**Concepts principaux:**")
                                cols = st.columns(min(3, len(mindmap["concepts_principaux"])))
                                for i, concept in enumerate(mindmap["concepts_principaux"]):
                                    with cols[i % 3]:
                                        st.markdown(
                                            f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                                            f'padding: 15px; border-radius: 10px; text-align: center; color: white; '
                                            f'margin: 5px;">{concept}</div>',
                                            unsafe_allow_html=True
                                        )
                            
                            if mindmap.get("relations"):
                                st.divider()
                                st.markdown("**Relations entre concepts:**")
                                for rel in mindmap["relations"]:
                                    st.markdown(
                                        f"- **{rel.get('de', '')}** {rel.get('type', '→')} **{rel.get('vers', '')}**"
                                    )
                        else:
                            st.info("Mind map non disponible pour ce document")
                    
                    # Tab 4: Timeline
                    with tabs[3]:
                        if summary.get("timeline"):
                            st.markdown("#### 📅 Timeline chronologique")
                            for event in summary["timeline"]:
                                importance_color = {
                                    "haute": "🔴",
                                    "moyenne": "🟡",
                                    "basse": "🟢"
                                }.get(event.get("importance", "moyenne").lower(), "⚪")
                                
                                st.markdown(
                                    f"**{importance_color} {event.get('date', 'Date inconnue')}** - "
                                    f"{event.get('evenement', '')}"
                                )
                        else:
                            st.info("Aucune timeline disponible (document non chronologique)")
                    
                    # Tab 5: Glossaire automatique
                    with tabs[4]:
                        if summary.get("glossaire"):
                            st.markdown("#### 📖 Glossaire des termes techniques")
                            for terme_obj in summary["glossaire"]:
                                with st.container():
                                    st.markdown(f"**{terme_obj.get('terme', '')}**")
                                    st.write(terme_obj.get('definition', ''))
                                    if terme_obj.get('exemple'):
                                        st.caption(f"*Exemple: {terme_obj['exemple']}*")
                                    st.divider()
                        else:
                            st.info("Glossaire non disponible")
                    
                    # Tab 6: Flashcards
                    with tabs[5]:
                        if summary.get("flashcards"):
                            st.markdown("#### 🎴 Flashcards générées automatiquement")
                            st.caption("Utilisez ces cartes pour réviser efficacement!")
                            
                            for i, card in enumerate(summary["flashcards"]):
                                with st.container():
                                    difficulty_badge = {
                                        "facile": "🟢",
                                        "moyen": "🟡",
                                        "difficile": "🔴"
                                    }.get(card.get("difficulte", "moyen").lower(), "⚪")
                                    
                                    st.markdown(f"**Carte {i+1}** {difficulty_badge} {card.get('difficulte', 'Moyen')}")
                                    
                                    # Question dans un expander
                                    with st.expander(f"❓ {card.get('question', '')}"):
                                        st.success(f"✅ **Réponse:** {card.get('reponse', '')}")
                                    st.divider()
                        else:
                            st.info("Flashcards non disponibles")
                
                else:
                    st.info("Aucun résumé disponible. Cliquez sur 'Analyser tous les documents'.")
                    if st.button("🗑️ Supprimer", key=f"del_no_summary_{idx}"):
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
