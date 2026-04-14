import psycopg2

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="nevumo_leads",
    user="nevumo",
    password="nevumo"
)

# Read SQL file
with open('load_translations_v2.sql', 'r') as f:
    sql = f.read()

# Execute
cur = conn.cursor()
cur.execute(sql)
conn.commit()

print(f"Executed: {cur.rowcount} rows affected")

cur.close()
conn.close()
