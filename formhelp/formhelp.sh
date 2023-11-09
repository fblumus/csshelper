#!/bin/bash

# Überprüfe, ob genügend Argumente übergeben wurden
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 [URL] [DEPTH]"
    exit 1
fi

URL=$1
DEPTH=$2

# Datum und Uhrzeit für den Verzeichnisnamen generieren
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Temporäres Verzeichnis im aktuellen Verzeichnis erstellen
TMP_DIR="./${TIMESTAMP}_website_scan"

# Erstelle das Verzeichnis
mkdir -p "$TMP_DIR"

# Hilfsfunktionen definieren
print_urls_with_forms() {
    echo "Seiten mit Formularfeldern (input, select, textarea):"
    grep --binary-files=text -Hrio -e '<input' -e '<select' -e '<textarea' "$1" | cut -d: -f1 | uniq
}

print_tokens() {
    echo "Mögliche Tokens gefunden auf:"
    grep --binary-files=text -Hrio -e '<input .*type="hidden".*>' "$1" |
    grep -i 'csrf\|token' |
    cut -d: -f1 | uniq |
    while read -r line; do
        echo "Datei: $line"
        grep -o '<input [^>]*type="hidden"[^>]*>' "$line"
    done
}

print_all_links() {
    echo "Gefundene Links:"
    find "$1" -type f -exec grep -oP 'href="\K[^"]+' {} \; | sort | uniq
}

# Funktion, um rekursiv Webseiten herunterzuladen
scan_website() {
    local current_depth="$1"
    local current_url="$2"
    local current_dir="$3"

    # Webseite rekursiv herunterladen bis zur angegebenen Tiefe
    wget -q -r -l "$current_depth" -P "$current_dir" -E -H -k -p "$current_url"
}

# Starte den Scan
scan_website "$DEPTH" "$URL" "$TMP_DIR"

# Ergebnisse ausgeben
echo "-------------------------"
print_all_links "$TMP_DIR"
echo "-------------------------"
print_urls_with_forms "$TMP_DIR"
echo "-------------------------"
print_tokens "$TMP_DIR"
echo "-------------------------"

# Aufräumen entfernen
#rm -rf "$TMP_DIR"
