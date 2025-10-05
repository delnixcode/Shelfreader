#Rôle : Chercher les infos du livre sur Open Library Technologies : requests, JSON
#Concepts : REST API, parsing de réponses

import requests
import time
import re
from typing import Optional, Dict, List, Any

class OpenLibraryClient:
    """Client pour interagir avec l'API Open Library"""

    def __init__(self, timeout=10):
        self.base_url = "https://openlibrary.org"
        self.timeout = timeout
        self.session = requests.Session()  # Utiliser une session pour de meilleures performances

    def search_books(self, query, limit=5):
        """Cherche des livres par titre sur Open Library"""

        # Nettoyer et encoder la requête
        query = query.strip()
        if not query:
            return None

        # Encoder les espaces et caractères spéciaux
        query_encoded = requests.utils.quote(query)

        url = f"{self.base_url}/search.json?q={query_encoded}&limit={limit}"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
            time.sleep(0.1)  # Rate limiting
            return response.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la recherche: {e}")
            return None

    def get_book_details(self, work_key):
        """Récupère les détails d'un livre"""
        if not work_key or not work_key.startswith('/works/'):
            return None

        url = f"{self.base_url}{work_key}.json"

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            time.sleep(0.1)
            return response.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des détails: {e}")
            return None

    def get_book_cover_url(self, isbn, size='M'):
        """Génère l'URL de la couverture d'un livre

        Args:
            isbn: L'ISBN du livre (ex: "9780441172719")
            size: Taille de l'image ('S', 'M', 'L') - défaut: 'M'

        Returns:
            str: URL de la couverture si ISBN existe
            None: Si pas d'ISBN
        """
        if isbn and isinstance(isbn, str):
            # Nettoyer l'ISBN (enlever les tirets et espaces)
            isbn_clean = re.sub(r'[-\s]', '', isbn)
            if len(isbn_clean) in [10, 13] and isbn_clean.isdigit():
                return f"https://covers.openlibrary.org/b/isbn/{isbn_clean}-{size}.jpg"
        return None

    def search_book_by_title_and_author(self, title: str, author: Optional[str] = None, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Recherche avancée avec titre et auteur

        Args:
            title: Titre du livre
            author: Auteur (optionnel)
            limit: Nombre maximum de résultats

        Returns:
            Résultats de recherche ou None
        """
        if not title.strip():
            return None

        query = f'title:"{title.strip()}"'
        if author:
            query += f' author:"{author.strip()}"'

        return self.search_books(query, limit)

    def get_book_info_for_ocr_result(self, ocr_text: str) -> Optional[Dict[str, Any]]:
        """Enrichit un résultat OCR avec des informations de Open Library

        Args:
            ocr_text: Texte extrait par OCR

        Returns:
            Dictionnaire avec informations enrichies ou None
        """
        if not ocr_text or len(ocr_text.strip()) < 3:
            return None

        # Nettoyer le texte OCR (enlever la ponctuation excessive, normaliser)
        clean_text = re.sub(r'[^\w\s]', ' ', ocr_text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)

        # Recherche sur Open Library
        results = self.search_books(clean_text, limit=1)

        if results and results.get('docs'):
            book = results['docs'][0]

            # Récupérer plus de détails si possible
            work_key = book.get('key')
            details = None
            if work_key:
                details = self.get_book_details(work_key)

            # Construire la réponse enrichie
            enriched_info = {
                'ocr_text': ocr_text,
                'title': book.get('title', 'Titre inconnu'),
                'author': book.get('author_name', ['Auteur inconnu'])[0] if book.get('author_name') else 'Auteur inconnu',
                'first_publish_year': book.get('first_publish_year'),
                'isbn': book.get('isbn', [None])[0] if book.get('isbn') else None,
                'cover_url': self.get_book_cover_url(book.get('isbn', [None])[0]) if book.get('isbn') else None,
                'open_library_url': f"https://openlibrary.org{work_key}" if work_key else None,
                'description': details.get('description') if details else None,
                'subjects': book.get('subject', []),
                'language': book.get('language', ['unknown'])[0] if book.get('language') else 'unknown'
            }

            return enriched_info

        return None