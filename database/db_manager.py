import pyodbc
import os
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.conn_str = (
            f"DRIVER={os.getenv('AZURE_SQL_DRIVER', '{ODBC Driver 18 for SQL Server}')};"
            f"SERVER={os.getenv('AZURE_SQL_SERVER', 'library-server-karimov1211.database.windows.net')};"
            f"DATABASE={os.getenv('AZURE_SQL_DATABASE', 'RankingDB_v2')};"
            f"UID={os.getenv('AZURE_SQL_USERNAME', 'dbadmin')};"
            f"PWD={os.getenv('AZURE_SQL_PASSWORD', 'AzurePassword123!')}"
        )

    def get_connection(self):
        return pyodbc.connect(self.conn_str)

    def init_db(self):
        """Ma'lumotlar bazasida barcha kerakli jadvallarni yaratish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Talabalar
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Students')
                CREATE TABLE Students (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    FullName NVARCHAR(100) NOT NULL,
                    Major NVARCHAR(100)
                )
            """)
            
            # 2. Fanlar
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Courses')
                CREATE TABLE Courses (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    Name NVARCHAR(100) NOT NULL,
                    Credits INT NOT NULL
                )
            """)
            
            # 3. Baholar
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Grades')
                CREATE TABLE Grades (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    StudentID INT FOREIGN KEY REFERENCES Students(ID),
                    CourseID INT FOREIGN KEY REFERENCES Courses(ID),
                    Grade FLOAT NOT NULL
                )
            """)

            # 4. Imtihonlar jadvali
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Exams')
                CREATE TABLE Exams (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    ExamType NVARCHAR(50),
                    CourseName NVARCHAR(100),
                    ExamDate DATE,
                    ExamTime NVARCHAR(10),
                    Teacher NVARCHAR(100),
                    Room NVARCHAR(50)
                )
            """)
            
            # 5. Talabalar moliyasi
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Finances')
                CREATE TABLE Finances (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    StudentID INT FOREIGN KEY REFERENCES Students(ID),
                    FundingType NVARCHAR(20),
                    TotalAmount FLOAT DEFAULT 0,
                    PaidAmount FLOAT DEFAULT 0
                )
            """)
            
            conn.commit()
            print("Jadvallar muvaffaqiyatli yaratildi.")

    def get_exams(self):
        """Imtihonlar jadvalini olish"""
        query = "SELECT ExamType, CourseName, ExamDate, ExamTime, Teacher, Room FROM Exams ORDER BY ExamDate"
        exams = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                exams.append({
                    'type': row.ExamType,
                    'course': row.CourseName,
                    'date': str(row.ExamDate),
                    'time': row.ExamTime,
                    'teacher': row.Teacher,
                    'room': row.Room
                })
        return exams

    def get_finances(self):
        """Talabalar to'lov ma'lumotlarini olish"""
        query = """
            SELECT s.FullName, f.FundingType, f.TotalAmount, f.PaidAmount 
            FROM Finances f
            JOIN Students s ON f.StudentID = s.ID
        """
        finances = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                finances.append({
                    'full_name': row.FullName,
                    'type': row.FundingType,
                    'total': row.TotalAmount,
                    'paid': row.PaidAmount,
                    'debt': row.TotalAmount - row.PaidAmount
                })
        return finances

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
