"""
Composant de visualisation - ShelfReader P1

Ce module gère la création et l'affichage des visualisations des zones
de livres détectées sur les images, avec bounding boxes colorées.
"""

import streamlit as st
import cv2
import numpy as np
from typing import Dict, List, Optional, Any
from PIL import Image


def visualize_detected_zones(image_path: str, books: List[Dict]) -> Optional[np.ndarray]:
    """
    Crée une visualisation des zones de livres détectées sur l'image.

    Cette fonction dessine des rectangles colorés autour de chaque livre
    détecté et ajoute des numéros pour identifier facilement les zones.

    Args:
        image_path (str): Chemin vers l'image originale
        books (List[Dict]): Liste des livres détectés avec coordonnées

    Returns:
        Optional[np.ndarray]: Image avec visualisations (RGB) ou None si erreur

    Note:
        Les couleurs sont cyclées pour différencier les livres.
        Le numéro de chaque livre est affiché dans le rectangle supérieur-gauche.
    """
    try:
        # Charger l'image avec OpenCV
        image = cv2.imread(image_path)
        if image is None:
            st.error(f"Impossible de charger l'image : {image_path}")
            return None

        # Convertir BGR vers RGB pour Streamlit
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Palette de couleurs pour différencier les livres
        colors = [
            (255, 0, 0),    # Rouge
            (0, 255, 0),    # Vert
            (0, 0, 255),    # Bleu
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Jaune
        ]

        # Dessiner les rectangles pour chaque livre détecté
        for i, book in enumerate(books):
            # Coordonnées du rectangle
            x = int(book.get('x', 0))
            y = int(book.get('y', 0))
            width = int(book.get('width', 0))
            height = int(book.get('height', 0))

            # Sélection de la couleur (cycle à travers la palette)
            color = colors[i % len(colors)]

            # Dessiner le rectangle
            cv2.rectangle(
                image_rgb,
                (x, y),           # Coin supérieur-gauche
                (x + width, y + height),  # Coin inférieur-droit
                color,
                3                  # Épaisseur de la ligne
            )

            # Ajouter le numéro du livre
            cv2.putText(
                image_rgb,
                str(i + 1),       # Numéro du livre (1-indexé)
                (x + 5, y + 30),  # Position du texte
                cv2.FONT_HERSHEY_SIMPLEX,
                1,                 # Taille de la police
                color,             # Couleur du texte
                2                  # Épaisseur du texte
            )

        return image_rgb

    except Exception as e:
        st.error(f"Erreur lors de la visualisation : {str(e)}")
        return None


def display_visualization(image_path: str, books: List[Dict],
                         title: str = "Zones détectées") -> None:
    """
    Affiche la visualisation des zones détectées dans Streamlit.

    Args:
        image_path (str): Chemin vers l'image originale
        books (List[Dict]): Liste des livres détectés
        title (str): Titre de la section de visualisation
    """
    st.subheader(f"👁️ {title}")

    if books:
        # Générer l'image visualisée
        viz_image = visualize_detected_zones(image_path, books)

        if viz_image is not None:
            # Afficher l'image avec légende
            st.image(
                viz_image,
                caption=f"{len(books)} livres détectés",
                use_container_width=True
            )

            # Légende explicative
            st.info("💡 **Légende :** Chaque rectangle coloré représente un livre détecté avec son numéro")

        else:
            st.warning("⚠️ Impossible de créer la visualisation")
    else:
        st.warning("⚠️ Aucun livre détecté à visualiser")


def display_comparison_visualizations(results_dict: Dict[str, Dict],
                                    selected_engines: List[str],
                                    image_path: str) -> None:
    """
    Affiche les visualisations côte à côte pour la comparaison des moteurs.

    Args:
        results_dict (Dict[str, Dict]): Résultats par moteur OCR
        selected_engines (List[str]): Liste des moteurs comparés
        image_path (str): Chemin vers l'image originale
    """
    st.markdown("## Visualisation des bounding boxes par moteur")

    # Créer les colonnes pour l'affichage côte à côte
    img_cols = st.columns(len(selected_engines))

    for idx, engine in enumerate(selected_engines):
        with img_cols[idx]:
            books = results_dict[engine].get('books', [])
            if books:
                # Générer la visualisation pour ce moteur
                viz_image = visualize_detected_zones(image_path, books)
                if viz_image is not None:
                    st.image(viz_image, caption=f"{engine}", use_container_width=True)
                else:
                    st.error(f"Erreur de visualisation pour {engine}")
            else:
                st.warning(f"{engine}: Aucun livre détecté")


def display_book_details(enriched_books: List[Dict], image_path: str) -> None:
    """
    Affiche les détails détaillés de chaque livre détecté.

    Args:
        enriched_books (List[Dict]): Livres enrichis avec Open Library
        image_path (str): Chemin vers l'image pour la visualisation
    """
    st.markdown("### 📋 Détails par livre")

    for i, book in enumerate(enriched_books, 1):
        enriched = book.get('enriched', False)

        with st.expander(f"📖 Livre {i} - {book.get('text', 'N/A')[:50]}..."):
            # Informations OCR de base
            st.write(f"**Texte OCR :** {book.get('text', 'N/A')}")
            st.write(f"**Confiance :** {book.get('confidence', 0):.1%}")

            # Informations Open Library si enrichi
            if enriched:
                st.write(f"**Titre Open Library :** {book.get('openlibrary_title', 'N/A')}")
                st.write(f"**Auteur :** {book.get('openlibrary_author', 'N/A')}")
                st.write(f"**Année :** {book.get('openlibrary_year', 'N/A')}")

                # Afficher la couverture si disponible
                cover_url = book.get('openlibrary_cover_url')
                if cover_url:
                    st.image(cover_url, width=100, caption="Couverture")
                else:
                    st.write("🖼️ *Pas de couverture disponible*")

                # Lien vers Open Library
                ol_url = book.get('openlibrary_url')
                if ol_url:
                    st.markdown(f"[🔗 Voir sur Open Library]({ol_url})")
            else:
                st.write("📚 *Informations Open Library non disponibles*")