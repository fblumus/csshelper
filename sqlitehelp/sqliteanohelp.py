def identify_fields(query):
    select_part = query.split("FROM")[0].replace("SELECT", "").strip()
    fields = [field.strip() for field in select_part.split(",")]
    return fields

def get_date_positions(date_example):
    if "-" in date_example:
        separator = "-"
    elif "/" in date_example:
        separator = "/"
    else:
        separator = "."

    day, month, year = date_example.split(separator)
    day_pos = (1, len(day))
    month_pos = (day_pos[1] + 2, day_pos[1] + 1 + len(month))
    year_pos = (month_pos[1] + 2, month_pos[1] + 1 + len(year))

    return day_pos, month_pos, year_pos, separator

def get_anonymization_options(fields):
    anonymized_fields = []

    for field in fields:
        print(f"\nWie möchten Sie das Feld '{field}' anonymisieren?")
        print("1. Nicht anonymisieren")
        print("2. Datum: Nur Jahr anzeigen")
        print("3. Datum: Nur Jahr und Monat anzeigen")
        print("4. String: Anzahl der anzuzeigenden Zeichen")
        print("5. String: Ersetzen durch festgelegte Anzahl von Ersatzzeichen")

        choice = input("Ihre Wahl: ")
        if choice == "1":
            anonymized_fields.append(field)
        elif choice in ["2", "3"]:
            date_example = input("Bitte geben Sie ein Beispiel für das Datum im aktuellen Format an (z.B. 09.04.1976 oder 12/25/2022): ")
            day_pos, month_pos, year_pos, separator = get_date_positions(date_example)

            if choice == "2":
                anonymized_fields.append(f"SUBSTR({field}, {year_pos[0]}, {year_pos[1] - year_pos[0] + 1}) AS '{field}'")
            elif choice == "3":
                anonymized_fields.append(f"SUBSTR({field}, {month_pos[0]}, {month_pos[1] - month_pos[0] + 1}) || '{separator}' || SUBSTR({field}, {year_pos[0]}, {year_pos[1] - year_pos[0] + 1}) AS '{field}'")
        elif choice == "4":
            length = input("Anzahl der anzuzeigenden Zeichen: ")
            anonymized_fields.append(f"SUBSTR({field}, 1, {length}) AS '{field}'")
        elif choice == "5":
            length = input("Anzahl der anzuzeigenden Zeichen: ")
            replacement = input("Geben Sie die Ersatzzeichen ein: ")
            anonymized_fields.append(f"SUBSTR({field}, 1, {length}) || '{replacement}' AS '{field}'")
        else:
            print("Ungültige Auswahl, das Feld wird nicht anonymisiert.")
            anonymized_fields.append(field)
        
    return anonymized_fields



def create_anonymized_query(query, anonymized_fields):
    select_part = ",\n  ".join(anonymized_fields)
    from_part_onwards = query.split("FROM")[1]
    anonymized_query = f"SELECT\n  {select_part}\nFROM{from_part_onwards}"
    return anonymized_query

# Hauptteil des Scripts
with open('query.sql', 'r') as file:
    query = file.read()

fields = identify_fields(query)
anonymized_fields = get_anonymization_options(fields)
anonymized_query = create_anonymized_query(query, anonymized_fields)
print("\nIhr anonymisierter SQL-Query:")
print(anonymized_query)
