import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API Configuration
    AI_PROVIDER = os.getenv(
        "AI_PROVIDER", "deepseek"
    )  # deepseek, groq, ollama, anthropic, openai

    # API Keys
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    # Model Configuration per Provider
    MODELS = {
        "deepseek": "deepseek-chat",
        "groq": "llama-3.1-70b-versatile",  # ou mixtral-8x7b-32768
        "ollama": "llama3.1:8b",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-sonnet-20241022",
        "together": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    }

    # App Config
    APP_TITLE = "QuizAI - Apprentissage Universitaire"
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
