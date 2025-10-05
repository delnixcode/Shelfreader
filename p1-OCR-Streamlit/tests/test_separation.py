#!/usr/bin/env python3
"""
Test script pour la logique de séparation verticale sans EasyOCR
"""

def _refine_book_group_vertically(book_group, image_height):
    """Affiner un groupe de livre en séparant les textes vraiment distincts verticalement."""
    if len(book_group) <= 2:
        return [book_group]

    # Trier par position verticale
    sorted_group = sorted(book_group, key=lambda b: b['y'])

    # === ANALYSE AVANCÉE POUR ÉTAGÈRES DE LIVRES ===

    # 1. Analyser les gaps verticaux avec seuils adaptatifs
    vertical_gaps = []
    for i in range(len(sorted_group) - 1):
        gap = sorted_group[i + 1]['y'] - (sorted_group[i]['y'] + sorted_group[i]['height'])
        if gap > 0:
            vertical_gaps.append((i, gap))

    if not vertical_gaps:
        return [book_group]

    # 2. Détecter les changements de hauteur de police (indicateur fort de livre différent)
    font_size_changes = []
    for i in range(len(sorted_group) - 1):
        current_font = sorted_group[i]['font_size']
        next_font = sorted_group[i + 1]['font_size']
        size_diff = abs(current_font - next_font) / max(current_font, next_font)
        if size_diff > 0.3:  # Changement de taille > 30%
            font_size_changes.append(i + 1)  # Position de séparation

    # 3. Analyser les gaps avec seuils plus fins pour étagères
    gap_values = [gap for _, gap in vertical_gaps]
    if gap_values:
        # Pour étagères, utiliser des seuils plus sensibles
        avg_gap = sum(gap_values) / len(gap_values)
        min_gap = min(gap_values)
        max_gap = max(gap_values)

        # Seuil adaptatif : gaps significativement plus grands que la moyenne
        # mais plus sensible que l'ancien seuil de 2.0
        gap_threshold = max(avg_gap * 1.2, min_gap * 1.8, image_height * 0.02)  # 2% de la hauteur

        gap_separations = []
        for i, gap in vertical_gaps:
            if gap >= gap_threshold:
                gap_separations.append(i + 1)

        # 4. Combiner les séparations : changements de police + gaps significatifs
        all_separations = sorted(set(font_size_changes + gap_separations))

        # 5. Filtrer les séparations trop proches (éviter les micro-séparations)
        filtered_separations = []
        for sep in all_separations:
            # Vérifier qu'il n'y a pas de séparation trop proche
            if not filtered_separations or sep - filtered_separations[-1] >= 2:
                filtered_separations.append(sep)

        vertical_separations = filtered_separations
    else:
        vertical_separations = font_size_changes

    # 6. Créer les sous-groupes
    if not vertical_separations:
        return [book_group]  # Pas de séparation verticale

    subgroups = []
    start_idx = 0

    for sep_idx in vertical_separations:
        subgroup = sorted_group[start_idx:sep_idx]
        if len(subgroup) >= 1:  # Au moins un élément
            subgroups.append(subgroup)
        start_idx = sep_idx

    # Ajouter le dernier sous-groupe
    last_subgroup = sorted_group[start_idx:]
    if last_subgroup:
        subgroups.append(last_subgroup)

    # Filtrer les sous-groupes trop petits (artefacts)
    valid_subgroups = [sg for sg in subgroups if len(sg) >= 1]

    return valid_subgroups if valid_subgroups else [book_group]

if __name__ == "__main__":
    # Données de test simulées
    test_boxes = [
        {'x': 100, 'y': 50, 'width': 20, 'height': 15, 'font_size': 12, 'text': 'BOOK1'},
        {'x': 100, 'y': 70, 'width': 20, 'height': 15, 'font_size': 12, 'text': 'PART1'},
        {'x': 100, 'y': 120, 'width': 20, 'height': 18, 'font_size': 16, 'text': 'BOOK2'},  # Changement de taille
        {'x': 100, 'y': 145, 'width': 20, 'height': 18, 'font_size': 16, 'text': 'PART2'},
        {'x': 100, 'y': 200, 'width': 20, 'height': 14, 'font_size': 14, 'text': 'BOOK3'},  # Autre changement
    ]

    print("=== TEST DE LA SÉPARATION VERTICALE ===")
    print(f"Boîtes de test: {len(test_boxes)}")
    for i, box in enumerate(test_boxes):
        print(f"  {i+1}. y={box['y']}, font_size={box['font_size']}, text='{box['text']}'")

    result = _refine_book_group_vertically(test_boxes, 300)
    print(f"\nRésultat: {len(result)} groupes créés")
    for i, group in enumerate(result):
        print(f"Groupe {i+1}: {len(group)} éléments")
        for j, box in enumerate(group):
            print(f"  - {box['text']} (y={box['y']}, font_size={box['font_size']})")