## 🚀 Git Quick Reference - QuizAI Project

### Daily Workflow
```bash
# Check what's changed
git status

# Add changes
git add .

# Commit
git commit -m "type: description"

# Push to GitHub
git push
```

### Common Commands
```bash
git log --oneline              # View history
git diff                       # See changes
git branch                     # List branches
git checkout -b feature-name   # New branch
git pull                       # Get updates
```

### Emergency
```bash
git reset --soft HEAD~1        # Undo last commit (keep changes)
git checkout -- filename       # Discard changes in file
git stash                      # Save work temporarily
```

### Commit Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code improvement
- `style:` Formatting
- `test:` Tests
- `chore:` Maintenance

### ⚠️ Never Commit
- `.env` files
- API keys
- Passwords
- Local config files

✅ Already protected by `.gitignore`
