# ShelfReader P1 - Application Web de Démonstration

## 🚀 Démarrage rapide

1. **Activer l'environnement virtuel :**
   ```bash
   source env-p1/bin/activate
   ```

2. **Lancer l'application web :**
   ```bash
   ./run_streamlit.sh
   ```

3. **Ouvrir dans votre navigateur :**
   - http://localhost:8501

## 📸 Test avec une image d'exemple

L'application contient déjà des images de test dans le dossier `test_images/` :
- `books1.jpg` : 15 livres attendus, 14 détectés (93% précision)
- `books2.jpg` à `books6.png` : Images supplémentaires pour test

## 🎯 Fonctionnalités

- **Upload d'image** : Glissez-déposez ou sélectionnez un fichier
- **Paramètres ajustables** : Seuil de confiance, GPU, mode debug
- **Visualisation** : Aperçu des zones détectées en couleur
- **Résultats détaillés** : Liste complète des livres avec métriques
- **Export automatique** : Résultats sauvegardés dans `result-ocr/`

## 💡 Conseils d'utilisation

- **Qualité d'image** : Photos bien éclairées, perpendiculaires à l'étagère
- **Taille minimale** : 1000 pixels de largeur recommandée
- **Formats supportés** : JPG, PNG
- **GPU** : Activez-le pour des analyses 3x plus rapides

## 🔧 Dépannage

Si l'application ne démarre pas :
```bash
# Vérifier l'installation
pip install -r requirements.txt

# Relancer
./run_streamlit.sh
```

## 📊 Résultats attendus

Avec `books1.jpg` et les paramètres par défaut :
- **14 livres détectés** (sur 15 attendus)
- **93.3% de confiance moyenne**
- **Temps de traitement** : ~15-25 secondes (CPU) ou ~5-10 secondes (GPU)

---
*Application créée avec l'algorithme OCR adaptatif multi-échelle*