from flask import Blueprint, request, jsonify
from config import get_db_connection
from flask_cors import CORS
bp = Blueprint("auth", __name__)
CORS(bp)

# ---------------- Register ----------------
@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # check if user already exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing = cursor.fetchone()
    if existing:
        cursor.close()
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    # store plain text password (beginner style)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "User registered successfully!"})


# ---------------- Login ----------------
@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # check username + password directly (no hashing)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "user_id": user["id"]})


# ---------------- Update ----------------
@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    new_username = data.get("username")
    new_password = data.get("password")

    if not new_username:
        return jsonify({"error": "Username is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    if new_password:
        # update username + password directly
        cursor.execute(
            "UPDATE users SET username=%s, password=%s WHERE id=%s",
            (new_username, new_password, user_id)
        )
    else:
        cursor.execute(
            "UPDATE users SET username=%s WHERE id=%s",
            (new_username, user_id)
        )

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated successfully!"})


# ---------------- Delete ----------------
@bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User deleted successfully!"})
