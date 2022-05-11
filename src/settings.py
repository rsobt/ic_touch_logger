import os
from dotenv import load_dotenv

load_dotenv()

SQL_USER_NAME = os.environ.get("SQL_USER_NAME")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")
SQL_DB_NAME = os.environ.get("SQL_DB_NAME")

GOOGLE_CALENDER_ID = os.environ.get("GOOGLE_CALENDER_ID")
GOOGLE_CLEDENTIALS_PATH = os.environ.get("GOOGLE_CLEDENTIALS_PATH")
