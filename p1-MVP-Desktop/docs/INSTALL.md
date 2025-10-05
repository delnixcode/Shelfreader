# Installation ShelfReader P1 - Desktop

## Prérequis
- Python 3.8+
- pip
- Un GPU (optionnel, recommandé)

## Étapes

### 1. Cloner le dépôt
```bash
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader/p1-MVP-Desktop
```

### 2. Activer l'environnement virtuel
```bash
# Linux/macOS
source env-p1/bin/activate
# Windows
env-p1\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
streamlit run src/app.py
```

Ouvrir http://localhost:8501 dans votre navigateur.
