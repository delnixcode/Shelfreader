#!/bin/bash
# Script de sauvegarde et restauration de l'environnement virtuel P1
# Usage: ./backup_env.sh [backup|restore]

ENV_NAME="env-p1"
PROJECT_DIR="p1-OCR-Streamlit"
BACKUP_FILE="${ENV_NAME}-backup.tar.gz"

case "$1" in
    "backup")
        echo "🔄 Création de la sauvegarde de l'environnement virtuel..."
        if [ -d "$PROJECT_DIR/$ENV_NAME" ]; then
            tar -czf "$BACKUP_FILE" "$PROJECT_DIR/$ENV_NAME"
            echo "✅ Sauvegarde créée: $BACKUP_FILE"
            echo "📊 Taille: $(du -sh "$BACKUP_FILE" | cut -f1)"
        else
            echo "❌ Environnement $ENV_NAME introuvable dans $PROJECT_DIR/"
            exit 1
        fi
        ;;

    "restore")
        echo "🔄 Restauration de l'environnement virtuel..."
        if [ -f "$BACKUP_FILE" ]; then
            tar -xzf "$BACKUP_FILE"
            echo "✅ Environnement restauré dans $PROJECT_DIR/$ENV_NAME"
        else
            echo "❌ Fichier de sauvegarde $BACKUP_FILE introuvable"
            echo "💡 Créez d'abord une sauvegarde avec: ./backup_env.sh backup"
            exit 1
        fi
        ;;

    *)
        echo "Usage: $0 [backup|restore]"
        echo ""
        echo "Commands:"
        echo "  backup   - Sauvegarder l'environnement virtuel actuel"
        echo "  restore  - Restaurer l'environnement virtuel depuis la sauvegarde"
        echo ""
        echo "Note: Ce script permet de sauvegarder/restaurer l'environnement"
        echo "virtuel sans le versionner dans Git (meilleure pratique)"
        exit 1
        ;;
esac