from flask import Blueprint, request, jsonify
from config import get_db_connection
from flask_cors import CORS

# ---------------- Blueprint Setup ----------------
bp = Blueprint("recipes", __name__)
CORS(bp)

# ---------------- Get All Recipes ----------------
@bp.route("/recipes", methods=["GET"])
def get_recipes():
    user_id = request.args.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if user_id:
        cursor.execute("SELECT * FROM recipes WHERE user_id=%s", (user_id,))
    else:
        cursor.execute("SELECT * FROM recipes")

    recipes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(recipes)


# ---------------- Get Single Recipe ----------------
@bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM recipes WHERE id=%s", (recipe_id,))
    recipe = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM steps WHERE recipe_id=%s ORDER BY step_number", 
        (recipe_id,)
    )
    steps = cursor.fetchall()

    cursor.close()
    conn.close()

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    return jsonify({"recipe": recipe, "steps": steps})


# ---------------- Add Recipe ----------------
@bp.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.json
    title = data.get("title")
    category = data.get("category")
    ingredients = data.get("ingredients")
    steps = data.get("steps", [])
    user_id = data.get("user_id")

    if not title or not category or not ingredients or not user_id:
        return jsonify({"error": "Title, category, ingredients, and user_id are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO recipes (title, category, ingredients, user_id) VALUES (%s, %s, %s, %s)",
        (title, category, ingredients, user_id)
    )
    recipe_id = cursor.lastrowid

    for i, step in enumerate(steps, start=1):
        if not step.get("description") or step.get("time_minutes") is None:
            continue
        cursor.execute(
            "INSERT INTO steps (recipe_id, step_number, description, time_minutes) VALUES (%s, %s, %s, %s)",
            (recipe_id, i, step["description"], step["time_minutes"])
        )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Recipe added successfully!"})


# ---------------- Update Recipe ----------------
@bp.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    data = request.json
    title = data.get("title")
    category = data.get("category")
    ingredients = data.get("ingredients")
    steps = data.get("steps", [])
    user_id = data.get("user_id")

    if not title or not category or not ingredients or not user_id:
        return jsonify({"error": "Title, category, ingredients, and user_id are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verify ownership
    cursor.execute("SELECT * FROM recipes WHERE id=%s AND user_id=%s", (recipe_id, user_id))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Not allowed"}), 403

    # Update recipe
    cursor.execute(
        "UPDATE recipes SET title=%s, category=%s, ingredients=%s WHERE id=%s",
        (title, category, ingredients, recipe_id)
    )
    cursor.execute("DELETE FROM steps WHERE recipe_id=%s", (recipe_id,))

    for i, step in enumerate(steps, start=1):
        if not step.get("description") or step.get("time_minutes") is None:
            continue
        cursor.execute(
            "INSERT INTO steps (recipe_id, step_number, description, time_minutes) VALUES (%s, %s, %s, %s)",
            (recipe_id, i, step["description"], step["time_minutes"])
        )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Recipe updated successfully!"})


# ---------------- Delete Recipe ----------------
@bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    user_id = request.args.get("user_id") 

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verify ownership
    cursor.execute("SELECT * FROM recipes WHERE id=%s AND user_id=%s", (recipe_id, user_id))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Not allowed"}), 403

    # Delete steps and recipe
    cursor.execute("DELETE FROM steps WHERE recipe_id=%s", (recipe_id,))
    cursor.execute("DELETE FROM recipes WHERE id=%s", (recipe_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Recipe deleted successfully!"})
