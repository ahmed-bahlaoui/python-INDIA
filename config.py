import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # AI Provider Configuration
    AI_PROVIDER = os.getenv("AI_PROVIDER", "deepseek")

    # API Keys
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    XAI_API_KEY = os.getenv("XAI_API_KEY")  # Added xAI support

    # Models for each provider
    MODELS = {
        "deepseek": "deepseek-chat",
        "groq": "openai/gpt-oss-120b",
        "together": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "openai": "gpt-4o-mini",
        "xai": "grok-beta",
    }

    # App Configuration
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # App Config
    APP_TITLE = "MentorAI - Apprentissage Universitaire"
    MAX_FILE_SIZE = 10  # MB

    # ... reste du config
    PROFILES = ["Étudiant", "Enseignant", "Chercheur"]
    DISCIPLINES = [
        "Informatique",
        "Mathématiques",
        "Physique",
        "Chimie",
        "Biologie",
        "Économie",
        "Droit",
        "Médecine",
        "Ingénierie",
        "Sciences Humaines",
    ]
    NIVEAUX = ["L1", "L2", "L3", "M1", "M2", "Doctorat"]
    QUIZ_TYPES = [
        "QCM Examen",
        "Questions de cours",
        "Exercices d'application",
        "Questions de synthèse",
        "Préparation TD/TP",
        "Révision finale",
    ]
    EVAL_MODES = [
        "Mode Contrôle Continu",
        "Mode Examen Final",
        "Mode Rattrapage",
        "Mode Auto-évaluation",
    ]
    DIFFICULTIES = [
        "Niveau TD (facile)",
        "Niveau Partiel (moyen)",
        "Niveau Examen Final (difficile)",
    ]
