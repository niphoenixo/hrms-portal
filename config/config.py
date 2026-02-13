import os
from dotenv import load_dotenv

load_dotenv()
# Example: mysql+pymysql://root:password123@localhost:3306/hrms_db
DATABASE_URL=f"mysql+pymysql://{os.getenv("DB_USER_NAME")}:{os.getenv("DB_PASSSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"