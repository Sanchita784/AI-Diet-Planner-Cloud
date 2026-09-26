from flask import Blueprint, jsonify, request, session
from ai.diet_generator import generate_diet_plan

diet_api = Blueprint("diet_api", __name__)


@diet_api.route("/api/diet", methods=["GET"])
def diet_api_route():

    # User must be logged in
    if "user_email" not in session:
        return jsonify({
            "error": "User not logged in"
        }), 401

    goal = request.args.get("goal", "maintenance")

    plan = generate_diet_plan(
        session.get("user_age"),
        goal
    )

    return jsonify({
        "goal": goal,
        "diet_plan": plan
    })