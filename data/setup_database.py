import sqlite3
import pandas as pd

csv_file_path = 'expert_profiles_all.csv'  
db_file_path = 'experts.db'

# Connect to SQLite Database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS expert_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    name TEXT,
    label TEXT,
    profile TEXT,
    url TEXT
);
'''
cursor.execute(create_table_query)

df = pd.read_csv(csv_file_path)

df.to_sql('expert_profiles', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print(f"Database '{db_file_path}' populated successfully with data from '{csv_file_path}'.")
