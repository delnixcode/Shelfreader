# 📚 ShelfReader

**Reconnaissance automatique de livres par OCR — Suite multi-projets**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table des matières
- [À propos](#à-propos)
- [Architecture](#architecture)
- [Phases du projet](#phases-du-projet)
- [Démarrage rapide](#démarrage-rapide)
- [Documentation](#documentation)
- [Contribution](#contribution)
- [Licence](#licence)

---

## À propos
ShelfReader est une suite d'applications pour la reconnaissance optique de caractères (OCR) dédiée à l'identification automatique des titres de livres sur étagères. Le projet est découpé en plusieurs phases indépendantes (P1 à P4), chacune avec ses propres objectifs et documentation.

---

## Architecture
```
ShelfReader/
├── p1-OCR-Streamlit/     # Phase 1 : Desktop Streamlit
├── p2-Enhanced-Desktop/  # Phase 2 : Desktop avancé
├── p3-Mobile-Static/     # Phase 3 : Mobile statique
├── p4-Mobile-Real-time/  # Phase 4 : Mobile temps réel
└── shared/               # Ressources communes
```

---

## Phases du projet
| Phase | Dossier | Description | Documentation |
|-------|---------|-------------|---------------|
| P1    | [p1-OCR-Streamlit](./p1-OCR-Streamlit) | MVP Desktop avec Streamlit, 3 moteurs OCR | [README P1](./p1-OCR-Streamlit/README.md) |
| P2    | [p2-Enhanced-Desktop](./p2-Enhanced-Desktop) | Desktop avancé, détection YOLOv8 | [README P2](./p2-Enhanced-Desktop/README.md) |
| P3    | [p3-Mobile-Static](./p3-Mobile-Static) | Application mobile statique | [README P3](./p3-Mobile-Static/README.md) |
| P4    | [p4-Mobile-Real-time](./p4-Mobile-Real-time) | Application mobile temps réel | [README P4](./p4-Mobile-Real-time/README.md) |

---

## Démarrage rapide

```bash
# Cloner le dépôt
git clone https://github.com/delnixcode/Shelfreader.git
cd Shelfreader
```

Pour chaque phase, consulte le README du dossier correspondant pour l'installation et l'utilisation.

---

## Documentation
- Documentation technique et guides dans chaque dossier de phase
- Ressources partagées dans `shared/docs/`

---

## Contribution
Les contributions sont les bienvenues sur toutes les phases !
- Ouvre une issue pour discuter d'une amélioration
- Forke le dépôt et propose une Pull Request

---

## Licence
Ce projet est sous licence MIT — voir le fichier [LICENSE](LICENSE).

---

*Développé avec ❤️ pour les amoureux des livres*
