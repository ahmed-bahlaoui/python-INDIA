# 🔑 Guide de Configuration des API

Votre application QuizAI supporte plusieurs fournisseurs d'IA. Voici comment les configurer :

## ⚡ **Option 1: Groq (RECOMMANDÉ - GRATUIT)**

**Avantages:** Gratuit, Rapide, Excellent pour les étudiants

### Étapes:

1. Visitez: https://console.groq.com/keys
2. Créez un compte gratuit
3. Générez une clé API
4. Modifiez votre fichier `.env`:

```env
AI_PROVIDER=groq
GROQ_API_KEY=gsk_votre_clé_ici
```

**Modèles disponibles:**

- `llama-3.1-70b-versatile` (par défaut)
- `mixtral-8x7b-32768`

---

## 🚀 **Option 2: DeepSeek (Payant)**

**Avantages:** Bon rapport qualité/prix

### Étapes:

1. Visitez: https://platform.deepseek.com/
2. Rechargez votre compte (minimum 10$)
3. Copiez votre clé API
4. Modifiez votre fichier `.env`:

```env
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk_votre_clé_ici
```

**Note:** Votre clé actuelle a un solde insuffisant.

---

## 🤖 **Option 3: OpenAI (Payant - Haute Qualité)**

**Avantages:** Meilleure qualité, Modèles avancés (GPT-4)

### Étapes:

1. Visitez: https://platform.openai.com/api-keys
2. Créez une clé API
3. Modifiez votre fichier `.env`:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk_votre_clé_ici
```

**Modèles:** `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`

---

## 🏠 **Option 4: Ollama (GRATUIT - LOCAL)**

**Avantages:** 100% gratuit, privé, hors ligne

### Étapes:

1. Installez Ollama: https://ollama.com/download
2. Téléchargez un modèle:

```bash
ollama pull llama3.1:8b
```

3. Modifiez votre fichier `.env`:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

**Note:** Nécessite un ordinateur puissant (8GB+ RAM)

---

## 🎯 **Comparaison Rapide**

| Provider | Prix                    | Vitesse        | Qualité    | Setup  |
| -------- | ----------------------- | -------------- | ---------- | ------ |
| **Groq** | ✅ Gratuit              | ⚡ Très rapide | ⭐⭐⭐⭐   | Facile |
| DeepSeek | 💰 ~0.14$/M tokens      | 🚀 Rapide      | ⭐⭐⭐⭐   | Facile |
| OpenAI   | 💰💰 ~0.15-60$/M tokens | 🚀 Rapide      | ⭐⭐⭐⭐⭐ | Facile |
| Ollama   | ✅ Gratuit              | 🐌 Moyen       | ⭐⭐⭐     | Moyen  |

---

## 🔧 **Modification du fichier .env**

Éditez le fichier `.env` à la racine du projet:

```env
# Choisir le provider : deepseek, groq, ollama, anthropic, openai, together
AI_PROVIDER=groq

# API Keys (ajoutez celle que vous utilisez)
GROQ_API_KEY=votre_clé_groq
DEEPSEEK_API_KEY=votre_clé_deepseek
OPENAI_API_KEY=votre_clé_openai

# Ollama (si vous utilisez Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# App Configuration
APP_ENV=development
DEBUG=True
```

---

## ✅ **Test de Configuration**

Après modification, redémarrez Streamlit:

```bash
streamlit run app.py
```

Essayez de générer un quiz pour vérifier que tout fonctionne!

---

## 🆘 **Problèmes Courants**

### Erreur: "Insufficient Balance"

- **Solution:** Rechargez votre compte ou passez à Groq (gratuit)

### Erreur: "Invalid API Key"

- **Solution:** Vérifiez que la clé est correcte dans `.env`

### Erreur: "Connection Error"

- **Solution:** Vérifiez votre connexion internet

---

## 📞 **Support**

Pour obtenir de l'aide, consultez:

- Groq: https://console.groq.com/docs
- OpenAI: https://platform.openai.com/docs
- DeepSeek: https://platform.deepseek.com/docs
