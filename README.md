# FastAPI Chatbot with Streamlit Frontend

This is a chatbot application built with FastAPI for the backend and Streamlit for the frontend. The chatbot utilizes the DialoGPT model from Hugging Face and stores data using SQLAlchemy.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)


## Installation

Clone the repository:

```bash
git clone https://github.com..
cd AIchatbot
```

#### Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```
## Setup

```bash
DATABASE_URL="mysql://root@localhost/chatbot"
SECRET_KEY="your_secret_key"
```
#### Update config.py to load environment variables:

```bash
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root@localhost/chatbot")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## Running the Application

#### Run the FastAPI backend:
```bash
uvicorn main:app --reload
```



#### Run the Streamlit frontend:
```bash
streamlit run front_end.py
```



> [!NOTE]
>  Open your browser and navigate to http://127.0.0.1:8000/docs to see the API documentation.
>  Open your browser and navigate to http://localhost:8501.


## Endpoints

- POST /token: Obtain an access token
- POST /users/: Create a new user
- POST /generate/: Generate a chatbot response
- GET /messages/{user_id}: Retrieve user messages


> [!IMPORTANT]
> Replace yourusername in the git clone URL with your actual GitHub username.
Ensure the .env file is properly listed in .gitignore to keep sensitive information secure.
The Streamlit application (front_end.py) should be in the root directory or properly referenced if it's located elsewhere.
Add any other relevant environment variables and configurations that your project requires.





