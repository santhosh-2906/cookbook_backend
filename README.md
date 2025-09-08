🍴 CookBook - Backend

This is the backend for the CookBook application, built with Python Flask and MySQL. It handles user authentication, recipe management, and serves as the API for the frontend.

Preview
  ![CookBook Frontend Screenshot](./src/assets/image.png)
🌐 Live Demo

  Frontend: https://cookbook-frontend-oi5f.vercel.app

  Backend API: https://your-backend-url.com

Features

  User authentication (Login/Register)

  Create, read, update, delete recipes

  Recipe steps with timers

  RESTful API endpoints

  CORS enabled for frontend integration

  Secure password hashing

🛠️ Tech Stack

  Python 3.10+

  Flask

  Flask-CORS

  MySQL / MariaDB

  Gunicorn (for production deployment)

💻 Installation

  Clone the repository:

    git clone https://github.com/yourusername/cookbook-backend.git
    cd cookbook-backend

Create a virtual environment and activate it:

    python -m venv venv
# Windows
    venv\Scripts\activate
# macOS/Linux
    source venv/bin/activate


Install dependencies:

    pip install -r requirements.txt


Create a .env file in the root :

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=cookbook


Run the Flask server:

flask run


The API will be available at http://localhost:5000.
```
📂 Folder Structure
backend/
 ├─ app.py            # Main Flask app
 ├─ config.py         # DB connection / configuration
 ├─ routes/           # API route modules
 ├─ models/           # Database models (optional)
 ├─ migrations/       # Database migrations (optional)
 ├─ .env
 ├─ requirements.txt
 └─ README.md
```
🔧 Scripts
flask run          # Run the backend in development mode
gunicorn app:app   # Run in production (ensure gunicorn is installed)
