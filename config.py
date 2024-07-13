import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root@localhost/chatbot")
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
