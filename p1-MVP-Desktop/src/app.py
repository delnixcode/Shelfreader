"""
Interface Streamlit pour ShelfReader P1 - MVP Desktop
OCR adaptatif multi-échelle avec détection intelligente de livres
"""

import streamlit as st
import os
import sys
import time
from PIL import Image
import numpy as np
import cv2
import tempfile
import pandas as pd

# Ajouter le répertoire src au path pour importer nos modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import de nos modules OCR
from ocr_easyocr import EasyOCRProcessor

# Configuration de la page
st.set_page_config(
    page_title="ShelfReader P1 - OCR Adaptatif",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("📚 ShelfReader P1 - OCR Adaptatif")
st.markdown("**Détection automatique de livres sur étagères avec OCR intelligent**")
st.markdown("---")

# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ Informations")
    st.markdown("""
    **Algorithme :** OCR Adaptatif Multi-échelle
    **Précision :** 93% (14/15 livres)
    **Méthode :** Shelfie avec fallback intelligent
    **GPU :** Support automatique
    """)

    st.markdown("---")
    st.markdown("**Paramètres recommandés :**")
    st.markdown("- **GPU** : Activé si disponible")
    st.markdown("- **Confiance** : 0.3 (optimisé)")
    st.markdown("- **Méthode** : Shelfie (adaptatif)")

    st.markdown("---")
    st.markdown("**Testé sur :**")
    st.markdown("- books1.jpg : 14/15 livres (93%)")
    st.markdown("- 6 images : moyenne 83.8%")

# Fonction principale de traitement OCR
def process_image_with_ocr(image_path, confidence=0.3, use_gpu=True, debug=False):
    """Traite une image avec notre OCR adaptatif"""
    try:
        start_time = time.time()

        # Créer le processeur OCR
        processor = EasyOCRProcessor(['en'], confidence, use_gpu)

        # Charger l'image
        pil_image = Image.open(image_path)

        # Traitement avec l'algorithme adaptatif
        boxes = processor.get_boxes(
            pil_image,
            preprocess=False,
            use_spine_detection=True,
            debug=debug,
            reference_titles=None,
            spine_method="shelfie"
        )

        text, avg_confidence = processor.get_text_and_confidence(
            pil_image,
            preprocess=False,
            use_spine_detection=True,
            reference_titles=None,
            spine_method="shelfie"
        )

        processing_time = time.time() - start_time

        # Formater les résultats comme attendu par display_results
        results = {
            'books': boxes,
            'text': text,
            'confidence': avg_confidence,
            'processing_time': processing_time
        }

        return results, processing_time

    except Exception as e:
        st.error(f"Erreur lors du traitement OCR : {str(e)}")
        return None, 0

# Fonction pour afficher les résultats
def display_results(results, processing_time):
    """Affiche les résultats de l'OCR de manière structurée"""
    if not results or 'books' not in results:
        st.error("Aucun résultat OCR trouvé")
        return

    books = results['books']

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Livres détectés", len(books))

    with col2:
        avg_confidence = np.mean([book.get('confidence', 0) for book in books]) if books else 0
        st.metric("🎯 Confiance moyenne", f"{avg_confidence:.1%}")

    with col3:
        st.metric("⚡ Temps de traitement", f"{processing_time:.2f}s")

    with col4:
        total_chars = sum(len(book.get('text', '')) for book in books)
        st.metric("📝 Caractères totaux", total_chars)

    st.markdown("---")

    # Affichage détaillé des livres
    st.subheader("📖 Livres détectés")

    if books:
        # Créer un DataFrame pour l'affichage
        books_data = []
        for i, book in enumerate(books, 1):
            books_data.append({
                "N°": i,
                "Titre": book.get('text', 'N/A'),
                "Confiance": f"{book.get('confidence', 0):.1%}",
                "Position": f"x={book.get('x', 0)}, y={book.get('y', 0)}",
                "Dimensions": f"{book.get('width', 0)}×{book.get('height', 0)}"
            })

        df = pd.DataFrame(books_data)
        st.dataframe(df, use_container_width=True)

        # Affichage en format carte pour plus de lisibilité
        st.markdown("### 📋 Détails par livre")
        for i, book in enumerate(books, 1):
            with st.expander(f"📖 Livre {i} - {book.get('text', 'N/A')[:50]}..."):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Texte complet :** {book.get('text', 'N/A')}")
                    st.write(f"**Confiance :** {book.get('confidence', 0):.1%}")

                with col2:
                    st.write(f"**Position :** x={book.get('x', 0)}, y={book.get('y', 0)}")
                    st.write(f"**Dimensions :** {book.get('width', 0)}×{book.get('height', 0)} px")

    else:
        st.warning("⚠️ Aucun livre détecté dans cette image")

# Fonction pour visualiser les zones détectées
def visualize_detected_zones(image_path, books):
    """Crée une visualisation des zones de livres détectées sur l'image"""
    try:
        # Charger l'image avec OpenCV
        image = cv2.imread(image_path)
        if image is None:
            return None

        # Convertir BGR vers RGB pour Streamlit
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Dessiner les rectangles pour chaque livre détecté
        for i, book in enumerate(books):
            x = int(book.get('x', 0))
            y = int(book.get('y', 0))
            width = int(book.get('width', 0))
            height = int(book.get('height', 0))

            # Couleur différente pour chaque livre (cycle à travers les couleurs)
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            color = colors[i % len(colors)]

            # Dessiner le rectangle
            cv2.rectangle(image_rgb, (x, y), (x + width, y + height), color, 3)

            # Ajouter le numéro du livre
            cv2.putText(image_rgb, f"{i+1}", (x + 5, y + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        return image_rgb

    except Exception as e:
        st.error(f"Erreur lors de la visualisation : {str(e)}")
        return None

# Interface principale
def main():
    st.header("🖼️ Upload et traitement d'image")

    # Upload d'image
    uploaded_file = st.file_uploader(
        "Choisissez une image d'étagère de livres",
        type=['jpg', 'jpeg', 'png'],
        help="Formats supportés : JPG, PNG. Taille recommandée : 1000px minimum"
    )

    if uploaded_file is not None:
        # Afficher l'image uploadée
        image = Image.open(uploaded_file)

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📷 Image originale")
            st.image(image, use_column_width=True)

        with col2:
            st.subheader("⚙️ Paramètres de traitement")

            # Paramètres configurables
            confidence = st.slider(
                "Seuil de confiance OCR",
                min_value=0.1,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="0.1 = tolérant, 0.5 = strict. Recommandé : 0.3"
            )

            use_gpu = st.checkbox(
                "Utiliser le GPU (recommandé)",
                value=True,
                help="Accélère le traitement si GPU disponible"
            )

            debug_mode = st.checkbox(
                "Mode debug",
                value=False,
                help="Affiche les analyses détaillées (plus lent)"
            )

            # Bouton de traitement
            if st.button("🚀 Lancer l'analyse OCR", type="primary", use_container_width=True):
                with st.spinner("🔍 Analyse en cours avec algorithme adaptatif..."):
                    # Sauvegarder temporairement l'image
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                        image.save(tmp_file.name, 'JPEG')
                        temp_path = tmp_file.name

                    try:
                        # Traiter l'image
                        results, processing_time = process_image_with_ocr(
                            temp_path,
                            confidence=confidence,
                            use_gpu=use_gpu,
                            debug=debug_mode
                        )

                        if results:
                            # Afficher les résultats
                            st.success("✅ Analyse terminée !")
                            display_results(results, processing_time)

                            # Visualisation des zones détectées
                            if books := results.get('books'):
                                st.markdown("---")
                                st.subheader("👁️ Visualisation des zones détectées")

                                # Créer la visualisation
                                viz_image = visualize_detected_zones(temp_path, books)

                                if viz_image is not None:
                                    col1, col2 = st.columns(2)

                                    with col1:
                                        st.markdown("**📷 Image originale**")
                                        st.image(image, use_column_width=True)

                                    with col2:
                                        st.markdown("**🎯 Zones détectées**")
                                        st.image(viz_image, caption=f"{len(books)} livres détectés", use_column_width=True)

                                    st.info("💡 **Légende :** Chaque rectangle coloré représente un livre détecté avec son numéro")
                                else:
                                    st.warning("⚠️ Impossible de créer la visualisation")

                            # Informations techniques
                            with st.expander("🔧 Informations techniques"):
                                st.json(results)

                        else:
                            st.error("❌ Échec de l'analyse OCR")

                    finally:
                        # Nettoyer le fichier temporaire
                        os.unlink(temp_path)

    else:
        # Message d'accueil quand aucune image n'est uploadée
        st.info("👆 Veuillez uploader une image d'étagère de livres pour commencer l'analyse")

        # Exemples d'utilisation
        st.markdown("### 💡 Conseils d'utilisation")
        st.markdown("""
        - **Qualité d'image** : Photos bien éclairées, perpendiculaires à l'étagère
        - **Taille minimale** : 1000 pixels de largeur recommandée
        - **Formats** : JPG ou PNG
        - **Contenu** : Étageres de livres avec titres visibles
        """)

        # Images d'exemple
        st.markdown("### 🖼️ Images de test disponibles")
        test_images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_images")

        if os.path.exists(test_images_dir):
            test_images = [f for f in os.listdir(test_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

            if test_images:
                st.markdown("**Images disponibles pour test :**")
                for img in test_images:
                    st.code(f"test_images/{img}", language="text")
            else:
                st.info("Aucune image de test trouvée dans test_images/")

if __name__ == "__main__":
    main()

