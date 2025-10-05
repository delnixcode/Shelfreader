"""
Utilitaires d'enrichissement Open Library - ShelfReader P1

Ce module gère l'enrichissement des résultats OCR avec des métadonnées
provenant de l'API Open Library, permettant d'obtenir titres, auteurs,
dates de publication et couvertures de livres.
"""

from typing import Dict, List, Optional, Any
import sys
import os
# Ajouter le répertoire parent (src) au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.openlibrary_client import OpenLibraryClient


class OpenLibraryEnricher:
    """
    Classe pour enrichir les résultats OCR avec Open Library.

    Cette classe utilise l'API Open Library pour récupérer des informations
    supplémentaires sur les livres détectés par OCR, améliorant ainsi
    la qualité et la précision des résultats.

    Attributs:
        client (OpenLibraryClient): Client pour les appels API
    """

    def __init__(self, timeout: int = 10):
        """
        Initialise l'enrichisseur avec un client Open Library.

        Args:
            timeout (int): Timeout en secondes pour les appels API
        """
        self.client = OpenLibraryClient(timeout=timeout)

    def enrich_books(self, books: List[Dict]) -> List[Dict]:
        """
        Enrichit une liste de livres avec les données Open Library.

        Pour chaque livre détecté par OCR, cette méthode tente de trouver
        des informations complémentaires (titre exact, auteur, année, couverture)
        en utilisant le texte OCR comme requête de recherche.

        Args:
            books (List[Dict]): Liste des livres détectés par OCR
                Chaque livre doit contenir au minimum un champ 'text'

        Returns:
            List[Dict]: Liste des livres enrichis avec les champs supplémentaires:
                - openlibrary_title: Titre exact depuis Open Library
                - openlibrary_author: Auteur principal
                - openlibrary_year: Année de première publication
                - openlibrary_cover_url: URL de la couverture
                - openlibrary_url: Lien vers la page Open Library
                - openlibrary_description: Description du livre
                - openlibrary_subjects: Sujets/thèmes du livre
                - enriched: bool indiquant si l'enrichissement a réussi

        Note:
            Les livres non enrichis (pas de correspondance trouvée) gardent
            leur structure originale avec enriched=False.
        """
        enriched_books = []

        for book in books:
            text = book.get('text', '').strip()

            if text:
                # Tentative d'enrichissement via Open Library
                enriched_info = self.client.get_book_info_for_ocr_result(text)

                if enriched_info:
                    # Fusion des données OCR avec les données Open Library
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
                    # Livre OCR sans enrichissement
                    book_copy = book.copy()
                    book_copy['enriched'] = False
                    enriched_books.append(book_copy)
            else:
                # Texte OCR vide
                book_copy = book.copy()
                book_copy['enriched'] = False
                enriched_books.append(book_copy)

        return enriched_books

    def get_enrichment_stats(self, books: List[Dict]) -> Dict[str, int]:
        """
        Calcule les statistiques d'enrichissement.

        Args:
            books (List[Dict]): Liste des livres enrichis

        Returns:
            Dict[str, int]: Statistiques avec clés:
                - total: nombre total de livres
                - enriched: nombre de livres enrichis
                - not_enriched: nombre de livres non enrichis
                - enrichment_rate: taux d'enrichissement en pourcentage
        """
        total = len(books)
        enriched = sum(1 for book in books if book.get('enriched', False))
        not_enriched = total - enriched

        return {
            'total': total,
            'enriched': enriched,
            'not_enriched': not_enriched,
            'enrichment_rate': (enriched / total * 100) if total > 0 else 0
        }


# Instance globale pour éviter les réinitialisations
openlibrary_enricher = OpenLibraryEnricher()