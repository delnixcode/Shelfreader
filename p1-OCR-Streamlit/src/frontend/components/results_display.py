"""
Composant d'affichage des résultats - ShelfReader P1

Ce module gère l'affichage structuré des résultats OCR,
incluant les métriques, tableaux de livres et statistiques.
"""

import streamlit as st
import numpy as np
import pandas as pd
import html
from typing import Dict, List, Optional, Any


def display_results(results: Dict, processing_time: float,
                   enriched_books: Optional[List[Dict]] = None) -> None:
    """
    Affiche les résultats de l'OCR de manière structurée et complète.

    Cette fonction crée une interface utilisateur complète pour présenter
    les résultats de l'analyse OCR, avec métriques, tableaux et détails.

    Args:
        results (Dict): Résultats bruts de l'OCR contenant 'books', 'text', 'confidence'
        processing_time (float): Temps de traitement en secondes
        enriched_books (Optional[List[Dict]]): Livres enrichis avec Open Library (si disponible)
    """
    if not results or 'books' not in results:
        st.error("Aucun résultat OCR trouvé")
        return

    # Utiliser les livres enrichis si disponibles
    books = enriched_books if enriched_books else results['books']

    # Section métriques principales
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

    # Section tableau détaillé des livres
    st.subheader("📖 Livres détectés")

    if books:
        # Préparation des données pour le tableau
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

        # Fonction helper pour créer les liens HTML
        def make_link(url: str) -> str:
            """Crée un lien HTML cliquable pour Open Library."""
            if url:
                return f'<a href="{html.escape(url)}" target="_blank">🔗 Open Library</a>'
            return ""

        # Création du tableau HTML pour les liens cliquables
        table_html = "<table style='width:100%; border-collapse:collapse;'>"
        # En-têtes
        headers = ["N°", "Titre OCR", "Titre OL", "Auteur", "Année", "Confiance", "Enrichi", "Lien Open Library"]
        table_html += "<tr>" + "".join([f"<th style='border:1px solid #ccc; padding:4px'>{h}</th>" for h in headers]) + "</tr>"
        # Lignes de données
        for row in books_data:
            table_html += "<tr>"
            for h in headers[:-1]:  # Tous sauf le dernier (lien)
                table_html += f"<td style='border:1px solid #ccc; padding:4px'>{html.escape(str(row[h]))}</td>"
            # Lien cliquable spécial
            table_html += f"<td style='border:1px solid #ccc; padding:4px'>{make_link(row['Lien Open Library'])}</td>"
            table_html += "</tr>"
        table_html += "</table>"

        st.markdown(table_html, unsafe_allow_html=True)

    else:
        st.warning("⚠️ Aucun livre détecté dans cette image")


def display_comparison_results(results_dict: Dict[str, Dict],
                             selected_engines: List[str]) -> None:
    """
    Affiche les résultats de comparaison entre plusieurs moteurs OCR.

    Args:
        results_dict (Dict[str, Dict]): Résultats par moteur OCR
        selected_engines (List[str]): Liste des moteurs comparés
    """
    st.markdown("## Résultats par moteur")

    # Affichage côte à côte
    cols = st.columns(len(selected_engines))

    for idx, engine in enumerate(selected_engines):
        with cols[idx]:
            st.markdown(f"### {engine}")
            res = results_dict[engine]

            # Métriques principales
            st.write(f"**Texte OCR :** {res.get('text', 'N/A')}")
            st.write(f"**Confiance moyenne :** {res.get('confidence', 0):.1%}")
            st.write(f"**Livres détectés :** {len(res.get('books', []))}")

            # Tableau des livres pour ce moteur
            books = res.get('books', [])
            if books:
                books_data = []
                for i, book in enumerate(books, 1):
                    books_data.append({
                        "N°": i,
                        "Texte": book.get('text', 'N/A'),
                        "Confiance": f"{book.get('confidence', 0):.1%}",
                    })
                st.dataframe(books_data)
            else:
                st.warning("Aucun livre détecté.")


def display_comparison_charts(results_dict: Dict[str, Dict],
                            selected_engines: List[str]) -> None:
    """
    Affiche les graphiques de comparaison avancés.

    Args:
        results_dict (Dict[str, Dict]): Résultats par moteur OCR
        selected_engines (List[str]): Liste des moteurs comparés
    """
    st.markdown("## Graphiques de comparaison avancés")

    # Préparation des données
    confs = [results_dict[e].get('confidence', 0) for e in selected_engines]
    nb_books = [len(results_dict[e].get('books', [])) for e in selected_engines]

    df = pd.DataFrame({
        'Moteur': selected_engines,
        'Confiance moyenne': confs,
        'Livres détectés': nb_books
    })

    # Graphique en barres
    st.bar_chart(df.set_index('Moteur')[['Confiance moyenne', 'Livres détectés']])

    # Distribution des confiances
    st.markdown("### Distribution des confiances par moteur")
    for engine in selected_engines:
        confs_list = [book.get('confidence', 0) for book in results_dict[engine].get('books', [])]
        if confs_list:
            st.line_chart(confs_list, height=150)
        else:
            st.write(f"**{engine}**: Aucune donnée de confiance disponible")

    # Heatmap du nombre de livres détectés
    st.markdown("### Heatmap Livres détectés")
    import numpy as np
    heatmap_data = np.array(nb_books).reshape(1, -1)
    st.dataframe(heatmap_data)