import pyodbc
import os
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.conn_str = (
            f"DRIVER={os.getenv('AZURE_SQL_DRIVER')};"
            f"SERVER={os.getenv('AZURE_SQL_SERVER')};"
            f"DATABASE={os.getenv('AZURE_SQL_DATABASE')};"
            f"UID={os.getenv('AZURE_SQL_USERNAME')};"
            f"PWD={os.getenv('AZURE_SQL_PASSWORD')}"
        )

    def get_connection(self):
        return pyodbc.connect(self.conn_str)

    def init_db(self):
        """Ma'lumotlar bazasida kerakli jadvallarni yaratish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Talabalar jadvali
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Students')
                CREATE TABLE Students (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    FullName NVARCHAR(100) NOT NULL,
                    Major NVARCHAR(100)
                )
            """)
            
            # Fanlar jadvali
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Courses')
                CREATE TABLE Courses (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    Name NVARCHAR(100) NOT NULL,
                    Credits INT NOT NULL
                )
            """)
            
            # Baholar jadvali
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Grades')
                CREATE TABLE Grades (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    StudentID INT FOREIGN KEY REFERENCES Students(ID),
                    CourseID INT FOREIGN KEY REFERENCES Courses(ID),
                    Grade FLOAT NOT NULL
                )
            """)
            
            conn.commit()
            print("Jadvallar muvaffaqiyatli yaratildi yoki allaqachon mavjud.")

    def get_all_grades(self):
        """Baholarni o'qish (Pandas algoritmi uchun).
        Qaytaradi: [{'student_id': 1, 'grade': 85.0, 'credits': 4}, ...]"""
        query = """
            SELECT g.StudentID as student_id, g.Grade as grade, c.Credits as credits
            FROM Grades g
            JOIN Courses c ON g.CourseID = c.ID
        """
        results = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                results.append({
                    'student_id': row.student_id,
                    'grade': row.grade,
                    'credits': row.credits
                })
        return results

    def get_students(self):
        """Talabalar ro'yxatini olish"""
        query = "SELECT ID, FullName, Major FROM Students"
        students = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                students.append({
                    'id': row.ID,
                    'full_name': row.FullName,
                    'major': row.Major
                })
        return students

if __name__ == "__main__":
    db = DatabaseManager()
    db.init_db()
