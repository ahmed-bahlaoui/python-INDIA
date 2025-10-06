import json
import streamlit as st
from config import Config
from typing import List, Dict, Any, Optional
import openai
import re


class AIGenerator:
    """Class to generate content using different AI providers."""

    def __init__(self):
        self.provider = Config.AI_PROVIDER
        # Ensure model is always a string; fallback to openai model if provider key missing
        self.model = Config.MODELS.get(self.provider)
        if not self.model:
            self.model = Config.MODELS.get("openai")
        if not self.model:
            raise ValueError("No valid model found for AI provider.")
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Initialize the client depending on the provider."""
        if self.provider == "deepseek":
            return openai.OpenAI(
                api_key=Config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"
            )
        elif self.provider == "groq":
            return openai.OpenAI(
                api_key=Config.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1"
            )
        elif self.provider == "together":
            return openai.OpenAI(
                api_key=Config.TOGETHER_API_KEY, base_url="https://api.together.xyz/v1"
            )
        elif self.provider == "openai":
            return openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            raise ValueError(f"Provider {self.provider} non supporté")

    def _extract_text(self, response) -> Optional[str]:
        """Try to extract the generated text from various response shapes."""
        # If response is already a string
        if isinstance(response, str):
            return response

        # If it's a dict-like object
        try:
            # common OpenAI SDK shape
            if hasattr(response, "choices") and response.choices:
                first = response.choices[0]
                # choice.message.content
                msg = getattr(first, "message", None)
                if msg:
                    if isinstance(msg, dict):
                        return msg.get("content")
                    return getattr(msg, "content", None)
                # choice.text
                text = getattr(first, "text", None)
                if text:
                    return text

            # direct content attribute
            if hasattr(response, "content"):
                return getattr(response, "content")

            # dict-like fallback
            if isinstance(response, dict):
                # deep search for 'content' or 'text'
                def find_str(d):
                    if isinstance(d, str):
                        return d
                    if isinstance(d, dict):
                        for k in ("content", "text", "message", "output"):
                            if k in d:
                                found = find_str(d[k])
                                if found:
                                    return found
                        for v in d.values():
                            found = find_str(v)
                            if found:
                                return found
                    if isinstance(d, list):
                        for item in d:
                            found = find_str(item)
                            if found:
                                return found
                    return None

                return find_str(response)
        except Exception:
            return None

        return None

    def _generate_completion(
        self, prompt: str, max_tokens: int = 4096
    ) -> Optional[str]:
        """Generate a completion using the configured provider and return the text."""
        try:
            if self.model is None:
                raise ValueError("Model must not be None when generating completion.")
            if self.provider == "anthropic":
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
            else:  # OpenAI-compatible APIs (DeepSeek, Groq, Together, OpenAI)
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )

            text = self._extract_text(resp)
            if text:
                return text
            # As a last resort, try dumping the response to string
            return str(resp)

        except Exception as e:
            st.error(f"Erreur avec {self.provider}: {e}")
            return f"Erreur: {e}"

    def generate_summary(
        self, text: str, discipline: str, niveau: str
    ) -> Optional[Dict[str, Any]]:
        """Generate an intelligent structured summary with enhanced features."""

        prompt = f"""En tant qu'expert en {discipline} pour le niveau {niveau}, 
génère un résumé intelligent et structuré du document suivant.

ANALYSE REQUISE :
1. **Résumé par section/chapitre** (si le document a des chapitres)
2. **Mind map visuel** - Diagramme des concepts principaux et leurs relations
3. **Timeline** - Pour documents historiques/chronologiques (dates importantes)
4. **Glossaire automatique** - Termes techniques avec explications claires
5. **Flashcards** - Paires question/réponse pour révision
6. **Analyse de document** :
   - Type détecté (cours, article scientifique, rapport, etc.)
   - Niveau de difficulté estimé (débutant/intermédiaire/avancé)
   - Mots-clés principaux extraits
   - Concepts connexes suggérés
   - Temps de lecture estimé
   - Statistiques (nombre de pages, concepts uniques)

Document :
{text[:4000]}

IMPORTANT : Retourne UNIQUEMENT un objet JSON valide, sans texte avant ou après.
Format JSON requis :
{{
    "resume_general": "résumé général du document",
    "sections": [
        {{"titre": "Titre section", "contenu": "Résumé détaillé de la section"}}
    ],
    "mindmap": {{
        "concepts_principaux": ["concept1", "concept2"],
        "relations": [
            {{"de": "concept1", "vers": "concept2", "type": "implique"}}
        ]
    }},
    "timeline": [
        {{"date": "1990", "evenement": "Découverte importante", "importance": "haute"}}
    ],
    "glossaire": [
        {{"terme": "terme technique", "definition": "explication claire", "exemple": "exemple d'usage"}}
    ],
    "flashcards": [
        {{"question": "Question à poser", "reponse": "Réponse attendue", "difficulte": "facile|moyen|difficile"}}
    ],
    "analyse": {{
        "type_document": "cours|article|rapport|these|manuel",
        "niveau_difficulte": "debutant|intermediaire|avance",
        "mots_cles": ["mot1", "mot2", "mot3"],
        "concepts_connexes": ["concept lié 1", "concept lié 2"],
        "temps_lecture_min": 15,
        "statistiques": {{
            "nb_pages_estime": 10,
            "nb_mots": 3000,
            "nb_concepts_uniques": 25
        }}
    }},
    "definitions": ["def1", "def2"],
    "theoremes_formules": ["th1", "th2"],
    "concepts_cles": ["concept1", "concept2"],
    "liens_cours": ["lien1", "lien2"]
}}
"""

        response_text = self._generate_completion(prompt)

        if response_text:
            try:
                # Extract JSON from the response (in case model added surrounding text)
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
                else:
                    st.error("Format JSON non trouvé dans la réponse")
                    return self._create_default_summary()
            except json.JSONDecodeError as e:
                st.error(f"Erreur de parsing JSON: {e}")
                return self._create_default_summary()

        return None

    def generate_quiz(
        self,
        text: str,
        quiz_type: str,
        difficulty: str,
        num_questions: int,
        discipline: str,
    ) -> List[Dict[str, Any]]:
        """Generate a quiz based on the document."""

        prompt = f"""En tant que professeur de {discipline}, crée un quiz de type 
"{quiz_type}" avec {num_questions} questions de difficulté "{difficulty}".

Contenu du cours :
{text[:4000]}

Le quiz doit inclure :
- Des questions pertinentes et académiques
- Des choix de réponse plausibles pour les QCM
- Des explications détaillées pour chaque réponse

IMPORTANT : Retourne UNIQUEMENT un objet JSON valide, sans texte avant ou après.
Format JSON requis :
{{
    "questions": [
        {{
            "id": 1,
            "type": "qcm",
            "question": "Question text?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explication": "Explication détaillée",
            "points": 2,
            "competence": "Compréhension"
        }}
    ]
}}

Types de compétences : Compréhension, Application, Analyse, Mémorisation
"""

        response_text = self._generate_completion(prompt)

        if response_text:
            try:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    quiz_data = json.loads(json_str)
                    return quiz_data.get("questions", [])
                else:
                    st.error("Format JSON non trouvé dans la réponse")
                    return []
            except json.JSONDecodeError as e:
                st.error(f"Erreur de parsing JSON: {e}")
                return []

        return []

    def generate_recommendations(
        self, quiz_results: List[Dict[str, Any]], weak_areas: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Generate personalized recommendations based on quiz results."""

        # Summarize results
        summary = {
            "total_quizzes": len(quiz_results),
            "avg_score": (
                sum(r.get("score", 0) for r in quiz_results) / len(quiz_results)
                if quiz_results
                else 0
            ),
            "weak_areas": weak_areas[:5],
        }

        prompt = f"""En tant que conseiller pédagogique, analyse les résultats 
de l'étudiant et propose des recommandations personnalisées.

Résumé des résultats : 
- Nombre de quiz : {summary['total_quizzes']}
- Score moyen : {summary['avg_score']:.1f}/20
- Points faibles : {', '.join(summary['weak_areas'][:3])}

Génère des recommandations incluant :
1. Points à revoir (chapitres/sections spécifiques)
2. Exercices recommandés
3. Ressources supplémentaires
4. Stratégies d'apprentissage
5. Planning de révision suggéré

IMPORTANT : Retourne UNIQUEMENT un objet JSON valide, sans texte avant ou après.
Format JSON requis :
{{
    "points_a_revoir": [
        {{"chapitre": "Chapitre X", "raison": "Raison détaillée"}}
    ],
    "exercices_recommandes": ["Exercice 1", "Exercice 2"],
    "ressources": [
        {{"type": "vidéo", "titre": "Titre", "description": "Description"}}
    ],
    "strategies": ["Stratégie 1", "Stratégie 2"],
    "planning": {{
        "semaine_1": ["Action 1", "Action 2"],
        "semaine_2": ["Action 3"]
    }}
}}
"""

        response_text = self._generate_completion(prompt)

        if response_text:
            try:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except json.JSONDecodeError as e:
                st.error(f"Erreur de parsing JSON: {e}")
                return self._create_default_recommendations()

        return None

    def _create_default_summary(self) -> Dict[str, Any]:
        """Create a default summary when generation fails."""
        return {
            "resume_general": "Résumé en cours de génération...",
            "sections": [],
            "mindmap": {"concepts_principaux": [], "relations": []},
            "timeline": [],
            "glossaire": [],
            "flashcards": [],
            "analyse": {
                "type_document": "non déterminé",
                "niveau_difficulte": "intermediaire",
                "mots_cles": [],
                "concepts_connexes": [],
                "temps_lecture_min": 0,
                "statistiques": {
                    "nb_pages_estime": 0,
                    "nb_mots": 0,
                    "nb_concepts_uniques": 0
                }
            },
            "definitions": [],
            "theoremes_formules": [],
            "concepts_cles": [],
            "liens_cours": [],
        }

    def _create_default_recommendations(self) -> Dict[str, Any]:
        """Create default recommendations when generation fails."""
        return {
            "points_a_revoir": [],
            "exercices_recommandes": ["Refaire les exercices du cours"],
            "ressources": [],
            "strategies": ["Relire régulièrement", "Pratiquer avec des exercices"],
            "planning": {
                "semaine_1": ["Revoir les cours"],
                "semaine_2": ["Faire des exercices"],
            },
        }
