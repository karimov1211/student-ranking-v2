import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

conn_str = (
    f"DRIVER={os.getenv('AZURE_SQL_DRIVER')};"
    f"SERVER={os.getenv('AZURE_SQL_SERVER')};"
    f"DATABASE={os.getenv('AZURE_SQL_DATABASE')};"
    f"UID={os.getenv('AZURE_SQL_USERNAME')};"
    f"PWD={os.getenv('AZURE_SQL_PASSWORD')}"
)

print(f"Connecting with: {conn_str}")

try:
    conn = pyodbc.connect(conn_str)
    print("Muvaffaqiyatli ulandi!")
    conn.close()
except Exception as e:
    print(f"Xatolik yuz berdi: {e}")
