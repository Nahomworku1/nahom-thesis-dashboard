"""
Convert MySQL thesis_db → thesis.db (SQLite)
Run ONCE:  python convert_to_sqlite.py
"""
import sqlite3, os
from decimal import Decimal
import mysql.connector

print("Connecting to MySQL...")
my = mysql.connector.connect(
    host="localhost", port=3306, user="root",
    password="#Dualscreen123",
    database="thesis_db",
)
mc = my.cursor()

print("Creating thesis.db...")
if os.path.exists("thesis.db"):
    os.remove("thesis.db")
sq = sqlite3.connect("thesis.db")
sc = sq.cursor()

mc.execute("SHOW TABLES")
tables = [row[0] for row in mc.fetchall()]
print(f"Found tables: {tables}")

for table in tables:
    print(f"\n  Table: {table}")

    mc.execute(f"DESCRIBE {table}")
    columns = mc.fetchall()

    col_defs = []
    col_names = []
    for col in columns:
        name       = col[0]
        mysql_type = col[1].upper()
        key        = col[3]
        col_names.append(name)

        if any(t in mysql_type for t in ["INT","TINYINT","SMALLINT","BIGINT"]):
            sq_type = "INTEGER"
        elif any(t in mysql_type for t in ["FLOAT","DOUBLE","DECIMAL","NUMERIC","REAL"]):
            sq_type = "REAL"
        else:
            sq_type = "TEXT"

        pk = " PRIMARY KEY" if key == "PRI" else ""
        col_defs.append(f"{name} {sq_type}{pk}")

    ddl = f"CREATE TABLE {table} ({', '.join(col_defs)})"
    print(f"    Columns: {col_names}")
    sc.execute(ddl)

    mc.execute(f"SELECT {', '.join(col_names)} FROM {table}")
    rows = mc.fetchall()
    if rows:
        # Convert Decimal → float so SQLite accepts the values
        clean = [
            tuple(float(v) if isinstance(v, Decimal) else v for v in row)
            for row in rows
        ]
        placeholders = ", ".join(["?"] * len(col_names))
        sc.executemany(f"INSERT INTO {table} VALUES ({placeholders})", clean)
    print(f"    Copied {len(rows)} rows ✓")

sq.commit()
sq.close()
my.close()

size = os.path.getsize("thesis.db") / 1024
print(f"\n✅ Done! thesis.db created ({size:.1f} KB)")
print("Now upload thesis.db + dashboard_sqlite.py + requirements.txt to GitHub")