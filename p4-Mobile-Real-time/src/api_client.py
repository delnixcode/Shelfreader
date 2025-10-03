#Rôle : Chercher les infos du livre sur Open Library Technologies : requests, JSON 
#Concepts : REST API, parsing de réponses

import requests
import time 

class OpenLibraryClient:
    """Client pour interagir avec l'API Open Library"""

    # TODO 1
    def __init__(self, timeout=10):
        self.base_url = "https://openlibrary.org"
        self.timeout = timeout

    # TODO 2
    def search_books(self, query, limit=5):
        """Cherche des livres par titre sur Open Library"""
        
        # 1. Construire l'URL avec f-string
        url = f"{self.base_url}/search.json?q={query}&limit={limit}"
        
        # 2. Faire la requête avec gestion d'erreurs
        try:
            response = requests.get(url, timeout=self.timeout)
            time.sleep(0.1)  # Rate limiting (max 10 req/sec)
            return response.json()  # Convertir JSON en dict Python
        except requests.RequestException:  # Capturer toutes les erreurs réseau
            return None  # Retourner None si erreur

    # TODO 3
    def get_book_details(self, work_key):
        """Récupère les détails d'un livre"""
        url = f"{self.base_url}{work_key}.json"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            time.sleep(0.1)
            return response.json()
        except requests.RequestException:
            return None

    # TODO 4
    def get_book_cover_url(self, isbn, size='M'):
        """Génère l'URL de la couverture d'un livre
        
        Args:
            isbn: L'ISBN du livre (ex: "9780441172719")
            size: Taille de l'image ('S', 'M', 'L') - défaut: 'M'
            
        Returns:
            str: URL de la couverture si ISBN existe
            None: Si pas d'ISBN
        """
        if isbn:
            return f"https://covers.openlibrary.org/b/isbn/{isbn}-{size}.jpg"
        return None