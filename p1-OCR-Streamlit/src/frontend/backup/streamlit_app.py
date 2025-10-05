"""
Interface Streamlit pour ShelfReader P1 - OCR Streamlit
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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import de nos modules OCR
from engines.easyocr_engine import EasyOCRProcessor
from engines.tesseract_engine import TesseractOCRProcessor
from engines.trocr_engine import TrOCRProcessor
from services.openlibrary_client import OpenLibraryClient

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


# Sidebar navigation always at the top
with st.sidebar:
    page = st.radio(
        "Navigation",
        ["Analyse OCR", "Comparaison OCR"],
        index=0
    )
    st.markdown("---")
    st.header("ℹ️ Informations")
    st.markdown("**Algorithme :** OCR Adaptatif Multi-échelle")
    st.markdown("**Précision :** 93% (14/15 livres)")
    st.markdown("**GPU :** Support automatique")
    st.markdown("**Enrichissement :** Open Library intégré")
    st.markdown("---")
    st.markdown("**Paramètres recommandés :**")
    st.markdown("- **GPU** : Activé si disponible")
    st.markdown("- **Confiance** : 0.3 (optimisé)")
    st.markdown("---")
    st.markdown("**Testé sur :**")
    st.markdown("- books1.jpg : 14/15 livres (93%)")
    st.markdown("- 6 images : moyenne 83.8%")

# Fonction principale de traitement OCR
def process_image_with_ocr(image_path, confidence=0.3, use_gpu=True, debug=False):
    """Traite une image avec notre OCR adaptatif"""
    try:
        start_time = time.time()

        # Sélection du moteur OCR
        ocr_engine = st.session_state.get('ocr_engine', 'EasyOCR')
        if ocr_engine == 'EasyOCR':
            processor = EasyOCRProcessor(['en'], confidence, use_gpu)
            st.markdown("**GPU :** Support automatique")
            st.markdown("**Enrichissement :** Open Library intégré")
            boxes = processor.get_boxes(
                pil_image,
                preprocess=False,
                use_spine_detection=True,
                debug=debug,
                reference_titles=None,
            )
            text, avg_confidence = processor.get_text_and_confidence(
                pil_image,
                preprocess=False,
                use_spine_detection=True,
                reference_titles=None,
                spine_method="shelfie"
            )
        elif ocr_engine == 'Tesseract':
            processor = TesseractOCRProcessor('eng', confidence, use_gpu)
            pil_image = Image.open(image_path)
            # Tesseract retourne des boxes similaires
            boxes = processor.get_boxes(pil_image)
            text, avg_confidence = processor.get_text_and_confidence(pil_image)
        elif ocr_engine == 'TrOCR':
            processor = TrOCRProcessor(['en'], confidence, use_gpu)
            pil_image = Image.open(image_path)
            boxes = processor.get_boxes(pil_image)
            text, avg_confidence = processor.get_text_and_confidence(pil_image)
        else:
            st.error(f"Moteur OCR inconnu : {ocr_engine}")
            return None, 0

        processing_time = time.time() - start_time
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
def display_results(results, processing_time, enriched_books=None):
    """Affiche les résultats de l'OCR de manière structurée"""
    if not results or 'books' not in results:
        st.error("Aucun résultat OCR trouvé")
        return

    books = enriched_books if enriched_books else results['books']

    # Affichage pleine largeur pour desktop
    # Métriques principales
    st.subheader("📊 Résultats de l'analyse")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Livres détectés", len(books))

    with col2:
        avg_confidence = np.mean([book.get('confidence', 0) for book in books]) if books else 0
        st.metric("🎯 Confiance moyenne", f"{avg_confidence:.1%}")

    with col3:
        st.metric("⚡ Temps de traitement", f"{processing_time:.2f}s")

    with col4:
        enriched_count = sum(1 for book in books if book.get('enriched', False))
        st.metric("📚 Enrichis Open Library", f"{enriched_count}/{len(books)}")

    st.markdown("---")

    # Affichage détaillé des livres
    st.subheader("📖 Livres détectés")

    if books:
        # Créer un DataFrame pour l'affichage
        books_data = []
        for i, book in enumerate(books, 1):
            enriched = book.get('enriched', False)
            year = book.get('openlibrary_year', 'N/A') if enriched else 'N/A'
            year_str = str(year) if year != 'N/A' else 'N/A'
            ol_url = book.get('openlibrary_url') if enriched else None
            books_data.append({
                "N°": i,
                "Titre OCR": book.get('text', 'N/A'),
                "Titre OL": book.get('openlibrary_title', 'N/A') if enriched else 'Non enrichi',
                "Auteur": book.get('openlibrary_author', 'N/A') if enriched else 'N/A',
                "Année": year_str,
                "Confiance": f"{book.get('confidence', 0):.1%}",
                "Enrichi": "✅" if enriched else "❌",
                "Lien Open Library": ol_url if ol_url else ""
            })

        # Rendre le lien Open Library cliquable dans le tableau
        import html
        def make_link(url):
            if url:
                return f'<a href="{html.escape(url)}" target="_blank">🔗 Open Library</a>'
            return ""

        # Créer une table HTML pour affichage cliquable
        table_html = "<table style='width:100%; border-collapse:collapse;'>"
        # En-têtes
        headers = ["N°", "Titre OCR", "Titre OL", "Auteur", "Année", "Confiance", "Enrichi", "Lien Open Library"]
        table_html += "<tr>" + "".join([f"<th style='border:1px solid #ccc; padding:4px'>{h}</th>" for h in headers]) + "</tr>"
        # Lignes
        for row in books_data:
            table_html += "<tr>"
            for h in headers[:-1]:
                table_html += f"<td style='border:1px solid #ccc; padding:4px'>{html.escape(str(row[h]))}</td>"
            # Lien cliquable
            table_html += f"<td style='border:1px solid #ccc; padding:4px'>{make_link(row['Lien Open Library'])}</td>"
            table_html += "</tr>"
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)


    else:
        st.warning("⚠️ Aucun livre détecté dans cette image")
def enrich_books_with_openlibrary(books, client):
    """Enrichit les résultats OCR avec des informations de Open Library"""
    enriched_books = []

    for book in books:
        text = book.get('text', '').strip()
        if text:
            # Essayer d'enrichir avec Open Library
            enriched_info = client.get_book_info_for_ocr_result(text)

            if enriched_info:
                # Fusionner les informations OCR avec celles de Open Library
                enriched_book = book.copy()
                enriched_book.update({
                    'openlibrary_title': enriched_info.get('title'),
                    'openlibrary_author': enriched_info.get('author'),
                    'openlibrary_year': enriched_info.get('first_publish_year'),
                    'openlibrary_cover_url': enriched_info.get('cover_url'),
                    'openlibrary_url': enriched_info.get('open_library_url'),
                    'openlibrary_description': enriched_info.get('description'),
                    'openlibrary_subjects': enriched_info.get('subjects', []),
                    'enriched': True
                })
                enriched_books.append(enriched_book)
            else:
                # Ajouter le livre OCR sans enrichissement
                book_copy = book.copy()
                book_copy['enriched'] = False
                enriched_books.append(book_copy)
        else:
            book_copy = book.copy()
            book_copy['enriched'] = False
            enriched_books.append(book_copy)

    return enriched_books

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
        image = Image.open(uploaded_file)

        # 1ère ligne : image originale + paramètres
        col_img, col_params = st.columns([1, 1])
        with col_img:
            st.subheader("📷 Image originale")
            st.image(image, use_container_width=True)
        with col_params:
            st.subheader("⚙️ Paramètres de traitement")
            ocr_engine = st.selectbox(
                "Moteur OCR",
                ["EasyOCR", "Tesseract", "TrOCR"],
                index=0,
                help="Choisissez le moteur OCR à utiliser"
            )
            st.session_state['ocr_engine'] = ocr_engine
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
            enrich_with_ol = st.checkbox(
                "Enrichir avec Open Library",
                value=True,
                help="Recherche les métadonnées des livres sur Open Library (nécessite connexion internet)"
            )

        # 2ème ligne : résultats et livres détectés
        st.markdown("---")
        if st.button("🚀 Lancer l'analyse OCR", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyse en cours avec algorithme adaptatif..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    if image.mode == 'RGBA':
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        background.paste(image, mask=image.split()[-1])
                        background.save(tmp_file.name, 'JPEG')
                    else:
                        rgb_image = image.convert('RGB')
                        rgb_image.save(tmp_file.name, 'JPEG')
                    temp_path = tmp_file.name

                try:
                    results, processing_time = process_image_with_ocr(
                        temp_path,
                        confidence=confidence,
                        use_gpu=use_gpu,
                        debug=debug_mode
                    )

                    if results:
                        enriched_books = None
                        if enrich_with_ol and results.get('books'):
                            with st.spinner("🔍 Enrichissement avec Open Library..."):
                                ol_client = OpenLibraryClient(timeout=10)
                                enriched_books = enrich_books_with_openlibrary(results['books'], ol_client)

                        st.success("✅ Analyse terminée !" + (" + Enrichissement OL" if enrich_with_ol else ""))
                        st.markdown("---")

                        # 2ème ligne : résultats et livres détectés (pleine largeur)
                        display_results(results, processing_time, enriched_books)

                        # 3ème ligne : détails et visualisation des zones détectées
                        st.markdown("---")
                        st.subheader("👁️ Visualisation des zones détectées")
                        books = results.get('books')
                        if books:
                            viz_image = visualize_detected_zones(temp_path, books)
                            col_det, col_viz = st.columns([1, 1])
                            with col_det:
                                st.markdown("### 📋 Détails par livre")
                                for i, book in enumerate(enriched_books if enriched_books else books, 1):
                                    enriched = book.get('enriched', False)
                                    with st.expander(f"� Livre {i} - {book.get('text', 'N/A')[:50]}..."):
                                        st.write(f"**Texte OCR :** {book.get('text', 'N/A')}")
                                        st.write(f"**Confiance :** {book.get('confidence', 0):.1%}")
                                        if enriched:
                                            st.write(f"**Titre Open Library :** {book.get('openlibrary_title', 'N/A')}")
                                            st.write(f"**Auteur :** {book.get('openlibrary_author', 'N/A')}")
                                            st.write(f"**Année :** {book.get('openlibrary_year', 'N/A')}")
                                            cover_url = book.get('openlibrary_cover_url')
                                            if cover_url:
                                                st.image(cover_url, width=100, caption="Couverture")
                                            else:
                                                st.write("�️ *Pas de couverture disponible*")
                                            ol_url = book.get('openlibrary_url')
                                            if ol_url:
                                                st.markdown(f"[🔗 Voir sur Open Library]({ol_url})")
                            with col_viz:
                                if viz_image is not None:
                                    st.image(viz_image, caption=f"{len(books)} livres détectés", use_container_width=True)
                                    st.info("💡 **Légende :** Chaque rectangle coloré représente un livre détecté avec son numéro")
                                else:
                                    st.warning("⚠️ Impossible de créer la visualisation")
                        with st.expander("🔧 Informations techniques"):
                            st.json(results)
                    else:
                        st.error("❌ Échec de l'analyse OCR")
                finally:
                    os.unlink(temp_path)
    else:
        st.info("👆 Veuillez uploader une image d'étagère de livres pour commencer l'analyse")
        st.markdown("### 💡 Conseils d'utilisation")
        st.markdown("""
        - **Qualité d'image** : Photos bien éclairées, perpendiculaires à l'étagère
        - **Taille minimale** : 1000 pixels de largeur recommandée
        - **Formats** : JPG ou PNG
        - **Contenu** : Étageres de livres avec titres visibles
        """)


def ocr_comparison_page():
    st.header("📊 Comparaison des moteurs OCR")
    st.markdown("Comparez plusieurs moteurs OCR sur la même image.")

    engines = ["EasyOCR", "Tesseract", "TrOCR"]
    selected_engines = st.multiselect(
        "Sélectionnez les moteurs OCR à comparer",
        options=engines,
        default=["EasyOCR", "Tesseract"],
        help="Choisissez au moins deux moteurs pour la comparaison."
    )
    if len(selected_engines) < 2:
        st.warning("Veuillez sélectionner au moins deux moteurs OCR.")
        return

    uploaded_file = st.file_uploader(
        "Téléchargez une image pour la comparaison",
        type=['jpg', 'jpeg', 'png'],
        help="Formats supportés : JPG, PNG. Taille recommandée : 1000px minimum"
    )
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Image à comparer", use_container_width=True)
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
        if st.button("🚀 Comparer les moteurs OCR", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                if image.mode == 'RGBA':
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    background.save(tmp_file.name, 'JPEG')
                else:
                    rgb_image = image.convert('RGB')
                    rgb_image.save(tmp_file.name, 'JPEG')
                temp_path = tmp_file.name
            try:
                results_dict = {}
                images_with_boxes = {}
                for idx, engine in enumerate(selected_engines):
                    progress_bar.progress(int((idx/len(selected_engines))*100))
                    if engine == "EasyOCR":
                        processor = EasyOCRProcessor(['en'], confidence, use_gpu)
                        pil_image = Image.open(temp_path)
                        boxes = processor.get_boxes(
                            pil_image,
                            preprocess=False,
                            use_spine_detection=True,
                            debug=debug_mode,
                            reference_titles=None,
                        )
                        text, avg_confidence = processor.get_text_and_confidence(
                            pil_image,
                            preprocess=False,
                            use_spine_detection=True,
                            reference_titles=None,
                            spine_method="shelfie"
                        )
                    elif engine == "Tesseract":
                        processor = TesseractOCRProcessor('eng', confidence, use_gpu)
                        pil_image = Image.open(temp_path)
                        boxes = processor.get_boxes(pil_image)
                        text, avg_confidence = processor.get_text_and_confidence(pil_image)
                    elif engine == "TrOCR":
                        processor = TrOCRProcessor(['en'], confidence, use_gpu)
                        pil_image = Image.open(temp_path)
                        boxes = processor.get_boxes(pil_image)
                        text, avg_confidence = processor.get_text_and_confidence(pil_image)
                    else:
                        st.error(f"Moteur OCR inconnu : {engine}")
                        continue
                    results_dict[engine] = {
                        'books': boxes,
                        'text': text,
                        'confidence': avg_confidence,
                        'processing_time': None
                    }
                    # Générer image avec bounding boxes
                    img_cv = cv2.imread(temp_path)
                    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                    for i, book in enumerate(boxes):
                        x = int(book.get('x', 0))
                        y = int(book.get('y', 0))
                        w = int(book.get('width', 0))
                        h = int(book.get('height', 0))
                        color = (255, 0, 0) if engine=="EasyOCR" else (0,255,0) if engine=="Tesseract" else (0,0,255)
                        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), color, 3)
                        cv2.putText(img_rgb, f"{i+1}", (x + 5, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    images_with_boxes[engine] = img_rgb
                progress_bar.progress(100)
                st.success("Comparaison terminée !")

                # Affichage des images avec bounding boxes côte à côte
                st.markdown("## Visualisation des bounding boxes par moteur")
                img_cols = st.columns(len(selected_engines))
                for idx, engine in enumerate(selected_engines):
                    with img_cols[idx]:
                        st.image(images_with_boxes[engine], caption=f"{engine}", use_container_width=True)

                # Display results side-by-side
                st.markdown("## Résultats par moteur")
                cols = st.columns(len(selected_engines))
                for idx, engine in enumerate(selected_engines):
                    with cols[idx]:
                        st.markdown(f"### {engine}")
                        res = results_dict[engine]
                        st.write(f"**Texte OCR :** {res['text']}")
                        st.write(f"**Confiance moyenne :** {res['confidence']:.1%}")
                        st.write(f"**Livres détectés :** {len(res['books'])}")
                        # Table of books
                        if res['books']:
                            books_data = []
                            for i, book in enumerate(res['books'], 1):
                                books_data.append({
                                    "N°": i,
                                    "Texte": book.get('text', 'N/A'),
                                    "Confiance": f"{book.get('confidence', 0):.1%}",
                                })
                            st.dataframe(books_data)
                        else:
                            st.warning("Aucun livre détecté.")

                # Graphiques avancés
                st.markdown("## Graphiques de comparaison avancés")
                import pandas as pd
                confs = [results_dict[e]['confidence'] for e in selected_engines]
                nb_books = [len(results_dict[e]['books']) for e in selected_engines]
                df = pd.DataFrame({
                    'Moteur': selected_engines,
                    'Confiance moyenne': confs,
                    'Livres détectés': nb_books
                })
                st.bar_chart(df.set_index('Moteur')[['Confiance moyenne', 'Livres détectés']])
                # Distribution des confiances
                st.markdown("### Distribution des confiances par moteur")
                for engine in selected_engines:
                    confs_list = [book.get('confidence', 0) for book in results_dict[engine]['books']]
                    st.line_chart(confs_list, height=150)
                # Heatmap du nombre de livres détectés (si pertinent)
                st.markdown("### Heatmap Livres détectés")
                import numpy as np
                heatmap_data = np.array(nb_books).reshape(1, -1)
                st.dataframe(heatmap_data)
            finally:
                os.unlink(temp_path)

if __name__ == "__main__":
    if 'page' not in locals():
        page = "Analyse OCR"
    if page == "Analyse OCR":
        main()
    elif page == "Comparaison OCR":
        ocr_comparison_page()

