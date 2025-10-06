import json
import os
from datetime import datetime
from typing import Dict, List


class Database:
    """Gestionnaire de base de données simple (JSON)"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_user_profile(self, profile_data: Dict):
        """Sauvegarder le profil utilisateur"""
        filepath = os.path.join(self.data_dir, "profile.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)

    def load_user_profile(self) -> Dict:
        """Charger le profil utilisateur"""
        filepath = os.path.join(self.data_dir, "profile.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_documents(self, documents: List[Dict]):
        """Sauvegarder les documents"""
        filepath = os.path.join(self.data_dir, "documents.json")
        # Ne pas sauvegarder le texte complet (trop volumineux)
        docs_light = [
            {k: v for k, v in doc.items() if k != "text"} for doc in documents
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(docs_light, f, indent=2, ensure_ascii=False)

    def save_quiz_results(self, results: List[Dict]):
        """Sauvegarder les résultats de quiz"""
        filepath = os.path.join(self.data_dir, "quiz_results.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    def load_quiz_results(self) -> List[Dict]:
        """Charger les résultats de quiz"""
        filepath = os.path.join(self.data_dir, "quiz_results.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def export_to_csv(self, results: List[Dict], filename: str):
        """Exporter les résultats en CSV"""
        import pandas as pd

        df = pd.DataFrame(results)
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False, encoding="utf-8")
        return filepath
