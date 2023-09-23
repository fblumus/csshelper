import sqlite3

def get_table_relations(conn):
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
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table});")
    columns = [column[1] for column in cursor.fetchall()]
    return columns

def select_columns(conn, relations):
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
conn = sqlite3.connect('c3-database-initial.db')

# Hole alle Tabellenbeziehungen
relations = get_table_relations(conn)

# Benutzer ausgewählte Spalten
selected_columns = select_columns(conn, relations)

# Erstelle eine JOIN Abfrage
query = create_join_query(conn, relations, selected_columns)
print(query)

