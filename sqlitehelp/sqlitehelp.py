#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Datei: sqlitehelp.py
Autor: Florian Blum
Datum: 17.10.2023
Lizenz: MIT

Git: https://github.com/fblumus/csshelper/blob/main/sqlitehelp/sqlitehelp.py

Beschreibung:
Dieses Skript ermöglicht es einem Benutzer, mit einer SQLite-Datenbank zu interagieren, 
um Beziehungen zwischen Tabellen zu identifizieren, spezifische Spalten für die Abfrage 
auszuwählen und dann basierend auf diesen Auswahlkriterien eine SQL JOIN-Abfrage zu 
generieren. Die Hauptfunktionalitäten umfassen das Abrufen von Tabellenbeziehungen, 
das Abrufen von Spaltennamen und das Erstellen einer JOIN-Abfrage.
"""

import sqlite3

def get_table_relations(conn):
    """
    Holt alle Tabellenbeziehungen aus der SQLite-Datenbank.

    Args:
    - conn (sqlite3.Connection): Die Verbindung zur SQLite-Datenbank.

    Returns:
    - dict: Ein Dictionary, das die Beziehungen zwischen den Tabellen repräsentiert. 
            Schlüssel sind Tupel (Ursprungstabelle, Zielkolonne) und Werte sind 
            Tupel (Zieltabelle, Zielkolonne).
    """
    cursor = conn.cursor()
    
    # Hole alle Tabellennamen in der Datenbank
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    relations = {}
    
    # Hole alle Beziehungen für jede Tabelle
    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        foreign_keys = cursor.fetchall()
        
        for fk in foreign_keys:
            relations[(table, fk[2])] = (fk[3], fk[4])
            
    return relations

def get_columns(conn, table):
    """
    Holt alle Spaltennamen einer Tabelle aus der SQLite-Datenbank.

    Args:
    - conn (sqlite3.Connection): Die Verbindung zur SQLite-Datenbank.
    - table (str): Der Name der Tabelle.

    Returns:
    - list: Eine Liste der Spaltennamen der gegebenen Tabelle.
    """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table});")
    columns = [column[1] for column in cursor.fetchall()]
    return columns

def select_columns(conn, relations):
    """
    Ermöglicht dem Benutzer das Auswählen von Spalten aus den Tabellen.

    Args:
    - conn (sqlite3.Connection): Die Verbindung zur SQLite-Datenbank.
    - relations (dict): Das Dictionary der Tabellenbeziehungen.

    Returns:
    - list: Eine Liste der ausgewählten Spalten.
    """
    selected_columns = []

    all_tables = set()
    for (table1, table2), _ in relations.items():
        all_tables.add(table1)
        all_tables.add(table2)

    for table in all_tables:
        columns = get_columns(conn, table)
        for column in columns:
            include_column = input(f"Möchten Sie die Spalte {column} aus der Tabelle {table} einbeziehen? (j/n): ").strip().lower()
            if include_column == 'j':
                selected_columns.append(f"{table}.{column}")
    
    return selected_columns

def create_join_query(conn, relations, selected_columns):
    """
    Erstellt eine SQL JOIN-Abfrage basierend auf den vom Benutzer ausgewählten Spalten und Beziehungen.

    Args:
    - conn (sqlite3.Connection): Die Verbindung zur SQLite-Datenbank.
    - relations (dict): Das Dictionary der Tabellenbeziehungen.
    - selected_columns (list): Die Liste der ausgewählten Spalten.

    Returns:
    - str: Die erstellte SQL-Abfrage.
    """
    query = "SELECT "
    
    if selected_columns:
        query += ", ".join(selected_columns) + " FROM "

        tables_in_query = set()
        for (table1, table2), (column1, column2) in relations.items():
            include_relation = input(f"Möchten Sie die Tabellen {table1} und {table2} joinen? (j/n): ").strip().lower()
            if include_relation == 'j':
                if not tables_in_query:
                    query += f"{table1} JOIN {table2} ON {table1}.{column1} = {table2}.{column2}"
                    tables_in_query.update({table1, table2})
                else:
                    if table2 not in tables_in_query:
                        query += f" JOIN {table2} ON {table1}.{column1} = {table2}.{column2}"
                        tables_in_query.add(table2)
    else:
        query += "* FROM " + next(iter(relations.keys()))[0]
    
    return query

# Verbinden zur SQLite Datenbank
conn = sqlite3.connect('css-exam-2021-anonymize-data-initial.db')

# Hole alle Tabellenbeziehungen
relations = get_table_relations(conn)

# Benutzer ausgewählte Spalten
selected_columns = select_columns(conn, relations)

# Erstelle eine JOIN Abfrage
query = create_join_query(conn, relations, selected_columns)
print(query)

