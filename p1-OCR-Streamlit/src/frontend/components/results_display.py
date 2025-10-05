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
                   enriched_books: Optional[List[Dict]] = None,
                   engine_name: str = None, advanced_params: Dict = None,
                   executed_command: str = None) -> None:
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

    # Section debug : commandes Streamlit vs Terminal
    if engine_name and advanced_params:
        with st.expander("🐛 Debug : Commandes exécutées"):
            st.markdown("### 📋 Paramètres utilisés dans Streamlit")

            # Paramètres spécifiques au moteur
            st.write("**Paramètres du moteur :**")
            engine_confidence = advanced_params.get('confidence', 0.3)
            engine_use_gpu = advanced_params.get('use_gpu', True)
            st.code(f"""
Confiance: {engine_confidence}
GPU: {'Activé' if engine_use_gpu else 'Désactivé'}
Moteur: {engine_name}
            """.strip())

            # Paramètres avancés par moteur
            st.write("**Paramètres avancés :**")
            if engine_name == 'EasyOCR' and advanced_params:
                st.code(f"""
Langues: {advanced_params.get('languages', ['en'])}
Méthode de détection: {advanced_params.get('spine_method', 'vertical_lines')}
                """.strip())
            elif engine_name == 'Tesseract' and advanced_params:
                st.code(f"""
Langue: {advanced_params.get('lang', 'eng')}
PSM: {advanced_params.get('psm', 6)}
                """.strip())
            elif engine_name == 'TrOCR' and advanced_params:
                st.code(f"""
Device: {advanced_params.get('device', 'auto')}
                """.strip())

            st.markdown("### 💻 Commande réellement exécutée")
            if executed_command:
                st.write("Commande capturée depuis les logs du terminal :")
                st.code(executed_command, language="bash")
            else:
                st.write("*Commande non capturée*")

            st.markdown("### 🔄 Commande équivalente reconstruite")
            st.write("Cette commande aurait produit le même résultat :")

            # Construction de la commande terminal
            cmd_parts = ["python", "main.py", "image_path"]

            if engine_use_gpu:
                cmd_parts.append("--gpu")
            if engine_confidence != 0.3:  # Si différent de la valeur par défaut
                cmd_parts.extend(["--confidence", str(engine_confidence)])

            # Paramètres avancés
            if advanced_params:
                if engine_name == 'EasyOCR':
                    if advanced_params.get('spine_method') and advanced_params['spine_method'] != 'vertical_lines':
                        cmd_parts.extend(["--spine-method", advanced_params['spine_method']])
                    if advanced_params.get('languages') and advanced_params['languages'] != ['en']:
                        cmd_parts.extend(["--languages"] + advanced_params['languages'])
                elif engine_name == 'Tesseract':
                    if advanced_params.get('lang') and advanced_params['lang'] != 'eng':
                        cmd_parts.extend(["--tesseract-lang", advanced_params['lang']])
                    if advanced_params.get('psm') and advanced_params['psm'] != 6:
                        cmd_parts.extend(["--tesseract-psm", str(advanced_params['psm'])])
                elif engine_name == 'TrOCR':
                    if advanced_params.get('device') and advanced_params['device'] != 'auto':
                        cmd_parts.extend(["--device", advanced_params['device']])

            terminal_cmd = " ".join(cmd_parts)
            st.code(terminal_cmd, language="bash")

            # Comparaison si les deux commandes sont disponibles
            if executed_command and executed_command != terminal_cmd.replace("image_path", "[IMAGE_PATH]"):
                st.warning("⚠️ **Différence détectée** : La commande exécutée ne correspond pas exactement à la reconstruction")
            elif executed_command:
                st.success("✅ **Correspondance parfaite** : Commande exécutée = commande reconstruite")

        st.markdown("---")

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
                             selected_engines: List[str],
                             global_confidence: float = None,
                             global_use_gpu: bool = None,
                             advanced_params: Dict = None,
                             executed_commands: Dict[str, str] = None,
                             enrich_with_ol: bool = False,
                             enriched_results: Dict[str, List[Dict]] = None) -> None:
    """
    Affiche les résultats de comparaison entre plusieurs moteurs OCR.

    Args:
        results_dict (Dict[str, Dict]): Résultats par moteur OCR
        selected_engines (List[str]): Liste des moteurs comparés
        global_confidence (float): Seuil de confiance global
        global_use_gpu (bool): Utilisation du GPU
        advanced_params (Dict): Paramètres avancés par moteur
        executed_commands (Dict[str, str]): Commandes exécutées
        enrich_with_ol (bool): Si vrai, afficher les livres enrichis
        enriched_results (Dict[str, List[Dict]]): Livres enrichis par config
    """
    # Section debug : commandes Streamlit vs Terminal
    if advanced_params:
        with st.expander("🐛 Debug : Commandes exécutées"):
            st.markdown("### 📋 Paramètres utilisés dans Streamlit")

            # Paramètres par configuration
            st.write("**Paramètres par configuration :**")
            for config_name, config_params in advanced_params.items():
                engine = config_params.get('engine', 'Unknown')
                confidence = config_params.get('confidence', 0.3)
                use_gpu = config_params.get('use_gpu', True)
                st.code(f"""
{config_name} ({engine}):
  Confiance: {confidence}
  GPU: {'Activé' if use_gpu else 'Désactivé'}
                """.strip())

                # Paramètres avancés spécifiques
                if engine == 'EasyOCR':
                    st.code(f"""
  Langues: {config_params.get('languages', ['en'])}
  Méthode de détection: {config_params.get('spine_method', 'vertical_lines')}
                    """.strip())
                elif engine == 'Tesseract':
                    st.code(f"""
  Langue: {config_params.get('lang', 'eng')}
  PSM: {config_params.get('psm', 6)}
                    """.strip())
                elif engine == 'TrOCR':
                    st.code(f"""
  Device: {config_params.get('device', 'auto')}
                    """.strip())

            st.markdown("### 💻 Commandes réellement exécutées")
            st.write("Commandes capturées depuis les logs du terminal :")

            if executed_commands:
                for config_name, cmd in executed_commands.items():
                    st.code(f"**{config_name}:**\n{cmd}", language="bash")
            else:
                st.write("*Aucune commande capturée*")

            st.markdown("### 🔄 Commandes équivalentes reconstruites")
            st.write("Ces commandes auraient produit les mêmes résultats :")

            # Construction des commandes terminal pour chaque configuration
            reconstructed_commands = {}
            for config_name, config_params in advanced_params.items():
                engine = config_params.get('engine', 'Unknown')
                
                # Utiliser le vrai chemin du script comme dans les vraies commandes
                if engine == 'EasyOCR':
                    cmd_parts = ["python", "src/engines/easyocr/main.py", "image_path"]
                elif engine == 'Tesseract':
                    cmd_parts = ["python", "src/engines/tesseract/main.py", "image_path"]
                elif engine == 'TrOCR':
                    cmd_parts = ["python", "src/engines/trocr/main.py", "image_path"]

                # Paramètres spécifiques à cette configuration - TOUJOURS inclus
                config_confidence = config_params.get('confidence', 0.3)
                config_use_gpu = config_params.get('use_gpu', True)
                
                if config_use_gpu:
                    cmd_parts.append("--gpu")
                else:
                    cmd_parts.append("--cpu")
                
                cmd_parts.extend(["--confidence", str(config_confidence)])

                # Paramètres avancés pour cette configuration - TOUJOURS inclus selon le moteur
                if engine == 'EasyOCR':
                    # Pour les spines : n'afficher que si différent du défaut (vertical_lines)
                    if config_params.get('spine_method') and config_params['spine_method'] != 'vertical_lines':
                        cmd_parts.extend(["--spine-method", config_params['spine_method']])
                    # Pour les langues : TOUJOURS inclus
                    if config_params.get('languages'):
                        cmd_parts.extend(["--lang"] + config_params['languages'])
                elif engine == 'Tesseract':
                    if config_params.get('lang'):
                        cmd_parts.extend(["--lang", config_params['lang']])
                    if config_params.get('psm') is not None:
                        cmd_parts.extend(["--psm", str(config_params['psm'])])
                elif engine == 'TrOCR':
                    if config_params.get('device'):
                        cmd_parts.extend(["--device", config_params['device']])

                terminal_cmd = " ".join(cmd_parts)
                reconstructed_commands[config_name] = terminal_cmd
                st.code(f"**{config_name}:**\n{terminal_cmd}", language="bash")

            # Comparaison si les commandes sont disponibles
            if executed_commands:
                differences_found = False
                for config_name in advanced_params.keys():
                    executed = executed_commands.get(config_name, "")
                    reconstructed = reconstructed_commands.get(config_name, "")
                    if executed and reconstructed:
                        # Normaliser pour la comparaison (remplacer les chemins temporaires)
                        executed_normalized = executed.replace("/tmp/", "[TEMP]/").split()
                        reconstructed_normalized = reconstructed.replace("image_path", "[TEMP]/image.jpg").split()
                        
                        if executed_normalized != reconstructed_normalized:
                            differences_found = True
                            break

                if differences_found:
                    st.warning("⚠️ **Différences détectées** : Certaines commandes exécutées ne correspondent pas aux reconstructions")
                else:
                    st.success("✅ **Correspondance parfaite** : Toutes les commandes exécutées correspondent aux reconstructions")

        st.markdown("---")

    st.markdown("## Résultats par moteur")

    # Affichage côte à côte
    cols = st.columns(len(selected_engines))

    for idx, config_name in enumerate(selected_engines):
        with cols[idx]:
            st.markdown(f"### {config_name}")
            res = results_dict[config_name]

            # Utiliser les livres enrichis si disponibles
            if enrich_with_ol and enriched_results and config_name in enriched_results and enriched_results[config_name]:
                books = enriched_results[config_name]
            else:
                books = res.get('books', [])

            # Métriques principales
            st.write(f"**Texte OCR :** {res.get('text', 'N/A')}")
            st.write(f"**Confiance moyenne :** {res.get('confidence', 0):.1%}")
            st.write(f"**Livres détectés :** {len(books)}")

            # Tableau des livres pour ce moteur
            if books:
                books_data = []
                for i, book in enumerate(books, 1):
                    enriched = book.get('enriched', False)
                    ol_url = book.get('openlibrary_url') if enriched else None
                    books_data.append({
                        "N°": i,
                        "Texte": book.get('text', 'N/A'),
                        "Confiance": f"{book.get('confidence', 0):.1%}",
                        "Lien Open Library": ol_url if ol_url else ""
                    })
                # Fonction helper pour créer les liens HTML
                def make_link(url: str) -> str:
                    if url:
                        return f'<a href="{html.escape(url)}" target="_blank">🔗 Open Library</a>'
                    return ""
                # Création du tableau HTML pour les liens cliquables
                table_html = "<table style='width:100%; border-collapse:collapse;'>"
                headers = ["N°", "Texte", "Confiance", "Lien Open Library"]
                table_html += "<tr>" + "".join([f"<th style='border:1px solid #ccc; padding:4px'>{h}</th>" for h in headers]) + "</tr>"
                for row in books_data:
                    table_html += "<tr>"
                    for h in headers[:-1]:
                        table_html += f"<td style='border:1px solid #ccc; padding:4px'>{html.escape(str(row[h]))}</td>"
                    table_html += f"<td style='border:1px solid #ccc; padding:4px'>{make_link(row['Lien Open Library'])}</td>"
                    table_html += "</tr>"
                table_html += "</table>"
                st.markdown(table_html, unsafe_allow_html=True)
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