from flask import Blueprint, jsonify, session
import sqlite3

uploaded_files_api = Blueprint("uploaded_files_api", __name__)


@uploaded_files_api.route("/api/uploaded-files")
def uploaded_files():

    user_email = session.get("user_email")

    if not user_email:
        return jsonify({
            "error": "User not logged in"
        }), 401

    connection = sqlite3.connect("diet_planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT file_name, cloud_url, uploaded_at
        FROM uploaded_files
        WHERE user_email = ?
        ORDER BY uploaded_at DESC
    """, (user_email,))

    files = cursor.fetchall()

    connection.close()

    result = []

    for file in files:
        result.append({
            "file_name": file[0],
            "cloud_url": file[1],
            "uploaded_at": file[2]
        })

    return jsonify({
        "uploaded_files": result
    })