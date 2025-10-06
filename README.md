# 🎓 QuizAI - Plateforme d'Apprentissage Universitaire Intelligente

Une application Streamlit alimentée par l'IA pour générer des quiz personnalisés à partir de documents académiques.

## ✨ Fonctionnalités

- 📚 **Upload de Documents**: Supporte PDF et DOCX
- 🤖 **Résumés Automatiques**: Génération de résumés structurés avec IA
- 📝 **Génération de Quiz**: Création de quiz personnalisés (QCM, questions ouvertes)
- 📊 **Suivi des Résultats**: Analyse des performances et points faibles
- 💡 **Recommandations**: Suggestions d'apprentissage personnalisées
- 🎯 **Multi-disciplines**: Support pour toutes les matières universitaires
- 🔄 **Multi-providers AI**: DeepSeek, Groq, OpenAI, Ollama, Together

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Cloner le repository**
```bash
git clone <your-repo-url>
cd python-INDIA
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet:

```env
# Choisir le provider : deepseek, groq, ollama, anthropic, openai, together
AI_PROVIDER=groq

# API Keys (obtenez votre clé gratuite sur https://console.groq.com/keys)
GROQ_API_KEY=votre_clé_api_ici

# App Configuration
APP_ENV=development
DEBUG=True
```

5. **Lancer l'application**
```bash
streamlit run app.py
```

L'application sera accessible à `http://localhost:9000`

## 🔑 Configuration des Providers AI

Consultez le fichier [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) pour:
- Instructions détaillées pour chaque provider
- Comparaison des providers (prix, vitesse, qualité)
- Résolution des problèmes courants

### Changement Rapide de Provider

Utilisez le script interactif:
```bash
python switch_provider.py
```

## 📁 Structure du Projet

```
python-INDIA/
├── app.py                          # Application principale
├── config.py                       # Configuration globale
├── requirements.txt                # Dépendances Python
├── .env                           # Variables d'environnement (à créer)
├── .streamlit/
│   └── config.toml                # Configuration Streamlit
├── pages/                         # Pages multi-pages Streamlit
│   ├── 1_📚_Upload_Documents.py
│   ├── 2_📝_Generate_Quiz.py
│   ├── 3_📊_Results.py
│   └── 4_💡_Recommendations.py
├── utils/                         # Modules utilitaires
│   ├── __init__.py
│   ├── ai_generator.py           # Génération de contenu IA
│   ├── database.py               # Gestion de la base de données
│   ├── document_processor.py     # Traitement des documents
│   └── quiz_manager.py           # Gestion des quiz
└── assets/
    └── styles.css                # Styles personnalisés
```

## 🎯 Utilisation

1. **Sélectionnez votre profil** (Étudiant, Enseignant, Chercheur)
2. **Choisissez votre discipline et niveau**
3. **Uploadez vos documents** (PDF, DOCX)
4. **Analysez les documents** pour générer des résumés
5. **Générez des quiz** personnalisés
6. **Passez les quiz** et consultez vos résultats
7. **Recevez des recommandations** d'apprentissage

## 🛠️ Technologies

- **Frontend**: Streamlit
- **IA**: OpenAI API, Groq, DeepSeek, Ollama, Together
- **Traitement Documents**: PyPDF2, python-docx
- **Base de données**: SQLite (via utils/database.py)
- **Python**: 3.8+

## 📊 Providers AI Supportés

| Provider | Coût | Vitesse | Qualité | Lien |
|----------|------|---------|---------|------|
| **Groq** | ✅ Gratuit | ⚡ Très rapide | ⭐⭐⭐⭐ | [console.groq.com](https://console.groq.com) |
| DeepSeek | 💰 ~0.14$/M | 🚀 Rapide | ⭐⭐⭐⭐ | [platform.deepseek.com](https://platform.deepseek.com) |
| OpenAI | 💰💰 Variable | 🚀 Rapide | ⭐⭐⭐⭐⭐ | [platform.openai.com](https://platform.openai.com) |
| Ollama | ✅ Gratuit | 🐌 Moyen | ⭐⭐⭐ | [ollama.com](https://ollama.com) |

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT.

## 🆘 Support

Pour obtenir de l'aide:
- 📖 Consultez [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md)
- 🐛 Ouvrez une issue sur GitHub
- 💬 Contactez l'équipe de développement

## 🔒 Sécurité

⚠️ **IMPORTANT**: 
- Ne commitez JAMAIS votre fichier `.env` contenant vos clés API
- Le fichier `.gitignore` est configuré pour exclure les informations sensibles
- Utilisez des variables d'environnement pour les configurations sensibles

## 📈 Roadmap

- [ ] Support pour plus de formats de documents (PPT, TXT, Markdown)
- [ ] Export des quiz en PDF
- [ ] Mode hors ligne avec Ollama
- [ ] Interface multilingue
- [ ] Application mobile
- [ ] Intégration avec LMS (Moodle, Canvas)

## 👥 Auteurs

Développé avec ❤️ pour faciliter l'apprentissage universitaire.

---

**Note**: Ce projet utilise l'IA pour générer du contenu éducatif. Toujours vérifier les informations générées avec vos ressources académiques officielles.
