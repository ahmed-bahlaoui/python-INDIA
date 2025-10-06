"""
Script pour changer facilement de provider AI
"""

import os
from pathlib import Path


def update_env_provider(provider: str, api_key: str = ""):
    """Met à jour le provider dans le fichier .env"""
    env_path = Path(__file__).parent / ".env"

    # Lire le fichier .env
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Modifier les lignes
    new_lines = []
    provider_updated = False

    for line in lines:
        if line.startswith("AI_PROVIDER="):
            new_lines.append(f"AI_PROVIDER={provider}\n")
            provider_updated = True
        else:
            new_lines.append(line)

    # Si AI_PROVIDER n'existe pas, l'ajouter
    if not provider_updated:
        new_lines.insert(0, f"AI_PROVIDER={provider}\n")

    # Ajouter la clé API si fournie
    if api_key:
        key_name = f"{provider.upper()}_API_KEY"
        key_line = f"{key_name}={api_key}\n"

        # Vérifier si la clé existe déjà
        key_exists = False
        for i, line in enumerate(new_lines):
            if line.startswith(f"{key_name}="):
                new_lines[i] = key_line
                key_exists = True
                break

        # Si la clé n'existe pas, l'ajouter
        if not key_exists:
            new_lines.append(f"\n{key_line}")

    # Écrire le fichier
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✅ Provider changé vers: {provider}")
    if api_key:
        print(f"✅ Clé API mise à jour")
    print("\n⚠️  Redémarrez Streamlit pour appliquer les changements!")


def main():
    print("=" * 60)
    print("🔧 Configuration du Provider AI")
    print("=" * 60)
    print("\nProviders disponibles:")
    print("1. groq       - Gratuit, Rapide (RECOMMANDÉ)")
    print("2. deepseek   - Payant, Bon rapport qualité/prix")
    print("3. openai     - Payant, Haute qualité")
    print("4. ollama     - Gratuit, Local (nécessite installation)")
    print("5. together   - Payant, Bons modèles")

    choice = input("\nChoisissez un provider (1-5): ").strip()

    providers = {
        "1": "groq",
        "2": "deepseek",
        "3": "openai",
        "4": "ollama",
        "5": "together",
    }

    provider = providers.get(choice)

    if not provider:
        print("❌ Choix invalide!")
        return

    if provider != "ollama":
        api_key = input(
            f"\nEntrez votre clé API {provider.upper()} (laissez vide pour garder l'actuelle): "
        ).strip()
    else:
        api_key = ""
        print("\n💡 Pour Ollama, assurez-vous que le service est lancé:")
        print("   ollama serve")

    update_env_provider(provider, api_key)

    print("\n" + "=" * 60)
    print("🎉 Configuration terminée!")
    print("=" * 60)

    if provider == "groq" and not api_key:
        print("\n⚠️  N'oubliez pas d'obtenir votre clé API gratuite:")
        print("   👉 https://console.groq.com/keys")


if __name__ == "__main__":
    main()
