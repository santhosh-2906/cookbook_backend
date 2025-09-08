from flask import Flask, jsonify
from flask_cors import CORS
from config import get_db_connection
import models
import routepath.auth_routes as auth_routes
import routepath.recipe_routes as recipe_routes

# ---------------- App Setup ----------------
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# ---------------- Initialize Database ----------------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(models.USER_TABLE)
    cursor.execute(models.RECIPE_TABLE)
    cursor.execute(models.STEP_TABLE)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

# ---------------- Register Blueprints ----------------
app.register_blueprint(auth_routes.bp)
app.register_blueprint(recipe_routes.bp)

# ---------------- Default Route ----------------
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Cooking Notes API!"})

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True)
