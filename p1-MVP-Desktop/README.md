# 🏗️ **P1 - MVP Desktop**
## OCR + API + Interface Web

**ShelfReader MVP Desktop** - Extraire du texte des photos de tranches de livres.

### 📁 **Structure**
```
p1-MVP-Desktop/
├── env-p1/              # Environnement virtuel
├── result-ocr/          # Résultats OCR (auto-généré)
├── ocr_easyocr.py       # Script OCR EasyOCR
├── ocr_tesseract.py     # Script OCR Tesseract
├── ocr_trocr.py         # Script OCR TrOCR
├── api_client.py        # Client Open Library
├── app.py               # Interface Streamlit
├── test_images/         # Images de test
├── requirements.txt     # Dépendances
└── README.md           # Cette doc
```

### 🚀 **Installation**
```bash
cd p1-MVP-Desktop
source env-p1/bin/activate
pip install -r requirements.txt
```

### � **Utilisation**

#### **Scripts OCR individuels**
Chaque moteur OCR peut être utilisé indépendamment. **Les résultats sont automatiquement sauvegardés dans le dossier `result-ocr/`**.

##### **EasyOCR (Recommandé - GPU/CPU)**
```bash
# Test de base avec GPU (recommandé)
python ocr_easyocr.py test_images/books1.jpg --gpu

# Test avec CPU seulement
python ocr_easyocr.py test_images/books1.jpg

# Avec seuil de confiance personnalisé
python ocr_easyocr.py test_images/books1.jpg --gpu --confidence 0.3
```

##### **Tesseract (Rapide - CPU seulement)**
```bash
# Test de base (optimisé pour la vitesse ~1.5s)
python ocr_tesseract.py test_images/books1.jpg

# Avec langue française
python ocr_tesseract.py test_images/books1.jpg --lang fra

# Avec seuil de confiance plus élevé
python ocr_tesseract.py test_images/books1.jpg --confidence 0.5
```

##### **TrOCR (Précis - GPU recommandé)**
```bash
# Test avec GPU (recommandé pour les performances)
python ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.5

# Test CPU (fonctionne mais plus lent)
python ocr_trocr.py test_images/books1.jpg --confidence 0.5

# Avec seuil de confiance plus strict
python ocr_trocr.py test_images/books1.jpg --gpu --confidence 0.7
```

#### **Options communes**
- `--gpu` : Utiliser le GPU (si disponible) - Accélère considérablement EasyOCR et TrOCR
- `--confidence X.X` : Seuil de confiance minimum (0.0 à 1.0) - Défaut: 0.2
  - `0.1` : Très tolérant (beaucoup de résultats, plus de faux positifs)
  - `0.2` : Équilibre (recommandé pour débuter)
  - `0.5` : Strict (moins de résultats, plus précis)
  - `0.7` : Très strict (seulement les meilleurs résultats)
- `--output fichier.txt` : Nom du fichier de sortie (défaut: `[moteur]_results.txt`)

#### **Options spécifiques par moteur**
- **EasyOCR** : `--gpu`, `--confidence`, `--output`
- **Tesseract** : `--lang [eng|fra|deu|...]`, `--confidence`, `--output`
- **TrOCR** : `--gpu`, `--confidence`, `--output`

### �️ **Interface Web**
```bash
streamlit run app.py
```

### 📁 **Résultats**
Les résultats sont sauvegardés automatiquement dans `result-ocr/`.

**Format des fichiers de résultats :**
```
=== RÉSULTATS OCR - test_images/books1.jpg ===
Date: 2025-10-04 12:34:56
Nombre de textes détectés: 11
Confiance moyenne: 0.885

TEXTE COMPLET:
[Tous les textes détectés séparés par |]

DÉTAIL PAR LIVRE:
--- Livre 1 ---
Confiance: 0.703
Texte: [Titre du livre 1]
--- Livre 2 ---
...
```

### 🧪 **Tests**
```bash
# Activer l'environnement virtuel d'abord
source env-p1/bin/activate

# Lancer tous les tests
python -m pytest tests/

# Tests avec couverture
python -m pytest tests/ --cov=. --cov-report=html
```

### 📊 **Comparaison des moteurs OCR**

| Moteur | GPU Support | Vitesse | Précision | Usage recommandé |
|--------|-------------|---------|-----------|------------------|
| **EasyOCR** | ✅ Excellent | 🚀 ~3-5s | 🟢🟢 Excellente | **Défaut - Tous usages** |
| **Tesseract** | ❌ Aucun | ⚡ ~1.5s | 🟡 Moyenne | Tests rapides, CPU limité |
| **TrOCR** | ✅ Bon | 🐌 ~8-15s | 🟢 Bonne | Précision maximale |

**📊 Benchmarks sur `test_images/books1.jpg` :**
- **EasyOCR** : 11 livres détectés, confiance 0.885, temps ~3s
- **Tesseract** : 15 textes détectés, confiance 0.733, temps ~1.5s  
- **TrOCR** : 14 textes détectés, confiance 0.807, temps ~12s

