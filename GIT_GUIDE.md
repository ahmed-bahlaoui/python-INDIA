# 📚 Git Workflow Guide - QuizAI Project

Ce guide vous aide à gérer votre repository Git pour le projet QuizAI.

## 🎯 Configuration Initiale (Déjà Fait ✅)

```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit"
```

## 📝 Workflow Quotidien

### 1. Vérifier l'état de vos fichiers
```bash
git status
```

### 2. Voir les modifications
```bash
# Voir les fichiers modifiés
git status

# Voir les changements détaillés
git diff

# Voir les changements d'un fichier spécifique
git diff app.py
```

### 3. Ajouter des fichiers
```bash
# Ajouter un fichier spécifique
git add app.py

# Ajouter tous les fichiers Python modifiés
git add *.py

# Ajouter tous les fichiers
git add .

# Ajouter de manière interactive
git add -p
```

### 4. Faire un commit
```bash
# Commit avec message
git commit -m "Description des changements"

# Commit avec message détaillé
git commit -m "Titre du commit" -m "Description détaillée des changements effectués"

# Modifier le dernier commit (avant push)
git commit --amend
```

## 🔄 Commandes Courantes

### Voir l'historique
```bash
# Historique simple
git log --oneline

# Historique détaillé
git log

# Historique graphique
git log --graph --oneline --all

# Historique des 5 derniers commits
git log -5
```

### Annuler des changements

```bash
# Annuler les modifications d'un fichier (avant add)
git checkout -- app.py

# Retirer un fichier du staging (après add, avant commit)
git reset app.py

# Annuler le dernier commit (garder les modifications)
git reset --soft HEAD~1

# Annuler le dernier commit (supprimer les modifications)
git reset --hard HEAD~1
```

### Branches

```bash
# Créer une nouvelle branche
git branch feature-nouvelle-fonctionnalite

# Changer de branche
git checkout feature-nouvelle-fonctionnalite

# Créer et changer de branche en une commande
git checkout -b feature-nouvelle-fonctionnalite

# Lister les branches
git branch

# Fusionner une branche dans main
git checkout main
git merge feature-nouvelle-fonctionnalite

# Supprimer une branche
git branch -d feature-nouvelle-fonctionnalite
```

## 🌐 Travailler avec GitHub/GitLab

### Première connexion à un repository distant

```bash
# Ajouter un remote
git remote add origin https://github.com/username/quizai.git

# Vérifier les remotes
git remote -v

# Pousser le code pour la première fois
git push -u origin main
```

### Push et Pull

```bash
# Pousser vos commits
git push

# Pousser une branche spécifique
git push origin feature-branch

# Récupérer les changements
git pull

# Récupérer sans merger
git fetch
```

### Cloner un repository

```bash
# Cloner votre projet
git clone https://github.com/username/quizai.git

# Cloner dans un dossier spécifique
git clone https://github.com/username/quizai.git mon-dossier
```

## 🔐 Fichiers à Ne Jamais Commiter

Le fichier `.gitignore` protège déjà ces fichiers:

- ❌ `.env` - Clés API et secrets
- ❌ `__pycache__/` - Fichiers Python compilés
- ❌ `venv/` - Environnement virtuel
- ❌ `.streamlit/secrets.toml` - Secrets Streamlit
- ❌ `*.log` - Fichiers de logs
- ❌ `*.db` - Bases de données locales

## 📋 Exemples de Messages de Commit

### Format Recommandé
```
Type: Description courte (50 caractères max)

Description détaillée si nécessaire (72 caractères par ligne)

- Point 1
- Point 2
```

### Types Courants
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage, style
- `refactor:` Refactorisation du code
- `test:` Ajout de tests
- `chore:` Maintenance, configuration

### Exemples
```bash
git commit -m "feat: Add support for Groq API provider"

git commit -m "fix: Resolve JSON parsing error in quiz generation"

git commit -m "docs: Update README with installation instructions"

git commit -m "refactor: Improve error handling in AI generator"

git commit -m "style: Format code with Black formatter"
```

## 🚀 Workflow Complet pour une Nouvelle Fonctionnalité

```bash
# 1. Créer une branche
git checkout -b feature-export-quiz-pdf

# 2. Développer la fonctionnalité
# ... faire vos modifications ...

# 3. Vérifier les changements
git status
git diff

# 4. Ajouter les fichiers
git add pages/2_📝_Generate_Quiz.py utils/pdf_exporter.py

# 5. Commiter
git commit -m "feat: Add PDF export functionality for quizzes"

# 6. Pousser la branche
git push -u origin feature-export-quiz-pdf

# 7. Créer une Pull Request sur GitHub/GitLab

# 8. Après merge, revenir sur main et mettre à jour
git checkout main
git pull

# 9. Supprimer la branche locale
git branch -d feature-export-quiz-pdf
```

## 🛠️ Commandes Utiles

### Sauvegarder temporairement des modifications
```bash
# Mettre de côté les modifications
git stash

# Lister les stash
git stash list

# Récupérer les modifications
git stash pop

# Appliquer un stash spécifique
git stash apply stash@{0}
```

### Nettoyer le repository
```bash
# Supprimer les fichiers non trackés
git clean -n  # Voir ce qui sera supprimé
git clean -f  # Supprimer

# Supprimer aussi les dossiers
git clean -fd
```

### Tags (versions)
```bash
# Créer un tag
git tag v1.0.0

# Tag avec message
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"

# Lister les tags
git tag

# Pousser les tags
git push --tags
```

## 📊 Statistiques du Repository

```bash
# Nombre de commits
git rev-list --count HEAD

# Nombre de lignes par auteur
git log --author="Your Name" --pretty=tformat: --numstat | \
  awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }'

# Fichiers les plus modifiés
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10
```

## 🆘 Situations d'Urgence

### J'ai commité par erreur un fichier .env avec des secrets!

```bash
# 1. Retirer le fichier de l'historique Git
git rm --cached .env

# 2. S'assurer qu'il est dans .gitignore
echo ".env" >> .gitignore

# 3. Commiter
git commit -m "chore: Remove .env from repository"

# 4. ⚠️ IMPORTANT: Changer TOUTES les clés API exposées!
```

### J'ai fait un commit sur la mauvaise branche

```bash
# 1. Créer une branche depuis ce commit
git branch correct-branch

# 2. Annuler le commit sur la branche actuelle
git reset --hard HEAD~1

# 3. Aller sur la bonne branche
git checkout correct-branch
```

### Je veux annuler un push public

```bash
# ⚠️ À utiliser avec précaution!
# Créer un commit qui annule les changements
git revert HEAD

# Pousser
git push
```

## 📖 Ressources

- **Documentation Git**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Learn Git Branching**: https://learngitbranching.js.org/

## 💡 Bonnes Pratiques

1. ✅ Faire des commits fréquents et atomiques
2. ✅ Écrire des messages de commit descriptifs
3. ✅ Utiliser des branches pour les fonctionnalités
4. ✅ Tester avant de commiter
5. ✅ Faire un pull avant de pousser
6. ✅ Ne jamais commiter de secrets/clés API
7. ✅ Utiliser .gitignore correctement
8. ✅ Faire des revues de code (Pull Requests)

---

**Astuce**: Créez des alias Git pour les commandes fréquentes:

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --graph --oneline --all"
```

Maintenant vous pouvez utiliser: `git st` au lieu de `git status`
