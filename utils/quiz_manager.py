from typing import Dict, List
import re


class QuizManager:
    """Gestionnaire de quiz"""

    def __init__(self):
        pass

    def evaluate_quiz(self, quiz: Dict, user_answers: Dict) -> Dict:
        """Évaluer un quiz complété"""
        questions = quiz["questions"]
        total_points = sum(q.get("points", 1) for q in questions)
        earned_points = 0
        correct_answers = 0
        competence_breakdown = {}
        weak_areas = []

        for idx, question in enumerate(questions):
            if idx not in user_answers:
                continue

            user_answer = user_answers[idx]
            correct = False
            points = 0

            if question["type"] == "qcm":
                if user_answer == question["correct_answer"]:
                    correct = True
                    points = question.get("points", 1)
                else:
                    # Appliquer le barème
                    if quiz["bareme"] == "Points négatifs":
                        points = -question.get("points", 1) * 0.25

            else:  # Question ouverte
                # Évaluation simple par mots-clés
                correct = self._evaluate_open_question(
                    user_answer, question["correct_answer"]
                )
                if correct:
                    points = question.get("points", 1)
                elif quiz["bareme"] == "Partiel":
                    # Points partiels
                    points = question.get("points", 1) * 0.5

            if correct:
                correct_answers += 1

            earned_points += max(0, points)  # Pas de points négatifs en dessous de 0

            # Analyse par compétence
            competence = question.get("competence", "Général")
            if competence not in competence_breakdown:
                competence_breakdown[competence] = {"earned": 0, "total": 0}

            competence_breakdown[competence]["earned"] += points
            competence_breakdown[competence]["total"] += question.get("points", 1)

            # Identifier les points faibles
            if not correct:
                weak_areas.append(question["question"][:50] + "...")

        # Calculer le score sur 20
        score = (earned_points / total_points) * 20 if total_points > 0 else 0
        percentage = (earned_points / total_points) * 100 if total_points > 0 else 0

        # Calculer les pourcentages par compétence
        competence_percentages = {
            comp: (data["earned"] / data["total"] * 100) if data["total"] > 0 else 0
            for comp, data in competence_breakdown.items()
        }

        return {
            "quiz_id": quiz["id"],
            "score": score,
            "percentage": percentage,
            "earned_points": earned_points,
            "total_points": total_points,
            "correct_answers": correct_answers,
            "total_questions": len(questions),
            "competence_breakdown": competence_percentages,
            "weak_areas": weak_areas[:5],  # Top 5 points faibles
        }

    def _evaluate_open_question(self, user_answer: str, correct_answer: str) -> bool:
        """Évaluer une question ouverte (simple)"""
        # Normaliser les textes
        user_lower = user_answer.lower().strip()
        correct_lower = correct_answer.lower().strip()

        # Extraire les mots-clés de la réponse correcte
        keywords = set(re.findall(r"\b\w{4,}\b", correct_lower))
        user_words = set(re.findall(r"\b\w{4,}\b", user_lower))

        # Calculer le pourcentage de mots-clés présents
        if not keywords:
            return False

        match_percentage = len(keywords & user_words) / len(keywords)

        return match_percentage >= 0.6  # 60% de correspondance

    def get_quiz_statistics(self, quiz_results: List[Dict]) -> Dict:
        """Obtenir des statistiques globales"""
        if not quiz_results:
            return {}

        total = len(quiz_results)
        avg_score = sum(r["score"] for r in quiz_results) / total
        avg_percentage = sum(r["percentage"] for r in quiz_results) / total

        # Meilleur et pire score
        best = max(quiz_results, key=lambda x: x["score"])
        worst = min(quiz_results, key=lambda x: x["score"])

        return {
            "total_quizzes": total,
            "average_score": avg_score,
            "average_percentage": avg_percentage,
            "best_score": best["score"],
            "worst_score": worst["score"],
            "improvement": (
                (quiz_results[-1]["score"] - quiz_results[0]["score"])
                if total > 1
                else 0
            ),
        }
