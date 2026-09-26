from flask import Blueprint, jsonify, session
import sqlite3

diet_history_api = Blueprint("diet_history_api", __name__)


@diet_history_api.route("/api/diet-history")
def diet_history():

    user_email = session.get("user_email")

    if not user_email:
        return jsonify({
            "error": "User not logged in"
        }), 401

    connection = sqlite3.connect("diet_planner.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT goal, breakfast, lunch, evening_snack, dinner, created_at
        FROM diet_history
        WHERE user_email = ?
        ORDER BY created_at DESC
    """, (user_email,))

    history = cursor.fetchall()

    connection.close()

    result = []

    for item in history:
        result.append({
            "goal": item[0],
            "breakfast": item[1],
            "lunch": item[2],
            "evening_snack": item[3],
            "dinner": item[4],
            "created_at": item[5]
        })

    return jsonify({
        "diet_history": result
    })