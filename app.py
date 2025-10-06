import streamlit as st
from config import Config
import os

# Configuration de la page
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# CSS personnalisé
def load_css():
    st.markdown(
        """
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Initialiser les variables de session"""
    if "profile" not in st.session_state:
        st.session_state.profile = None
    if "discipline" not in st.session_state:
        st.session_state.discipline = None
    if "niveau" not in st.session_state:
        st.session_state.niveau = None
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "quiz_results" not in st.session_state:
        st.session_state.quiz_results = []


def main():
    load_css()
    initialize_session_state()

    # Header
    st.markdown('<h1 class="main-header">🎓 QuizAI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">'
        "Plateforme d'apprentissage universitaire intelligente</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # Section 1: Sélection du profil
    st.markdown("## 1️⃣ Sélectionnez votre profil")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "👨‍🎓 Étudiant",
            use_container_width=True,
            type="primary" if st.session_state.profile == "Étudiant" else "secondary",
        ):
            st.session_state.profile = "Étudiant"
            st.rerun()

    with col2:
        if st.button(
            "👨‍🏫 Enseignant",
            use_container_width=True,
            type="primary" if st.session_state.profile == "Enseignant" else "secondary",
        ):
            st.session_state.profile = "Enseignant"
            st.rerun()

    with col3:
        if st.button(
            "🔬 Chercheur",
            use_container_width=True,
            type="primary" if st.session_state.profile == "Chercheur" else "secondary",
        ):
            st.session_state.profile = "Chercheur"
            st.rerun()

    if st.session_state.profile:
        st.success(f"✅ Profil sélectionné : **{st.session_state.profile}**")

        st.divider()

        # Section 2: Matière et Niveau
        st.markdown("## 2️⃣ Informations académiques")

        col1, col2 = st.columns(2)

        with col1:
            st.session_state.discipline = st.selectbox(
                "📚 Matière/Discipline",
                Config.DISCIPLINES,
                index=(
                    Config.DISCIPLINES.index(st.session_state.discipline)
                    if st.session_state.discipline
                    else 0
                ),
            )

        with col2:
            st.session_state.niveau = st.selectbox(
                "🎯 Niveau d'études",
                Config.NIVEAUX,
                index=(
                    Config.NIVEAUX.index(st.session_state.niveau)
                    if st.session_state.niveau
                    else 0
                ),
            )

        st.divider()

        # Section 3: Navigation
        st.markdown("## 3️⃣ Commencez votre apprentissage")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("**📚 Étape 1**\n\nUploadez vos documents (PDF, DOCX)")
            if st.button(
                "📤 Upload Documents", use_container_width=True, type="primary"
            ):
                st.switch_page("pages/1_📚_Upload_Documents.py")

        with col2:
            st.info("**📝 Étape 2**\n\nGénérez des quiz personnalisés")
            if st.button("🎲 Générer Quiz", use_container_width=True):
                st.switch_page("pages/2_📝_Generate_Quiz.py")

        with col3:
            st.info("**📊 Étape 3**\n\nConsultez vos résultats et recommandations")
            if st.button("📈 Voir Résultats", use_container_width=True):
                st.switch_page("pages/3_📊_Results.py")

        # Sidebar - Résumé du profil
        with st.sidebar:
            st.markdown("### 👤 Votre Profil")
            st.markdown(f"**Profil:** {st.session_state.profile}")
            st.markdown(f"**Discipline:** {st.session_state.discipline}")
            st.markdown(f"**Niveau:** {st.session_state.niveau}")

            st.divider()

            st.markdown("### 📊 Statistiques")
            st.metric("Documents uploadés", len(st.session_state.documents))
            st.metric("Quiz complétés", len(st.session_state.quiz_results))

            if st.session_state.quiz_results:
                avg_score = sum(
                    r.get("score", 0) for r in st.session_state.quiz_results
                ) / len(st.session_state.quiz_results)
                st.metric("Score moyen", f"{avg_score:.1f}/20")

    else:
        st.info("👆 Veuillez sélectionner votre profil pour continuer")


if __name__ == "__main__":
    main()
