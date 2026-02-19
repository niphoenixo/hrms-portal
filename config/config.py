import os
from dotenv import load_dotenv

load_dotenv()
# Example: mysql+pymysql://root:password123@localhost:3306/hrms_db
DATABASE_URL=f"mysql+pymysql://{os.getenv("DB_USER_NAME")}:{os.getenv("DB_PASSSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"
TOKEN_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30