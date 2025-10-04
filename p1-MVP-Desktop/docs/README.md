# 📚 ShelfReader# 📚 ShelfReader



Application pour détecter et rechercher des livres sur une étagère.Application pour détecter et rechercher des livres sur une étagère.



## 📱 Usage mobile principal## 📱 Usage mobile principal



1. L'utilisateur ouvre l'app mobile avec la caméra (flux vidéo continu).1. L'utilisateur ouvre l'app mobile avec la caméra (flux vidéo continu).

2. Il saisit un titre de livre ou une thématique (ex : "Python", "Dune").2. Il saisit un titre de livre ou une thématique (ex : "Python", "Dune").

3. L'app analyse en continu le flux vidéo de l'étagère.3. L'app analyse en continu le flux vidéo de l'étagère.

4. L'OCR détecte en temps réel tous les titres de livres présents dans le flux.4. L'OCR détecte en temps réel tous les titres de livres présents dans le flux.

5. Pour chaque titre détecté, l'app interroge l'API Open Library pour récupérer les sujets/thématiques.5. Pour chaque titre détecté, l'app interroge l'API Open Library pour récupérer les sujets/thématiques.

6. L'app compare les sujets/thématiques des livres détectés avec la recherche de l'utilisateur.6. L'app compare les sujets/thématiques des livres détectés avec la recherche de l'utilisateur.

7. Les livres correspondants sont mis en évidence sur l'image (bounding box, surlignage) en temps réel.7. Les livres correspondants sont mis en évidence sur l'image (bounding box, surlignage) en temps réel.



## 🎯 Fonctionnalités## 🎯 Fonctionnalités



1. 📸 Uploader une photo d'étagère1. 📸 Uploader une photo d'étagère

2. 🔍 Détecter les titres de livres (OCR)2. 🔍 Détecter les titres de livres (OCR)

3. 🌐 Récupérer les métadonnées (Open Library API)3. 🌐 Récupérer les métadonnées (Open Library API)

4. 🎨 Afficher les résultats dans une interface web4. 🎨 Afficher les résultats dans une interface web



## 📂 Structure du projet## 📂 Structure du projet



Consulte [STRUCTURE.md](STRUCTURE.md) pour la structure complète.Consulte [STRUCTURE.md](STRUCTURE.md) pour la structure complète.



## 🚀 Installation## 🚀 Installation



```bash```bash

# Cloner le projet# Cloner le projet

git clone <url>git clone <url>

cd ShelfReadercd ShelfReader



# Installer les dépendances# Installer les dépendances

pip install -r requirements.txtpip install -r requirements.txt

``````



## 📖 Documentation## 📖 Documentation



Consulte [docs/LEARNING.md](LEARNING.md) pour la documentation complète.Consulte [docs/LEARNING.md](docs/LEARNING.md) pour la documentation complète.



## 🧪 Tester l'API Client (Phase 1)## 🧪 Tester l'API Client (Phase 1)



```bash```bash

python src/api_client.pypython src/api_client.py

``````



## 🎯 Phases du projet## 🎯 Phases du projet



- ✅ **Phase 1** : Client API Open Library → `src/api_client.py`- ✅ **Phase 1** : Client API Open Library → `src/api_client.py`

- ⏳ **Phase 2** : OCR Tesseract → `src/ocr_processor.py`- ⏳ **Phase 2** : OCR Tesseract → `src/ocr_processor.py`

- ⏳ **Phase 3** : Interface Streamlit → `src/app.py`- ⏳ **Phase 3** : Interface Streamlit → `src/app.py`

- ⏳ **Phase 4** : Tests → `tests/`- ⏳ **Phase 4** : Tests → `tests/`



## 📝 Prochaines étapes## 📝 Prochaines étapes



1. Teste le client API : `python src/api_client.py`1. Teste le client API : `python src/api_client.py`

2. Lis la doc : [docs/learning/api_client.md](learning/api_client.md)2. Lis la doc : [docs/learning/api_client.md](docs/learning/api_client.md)
3. Passe à la Phase 2 : OCR