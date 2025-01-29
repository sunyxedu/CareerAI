from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Route to fetch all internships from the database
@app.route("/internships", methods=["GET"])
def get_internships():
    # Connect to the SQLite database
    conn = sqlite3.connect("internships.db")
    cursor = conn.cursor()

    # Execute a query to fetch all data from the internships table
    cursor.execute("SELECT * FROM internships")
    internships = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the list of tuples into a list of dictionaries
    internships_list = [
        {
            "id": internship[0],
            "company_name": internship[1],
            "programme_name": internship[2],
            "position_link": internship[3],
            "opening_date": internship[4],
            "closing_date": internship[5],
            "last_year_opening": internship[6],
            "cv_required": internship[7],
            "cover_letter": internship[8],
            "written_answers": internship[9],
            "notes": internship[10]
        }
        for internship in internships
    ]

    # Return the data as JSON
    return jsonify(internships_list)

# Main entry point for running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
