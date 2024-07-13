# FastAPI Chatbot with Streamlit Frontend

This is a chatbot application built with FastAPI for the backend and Streamlit for the frontend. The chatbot utilizes the DialoGPT model from Hugging Face and stores data using SQLAlchemy.

## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)

## Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/yourusername/fastapi-chatbot.git
   cd fastapi-chatbot
Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:```

   ```bash
pip install -r requirements.txt
Setup
Create a .env file in the project directory and add your environment variables:

   ```bash
DATABASE_URL="mysql://root@localhost/chatbot"
SECRET_KEY="your_secret_key"
Update config.py to load environment variables:

   ```bash
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root@localhost/chatbot")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
Running the Application
Run the FastAPI backend:

   ```bash
uvicorn main:app --reload
Run the Streamlit frontend:

   ```bash
streamlit run front_end.py
Access the applications:

FastAPI documentation: Open your browser and navigate to http://127.0.0.1:8000/docs to see the interactive API documentation.
Streamlit frontend: Open your browser and navigate to http://localhost:8501.

POST /token: Obtain an access token
POST /users/: Create a new user
POST /generate/: Generate a chatbot response
GET /messages/{user_id}: Retrieve user messages
Example Requests
Obtain an access token:

```bash
curl -X POST "http://127.0.0.1:8000/token" -H "accept: application/json" -d "username=test&password=test"
Create a new user:

```bash
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{"username": "test", "email": "test@example.com", "password": "test"}'
Generate a chatbot response:

   ```bash
curl -X POST "http://127.0.0.1:8000/generate/" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d '{"text": "Hello!"}'
Retrieve user messages:

   ```bash
curl -X GET "http://127.0.0.1:8000/messages/1" -H "accept: application/json"
License
This project is licensed under the MIT License. See the LICENSE file for more details.


### Notes:

1. **Replace `yourusername` in the git clone URL** with your actual GitHub username.
2. **Ensure the `.env` file is properly listed in `.gitignore`** to keep sensitive information secure.
3. **The Streamlit application (`front_end.py`) should be in the root directory** or properly referenced if it's located elsewhere.
4. **Add any other relevant environment variables** and configurations that your project requires.





