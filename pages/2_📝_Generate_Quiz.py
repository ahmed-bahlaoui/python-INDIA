import streamlit as st
from utils.ai_generator import AIGenerator
from utils.quiz_manager import QuizManager
from config import Config
import time
from datetime import datetime

st.set_page_config(page_title="Générer Quiz", page_icon="📝", layout="wide")


def main():
    st.title("📝 Génération et Passage de Quiz")

    # Vérifier le profil et les documents
    if not st.session_state.get("profile"):
        st.warning("⚠️ Veuillez d'abord sélectionner votre profil sur la page d'accueil")
        if st.button("← Retour à l'accueil"):
            st.switch_page("app.py")
        return

    if not st.session_state.get("documents"):
        st.warning("⚠️ Veuillez d'abord uploader des documents")
        if st.button("📚 Aller à Upload Documents"):
            st.switch_page("pages/1_📚_Upload_Documents.py")
        return

    st.markdown(
        f"**Profil:** {st.session_state.profile} | "
        f"**Discipline:** {st.session_state.discipline} | "
        f"**Niveau:** {st.session_state.niveau}"
    )

    st.divider()

    # Initialiser le quiz manager
    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager = QuizManager()

    # Initialiser l'état du quiz
    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = None
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Interface principale
    if not st.session_state.quiz_started:
        show_quiz_configuration()
    else:
        show_quiz_interface()


def show_quiz_configuration():
    """Afficher l'interface de configuration du quiz"""
    st.markdown("### ⚙️ Configuration du Quiz")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📚 Sélection du document")
        doc_names = [doc["name"] for doc in st.session_state.documents]
        selected_doc_name = st.selectbox(
            "Document source",
            doc_names,
            help="Choisissez le document sur lequel baser le quiz",
        )
        selected_doc = next(
            doc
            for doc in st.session_state.documents
            if doc["name"] == selected_doc_name
        )

        st.markdown("#### 📋 Type de Quiz")
        quiz_type = st.selectbox(
            "Format de quiz", Config.QUIZ_TYPES, help="Choisissez le type de questions"
        )

        st.markdown("#### 🎯 Difficulté")
        difficulty = st.radio(
            "Niveau de difficulté", Config.DIFFICULTIES, horizontal=True
        )

        st.markdown("#### 🎲 Nombre de questions")
        num_questions = st.slider(
            "Questions à générer", min_value=5, max_value=50, value=15, step=5
        )

    with col2:
        st.markdown("#### 📊 Mode d'évaluation")
        eval_mode = st.selectbox("Mode", Config.EVAL_MODES)

        st.markdown("#### ⚖️ Barème")
        bareme = st.radio(
            "Type de barème",
            ["Binaire (0 ou max points)", "Points négatifs", "Partiel"],
            help="Binaire: tout ou rien | Points négatifs: pénalités | Partiel: points partiels",
        )

        st.markdown("#### ⏱️ Temps suggéré")
        auto_time = st.checkbox(
            "Calculer automatiquement selon le nombre de questions", value=True
        )

        if auto_time:
            suggested_time = num_questions * 2  # 2 min par question
            st.info(f"⏱️ Temps suggéré : {suggested_time} minutes")
        else:
            suggested_time = st.number_input(
                "Temps limite (minutes)", min_value=5, max_value=180, value=30
            )

        st.markdown("#### 📝 Options avancées")
        show_explanations = st.checkbox(
            "Afficher les explications après chaque question", value=False
        )
        shuffle_questions = st.checkbox("Mélanger l'ordre des questions", value=True)
        shuffle_options = st.checkbox("Mélanger l'ordre des réponses", value=True)

    st.divider()

    # Bouton de génération
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
            "🎲 Générer et Commencer le Quiz", type="primary", use_container_width=True
        ):
            generate_and_start_quiz(
                selected_doc,
                quiz_type,
                difficulty,
                num_questions,
                eval_mode,
                bareme,
                suggested_time,
                show_explanations,
                shuffle_questions,
                shuffle_options,
            )


def generate_and_start_quiz(
    doc,
    quiz_type,
    difficulty,
    num_questions,
    eval_mode,
    bareme,
    time_limit,
    show_explanations,
    shuffle_questions,
    shuffle_options,
):
    """Générer et démarrer un nouveau quiz"""
    with st.spinner("🎲 Génération du quiz en cours..."):
        ai_gen = AIGenerator()

        # Générer les questions
        questions = ai_gen.generate_quiz(
            doc["text"],
            quiz_type,
            difficulty,
            num_questions,
            st.session_state.discipline,
        )

        if questions:
            # Créer le quiz
            quiz = {
                "id": f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "document": doc["name"],
                "quiz_type": quiz_type,
                "difficulty": difficulty,
                "eval_mode": eval_mode,
                "bareme": bareme,
                "time_limit": time_limit,
                "show_explanations": show_explanations,
                "questions": questions,
                "created_at": datetime.now().isoformat(),
            }

            # Mélanger si nécessaire
            if shuffle_questions:
                import random

                random.shuffle(quiz["questions"])

            if shuffle_options:
                import random

                for q in quiz["questions"]:
                    if q["type"] == "qcm" and "options" in q:
                        # Sauvegarder la bonne réponse AVANT de mélanger
                        correct_answer_text = q["correct_answer"]
                        random.shuffle(q["options"])
                        # La bonne réponse reste la même (le texte ne change pas)
                        q["correct_answer"] = correct_answer_text

            # Sauvegarder le quiz
            st.session_state.current_quiz = quiz
            st.session_state.quiz_started = True
            st.session_state.current_question_idx = 0
            st.session_state.user_answers = {}
            st.session_state.start_time = datetime.now()

            st.success("✅ Quiz généré avec succès!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Erreur lors de la génération du quiz")


def show_quiz_interface():
    """Afficher l'interface du quiz en cours"""
    quiz = st.session_state.current_quiz
    current_idx = st.session_state.current_question_idx

    # Header avec progression
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        progress = (current_idx + 1) / len(quiz["questions"])
        st.progress(progress)
        st.caption(f"Question {current_idx + 1} / {len(quiz['questions'])}")

    with col2:
        # Timer
        elapsed = (datetime.now() - st.session_state.start_time).seconds // 60
        remaining = quiz["time_limit"] - elapsed
        st.metric("⏱️ Temps restant", f"{remaining} min")

    with col3:
        # Score actuel
        answered = len(st.session_state.user_answers)
        st.metric("✅ Répondues", f"{answered}/{len(quiz['questions'])}")

    st.divider()

    # Question actuelle
    if current_idx < len(quiz["questions"]):
        question = quiz["questions"][current_idx]

        st.markdown(f"### Question {current_idx + 1}")
        st.markdown(f"**{question['question']}**")
        st.caption(
            f"🎯 Compétence : {question.get('competence', 'N/A')} | "
            f"⭐ Points : {question.get('points', 1)}"
        )

        st.divider()

        # Interface de réponse
        if question["type"] == "qcm":
            answer = st.radio(
                "Choisissez votre réponse :",
                question["options"],
                key=f"q_{current_idx}",
                index=None,
            )
        else:
            answer = st.text_area("Votre réponse :", key=f"q_{current_idx}", height=150)

        st.divider()

        # Boutons de navigation
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if current_idx > 0:
                if st.button("⬅️ Question Précédente", use_container_width=True):
                    st.session_state.current_question_idx -= 1
                    st.rerun()

        with col2:
            if answer:
                if st.button(
                    "💾 Enregistrer", type="primary", use_container_width=True
                ):
                    st.session_state.user_answers[current_idx] = answer
                    st.success("✅ Réponse enregistrée!")
                    time.sleep(0.5)

        with col3:
            if current_idx < len(quiz["questions"]) - 1:
                if st.button("Question Suivante ➡️", use_container_width=True):
                    if answer:
                        st.session_state.user_answers[current_idx] = answer
                    st.session_state.current_question_idx += 1
                    st.rerun()
            else:
                if st.button(
                    "🏁 Terminer le Quiz", type="primary", use_container_width=True
                ):
                    if answer:
                        st.session_state.user_answers[current_idx] = answer
                    finish_quiz()

        # Afficher l'explication si activé
        if quiz["show_explanations"] and current_idx in st.session_state.user_answers:
            st.info("💡 **Explication :** " + question.get("explication", "N/A"))

    # Sidebar - Navigation rapide
    with st.sidebar:
        st.markdown("### 📋 Navigation Rapide")

        for idx, q in enumerate(quiz["questions"]):
            status = "✅" if idx in st.session_state.user_answers else "⭕"
            if st.button(
                f"{status} Q{idx + 1}", key=f"nav_{idx}", use_container_width=True
            ):
                st.session_state.current_question_idx = idx
                st.rerun()

        st.divider()

        if st.button("❌ Abandonner le Quiz", type="secondary"):
            if st.button("⚠️ Confirmer l'abandon"):
                reset_quiz()
                st.rerun()


def finish_quiz():
    """Terminer et évaluer le quiz"""
    quiz = st.session_state.current_quiz

    # Calculer le score
    result = st.session_state.quiz_manager.evaluate_quiz(
        quiz, st.session_state.user_answers
    )

    # Sauvegarder les résultats
    result["end_time"] = datetime.now().isoformat()
    result["duration"] = (datetime.now() - st.session_state.start_time).seconds // 60
    st.session_state.quiz_results.append(result)

    # Réinitialiser
    reset_quiz()

    # Rediriger vers les résultats
    st.switch_page("pages/3_📊_Results.py")


def reset_quiz():
    """Réinitialiser l'état du quiz"""
    st.session_state.current_quiz = None
    st.session_state.quiz_started = False
    st.session_state.current_question_idx = 0
    st.session_state.user_answers = {}
    st.session_state.start_time = None


if __name__ == "__main__":
    main()
