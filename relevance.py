import os
import sqlite3
from groq import Groq

def relevance(text):
    conn = sqlite3.connect("internships.db")
    cursor = conn.cursor()

    # Query to get the internship position names
    cursor.execute("SELECT programme_name FROM internships")

    # Fetch all rows from the query result
    positions = cursor.fetchall()
    conn.close()

    client = Groq(
        api_key=("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"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Sort internship positions {positions} by relevance, using the CV \n {text}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return (chat_completion.choices[0].message.content)