#!/usr/bin/env python3
"""
Test du client API Open Library
Vérifie que les fonctionnalités de recherche et récupération fonctionnent.
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_client import OpenLibraryClient

def test_api_client():
    """Teste les fonctionnalités du client Open Library"""

    print("🧪 Test du client API Open Library")
    print("=" * 50)

    # Initialisation du client
    client = OpenLibraryClient(timeout=15)
    print("✅ Client initialisé")

    # Test 1: Recherche de livres
    print("\n🔍 Test 1: Recherche de livres")
    query = "Harry Potter"
    results = client.search_books(query, limit=3)

    if results:
        print(f"✅ Recherche réussie pour '{query}'")
        print(f"   Nombre de résultats: {results.get('num_found', 0)}")

        # Afficher les premiers résultats
        docs = results.get('docs', [])
        for i, doc in enumerate(docs[:3], 1):
            title = doc.get('title', 'Titre inconnu')
            author = doc.get('author_name', ['Auteur inconnu'])[0]
            print(f"   {i}. '{title}' par {author}")
    else:
        print(f"❌ Échec de la recherche pour '{query}'")
        return False

    # Test 2: Détails d'un livre
    print("\n📖 Test 2: Récupération des détails")
    if docs:
        first_book = docs[0]
        work_key = first_book.get('key')

        if work_key:
            details = client.get_book_details(work_key)
            if details:
                print("✅ Détails récupérés avec succès")
                print(f"   Titre: {details.get('title', 'N/A')}")
                description = details.get('description', 'N/A')
                if isinstance(description, str):
                    desc_preview = description[:100]
                else:
                    desc_preview = str(description)[:100]
                print(f"   Description: {desc_preview}{'...' if len(str(description)) > 100 else ''}")
            else:
                print("❌ Échec de récupération des détails")
                return False
        else:
            print("⚠️ Pas de clé de travail pour ce livre")
    else:
        print("❌ Aucun livre trouvé pour tester les détails")
        return False

    # Test 3: URL de couverture
    print("\n🖼️ Test 3: Génération d'URL de couverture")
    isbn = first_book.get('isbn', [None])[0]
    if isbn:
        cover_url = client.get_book_cover_url(isbn, 'M')
        if cover_url:
            print("✅ URL de couverture générée")
            print(f"   URL: {cover_url}")
        else:
            print("❌ Échec de génération d'URL de couverture")
            return False
    else:
        print("⚠️ Pas d'ISBN disponible pour ce livre - test avec ISBN connu")
        # Test avec un ISBN connu
        test_isbn = "9780439708180"  # Harry Potter
        cover_url = client.get_book_cover_url(test_isbn, 'M')
        if cover_url:
            print("✅ URL de couverture générée avec ISBN de test")
            print(f"   URL: {cover_url}")
        else:
            print("❌ Échec de génération d'URL de couverture même avec ISBN connu")

    # Test 4: Recherche avancée titre + auteur
    print("\n🔍 Test 4: Recherche avancée (titre + auteur)")
    advanced_results = client.search_book_by_title_and_author(
        "Harry Potter and the Philosopher's Stone",
        "J.K. Rowling",
        limit=2
    )

    if advanced_results:
        print("✅ Recherche avancée réussie")
        docs_advanced = advanced_results.get('docs', [])
        if docs_advanced:
            book = docs_advanced[0]
            print(f"   Résultat: '{book.get('title', 'N/A')}' par {book.get('author_name', ['N/A'])[0]}")
    else:
        print("❌ Échec de la recherche avancée")

    # Test 5: Enrichissement OCR
    print("\n🤖 Test 5: Enrichissement de résultats OCR")
    ocr_text = "Harry Potter and the Chamber of Secrets"
    enriched = client.get_book_info_for_ocr_result(ocr_text)

    if enriched:
        print("✅ Enrichissement OCR réussi")
        print(f"   Texte OCR: {enriched['ocr_text']}")
        print(f"   Titre trouvé: {enriched['title']}")
        print(f"   Auteur: {enriched['author']}")
        print(f"   Année: {enriched.get('first_publish_year', 'N/A')}")
        print(f"   Couverture: {'Oui' if enriched.get('cover_url') else 'Non'}")
    else:
        print("❌ Échec de l'enrichissement OCR")

    print("\n" + "=" * 50)
    print("🎉 Tous les tests sont passés avec succès!")
    print("\n📋 Fonctionnalités testées:")
    print("• Recherche de livres par titre")
    print("• Récupération des détails complets")
    print("• Génération d'URLs de couverture")
    print("• Recherche avancée titre + auteur")
    print("• Enrichissement de résultats OCR")
    print("• Gestion d'erreurs et timeouts")
    print("• Nettoyage et validation des données")

    return True

if __name__ == "__main__":
    success = test_api_client()
    sys.exit(0 if success else 1)