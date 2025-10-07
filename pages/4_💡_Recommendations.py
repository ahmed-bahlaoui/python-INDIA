import streamlit as st
from utils.ai_generator import AIGenerator
import plotly.graph_objects as go

st.set_page_config(page_title="Recommandations", page_icon="💡", layout="wide")


def main():
    st.title("💡 Recommandations Personnalisées")

    if not st.session_state.get("profile"):
        st.warning("⚠️ Veuillez d'abord sélectionner votre profil")
        if st.button("← Retour à l'accueil"):
            st.switch_page("app.py")
        return

    if not st.session_state.get("quiz_results"):
        st.info("📝 Complétez des quiz pour obtenir des recommandations")
        if st.button("🎲 Générer un Quiz"):
            st.switch_page("pages/2_📝_Generate_Quiz.py")
        return

    st.divider()

    # Générer les recommandations
    if "recommendations" not in st.session_state:
        with st.spinner("🤖 Génération de recommandations personnalisées..."):
            generate_recommendations()

    recommendations = st.session_state.get("recommendations")

    if recommendations:
        # Points à revoir
        st.markdown("## ⚠️ Points à Revoir")

        for point in recommendations.get("points_a_revoir", []):
            with st.expander(f"📖 {point.get('chapitre', 'Chapitre')}", expanded=True):
                st.warning(f"**Raison :** {point.get('raison', '')}")

                # Suggestions d'actions
                st.markdown("**Actions suggérées :**")
                st.markdown("- Relire le cours")
                st.markdown("- Faire les exercices d'application")
                st.markdown("- Consulter les annales")

        st.divider()

        # Exercices recommandés
        st.markdown("## 📚 Exercices Recommandés")

        exercices = recommendations.get("exercices_recommandes", [])

        if exercices:
            col1, col2 = st.columns(2)

            for idx, exercice in enumerate(exercices):
                with col1 if idx % 2 == 0 else col2:
                    st.info(f"📝 **Exercice {idx + 1}:** {exercice}")
        else:
            st.info("Continuez à pratiquer avec des quiz")

        st.divider()

        # Ressources supplémentaires
        st.markdown("## 📖 Ressources Supplémentaires")

        ressources = recommendations.get("ressources", [])

        for ressource in ressources:
            ressource_type = ressource.get("type", "ressource")
            icon = {"vidéo": "🎥", "livre": "📚", "article": "📄", "cours": "🎓"}.get(
                ressource_type.lower(), "📌"
            )

            with st.expander(f"{icon} {ressource.get('titre', 'Ressource')}"):
                st.markdown(ressource.get("description", ""))

                if st.button(f"🔗 Consulter", key=f"res_{ressource.get('titre')}"):
                    st.info("Lien vers la ressource")

        st.divider()

        # Stratégies d'apprentissage
        st.markdown("## 🎯 Stratégies d'Apprentissage")

        strategies = recommendations.get("strategies", [])

        if strategies:
            for idx, strategy in enumerate(strategies, 1):
                st.success(f"**{idx}.** {strategy}")

        st.divider()

        # Planning de révision
        st.markdown("## 📅 Planning de Révision Suggéré")

        planning = recommendations.get("planning", {})

        if planning:
            for week, actions in planning.items():
                with st.expander(f"📆 {week.replace('_', ' ').title()}", expanded=True):
                    for action in actions:
                        st.checkbox(action, key=f"plan_{week}_{action}")

        st.divider()

        # Visualisation de la progression
        st.markdown("## 📈 Projection de Progression")

        show_progress_projection()

        # Boutons d'action
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Régénérer les Recommandations", use_container_width=True):
                del st.session_state["recommendations"]
                st.rerun()

        with col2:
            if st.button(
                "📥 Exporter le Plan", type="primary", use_container_width=True
            ):
                st.info("Fonctionnalité à implémenter")

    else:
        st.error("Erreur lors de la génération des recommandations")
        if st.button("🔄 Réessayer"):
            st.rerun()


def generate_recommendations():
    """Générer les recommandations avec AI"""
    try:
        ai_gen = AIGenerator()
        results = st.session_state.quiz_results

        # Identifier les points faibles
        weak_areas = []
        for result in results:
            if "competence_breakdown" in result:
                for comp, score in result["competence_breakdown"].items():
                    if score < 60:
                        weak_areas.append(comp)
        
        # Ajouter aussi les weak_areas de chaque résultat
        for result in results:
            if "weak_areas" in result:
                weak_areas.extend(result["weak_areas"])

        # Générer les recommandations
        recommendations = ai_gen.generate_recommendations(results, weak_areas)
        
        # Vérifier que les recommandations ne sont pas None
        if recommendations is None:
            st.error("Erreur lors de la génération des recommandations")
            recommendations = {
                "points_a_revoir": [],
                "exercices_recommandes": ["Refaire les exercices du cours"],
                "ressources": [],
                "strategies": ["Relire régulièrement", "Pratiquer avec des exercices"],
                "planning": {
                    "semaine_1": ["Revoir les cours"],
                    "semaine_2": ["Faire des exercices"],
                },
            }
        
        st.session_state.recommendations = recommendations
    except Exception as e:
        st.error(f"Erreur lors de la génération: {str(e)}")
        # Fournir des recommandations par défaut
        st.session_state.recommendations = {
            "points_a_revoir": [],
            "exercices_recommandes": ["Refaire les exercices du cours"],
            "ressources": [],
            "strategies": ["Relire régulièrement", "Pratiquer avec des exercices"],
            "planning": {
                "semaine_1": ["Revoir les cours"],
                "semaine_2": ["Faire des exercices"],
            },
        }


def show_progress_projection():
    """Afficher une projection de progression"""
    results = st.session_state.quiz_results

    if len(results) < 2:
        st.info("Complétez plus de quiz pour voir la projection")
        return

    # Calculer la tendance
    scores = [r["score"] for r in results]

    # Projection linéaire simple
    import numpy as np

    x = np.arange(len(scores))
    z = np.polyfit(x, scores, 1)
    p = np.poly1d(z)

    # Projeter 5 quiz dans le futur
    future_x = np.arange(len(scores), len(scores) + 5)
    future_scores = p(future_x)

    # Graphique
    fig = go.Figure()

    # Scores réels
    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(scores) + 1)),
            y=scores,
            mode="lines+markers",
            name="Scores Réels",
            line=dict(color="#1f77b4", width=3),
        )
    )

    # Projection
    fig.add_trace(
        go.Scatter(
            x=list(range(len(scores) + 1, len(scores) + 6)),
            y=future_scores,
            mode="lines+markers",
            name="Projection",
            line=dict(color="#2ecc71", width=2, dash="dash"),
        )
    )

    fig.add_hline(
        y=10, line_dash="dash", line_color="red", annotation_text="Seuil de réussite"
    )

    fig.update_layout(
        title="Projection de vos performances",
        xaxis_title="Numéro du Quiz",
        yaxis_title="Score (/20)",
        yaxis_range=[0, 20],
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Message motivant
    if future_scores[-1] > scores[-1]:
        st.success(
            f"📈 Tendance positive ! En continuant ainsi, vous pourriez atteindre {future_scores[-1]:.1f}/20"
        )
    else:
        st.warning(f"📉 Redoublez d'efforts pour améliorer vos résultats")


if __name__ == "__main__":
    main()
