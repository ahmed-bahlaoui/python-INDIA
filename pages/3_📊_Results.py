import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Résultats", page_icon="📊", layout="wide")


def main():
    st.title("📊 Résultats et Analyse")

    if not st.session_state.get("profile"):
        st.warning("⚠️ Veuillez d'abord sélectionner votre profil")
        if st.button("← Retour à l'accueil"):
            st.switch_page("app.py")
        return

    if not st.session_state.get("quiz_results"):
        st.info("📝 Vous n'avez pas encore complété de quiz")
        if st.button("🎲 Générer un Quiz"):
            st.switch_page("pages/2_📝_Generate_Quiz.py")
        return

    st.divider()

    # Onglets
    tab1, tab2, tab3 = st.tabs(
        ["📈 Vue d'ensemble", "📋 Détails des Quiz", "🎯 Analyse par Compétence"]
    )

    with tab1:
        show_overview()

    with tab2:
        show_quiz_details()

    with tab3:
        show_competence_analysis()


def show_overview():
    """Afficher la vue d'ensemble des résultats"""
    results = st.session_state.quiz_results

    # Statistiques globales
    st.markdown("### 📊 Statistiques Globales")

    col1, col2, col3, col4 = st.columns(4)

    # Calculs
    total_quizzes = len(results)
    avg_score = sum(r["score"] for r in results) / total_quizzes
    avg_percentage = sum(r["percentage"] for r in results) / total_quizzes
    total_time = sum(r.get("duration", 0) for r in results)

    with col1:
        st.metric("🎯 Quiz Complétés", total_quizzes)

    with col2:
        st.metric("📈 Score Moyen", f"{avg_score:.1f}/20")
        delta_color = "normal" if avg_score >= 10 else "inverse"

    with col3:
        st.metric("✅ Taux de Réussite", f"{avg_percentage:.1f}%")

    with col4:
        st.metric("⏱️ Temps Total", f"{total_time} min")

    st.divider()

    # Graphiques
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Évolution des Scores")

        # Graphique d'évolution
        df = pd.DataFrame(
            [
                {
                    "Quiz": f"Quiz {i+1}",
                    "Score": r["score"],
                    "Date": r.get("end_time", "")[:10],
                }
                for i, r in enumerate(results)
            ]
        )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["Quiz"],
                y=df["Score"],
                mode="lines+markers",
                name="Score",
                line=dict(color="#1f77b4", width=3),
                marker=dict(size=10),
            )
        )
        fig.add_hline(
            y=10,
            line_dash="dash",
            line_color="red",
            annotation_text="Seuil de réussite",
        )
        fig.update_layout(
            xaxis_title="Quiz",
            yaxis_title="Score (/20)",
            yaxis_range=[0, 20],
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🎯 Répartition des Mentions")

        # Calculer les mentions
        mentions = {
            "Excellent (≥16)": sum(1 for r in results if r["score"] >= 16),
            "Très Bien (14-16)": sum(1 for r in results if 14 <= r["score"] < 16),
            "Bien (12-14)": sum(1 for r in results if 12 <= r["score"] < 14),
            "Assez Bien (10-12)": sum(1 for r in results if 10 <= r["score"] < 12),
            "Insuffisant (<10)": sum(1 for r in results if r["score"] < 10),
        }

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=list(mentions.keys()),
                    values=list(mentions.values()),
                    hole=0.3,
                    marker_colors=[
                        "#2ecc71",
                        "#3498db",
                        "#f39c12",
                        "#e67e22",
                        "#e74c3c",
                    ],
                )
            ]
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Derniers résultats
    st.markdown("### 📋 Derniers Résultats")

    latest = results[-1]

    st.markdown(
        f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white;">
        <h3>📊 Dernier Quiz Complété</h3>
        <p><strong>Note :</strong> {latest['score']:.1f}/20 ({latest['percentage']:.1f}%)</p>
        <p><strong>Mention :</strong> {get_mention(latest['score'])}</p>
        <p><strong>Temps écoulé :</strong> {latest.get('duration', 'N/A')} min</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Bouton vers recommandations
    if st.button(
        "💡 Voir les Recommandations Personnalisées",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/4_💡_Recommendations.py")


def show_quiz_details():
    """Afficher les détails de chaque quiz"""
    results = st.session_state.quiz_results

    for idx, result in enumerate(reversed(results)):
        with st.expander(
            f"📝 Quiz #{len(results) - idx} - Score: {result['score']:.1f}/20",
            expanded=(idx == 0),
        ):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📈 Score", f"{result['score']:.1f}/20")
                st.metric("✅ Taux de réussite", f"{result['percentage']:.1f}%")

            with col2:
                st.metric("⏱️ Durée", f"{result.get('duration', 'N/A')} min")
                st.metric("📊 Questions", f"{result.get('total_questions', 'N/A')}")

            with col3:
                st.metric("🎯 Mention", get_mention(result["score"]))
                st.metric("✔️ Correctes", f"{result.get('correct_answers', 0)}")

            st.divider()

            # Analyse par compétence
            if "competence_breakdown" in result:
                st.markdown("#### 📊 Analyse par Compétence")

                comp_data = result["competence_breakdown"]
                df_comp = pd.DataFrame(
                    [{"Compétence": k, "Score": v} for k, v in comp_data.items()]
                )

                fig = px.bar(
                    df_comp,
                    x="Compétence",
                    y="Score",
                    color="Score",
                    color_continuous_scale="RdYlGn",
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # Points à revoir
            if "weak_areas" in result and result["weak_areas"]:
                st.markdown("#### ⚠️ Points à Revoir")
                for area in result["weak_areas"]:
                    st.markdown(f"- {area}")

            # Boutons d'action
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(
                    "📥 Télécharger Corrigé",
                    key=f"download_{idx}",
                    use_container_width=True,
                ):
                    st.info("Fonctionnalité à implémenter")

            with col2:
                if st.button(
                    "📊 Voir Statistiques", key=f"stats_{idx}", use_container_width=True
                ):
                    st.info("Fonctionnalité à implémenter")

            with col3:
                if st.button(
                    "🔄 Recommencer Quiz", key=f"retry_{idx}", use_container_width=True
                ):
                    st.info("Fonctionnalité à implémenter")


def show_competence_analysis():
    """Analyser les performances par compétence"""
    results = st.session_state.quiz_results

    st.markdown("### 🎯 Analyse Détaillée par Compétence")

    # Agréger les données par compétence
    all_competences = {}

    for result in results:
        if "competence_breakdown" in result:
            for comp, score in result["competence_breakdown"].items():
                if comp not in all_competences:
                    all_competences[comp] = []
                all_competences[comp].append(score)

    if all_competences:
        # Calcul des moyennes
        comp_averages = {
            comp: sum(scores) / len(scores) for comp, scores in all_competences.items()
        }

        # Graphique radar
        categories = list(comp_averages.keys())
        values = list(comp_averages.values())

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=values, theta=categories, fill="toself", name="Vos Performances"
            )
        )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Détails par compétence
        st.markdown("#### 📋 Détails par Compétence")

        for comp, avg in sorted(
            comp_averages.items(), key=lambda x: x[1], reverse=True
        ):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"**{comp}**")

            with col2:
                st.progress(avg / 100)

            with col3:
                st.metric("Score moyen", f"{avg:.1f}%")

            # Recommandation
            if avg < 50:
                st.error(f"⚠️ Compétence à travailler en priorité")
            elif avg < 70:
                st.warning(f"📚 Nécessite plus de pratique")
            else:
                st.success(f"✅ Bonne maîtrise")

            st.divider()
    else:
        st.info("Pas encore assez de données pour l'analyse par compétence")


def get_mention(score):
    """Obtenir la mention selon le score"""
    if score >= 16:
        return "Excellent 🌟"
    elif score >= 14:
        return "Très Bien 🎉"
    elif score >= 12:
        return "Bien 👍"
    elif score >= 10:
        return "Assez Bien ✔️"
    else:
        return "Insuffisant 📚"


if __name__ == "__main__":
    main()
