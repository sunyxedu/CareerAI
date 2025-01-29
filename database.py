import sqlite3
import Parser

# Create a connection to the SQLite database
conn = sqlite3.connect("internships.db")
cursor = conn.cursor()

# Create the internships table if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS internships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    company_link TEXT,
    programme_name TEXT,
    programme_link TEXT,
    opening_date TEXT,
    closing_date TEXT,
    last_year_opening TEXT,
    cv_required BOOLEAN,
    cover_letter TEXT,
    written_answers BOOLEAN,
    notes TEXT
)
''')

# Now the table exists, we can proceed with inserting data
jobs = Parser.Parser()

# Prepare data for insertion
data = []
for job in jobs:
    # Convert the Job object to a dictionary, then extract values
    job_dict = job.to_dict()
    data.append((
        job_dict["company_name"],  # company_name
        job_dict["company_link"],   # company_link
        job_dict["programme_name"], # programme_name
        job_dict["programme_link"], # programme_link
        job_dict["opening_date"],   # opening_date
        job_dict["closing_date"]    # closing_date
    ))

# Insert data into the internships table
cursor.executemany('''
INSERT INTO internships (company_name, company_link, programme_name, programme_link, opening_date, closing_date)
VALUES (?, ?, ?, ?, ?, ?)
''', data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully, and data inserted!")
