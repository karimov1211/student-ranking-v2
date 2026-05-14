from db_manager import DatabaseManager
import random

def seed_database():
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Talabalar qo'shish
        students = [
            ("Aziz Karimov", "Software Engineering"),
            ("Malika Ergasheva", "Data Science"),
            ("Jasur Rahimov", "Cyber Security")
        ]
        
        # Agar jadval bo'sh bo'lsa qo'shamiz
        cursor.execute("SELECT COUNT(*) FROM Students")
        if cursor.fetchone()[0] == 0:
            for s in students:
                cursor.execute("INSERT INTO Students (FullName, Major) VALUES (?, ?)", s)
            print("Talabalar qo'shildi.")
        
        # 2. Fanlar qo'shish
        courses = [
            ("Mathematics", 5),
            ("Programming", 6),
            ("Database Systems", 4),
            ("Physics", 3)
        ]
        
        cursor.execute("SELECT COUNT(*) FROM Courses")
        if cursor.fetchone()[0] == 0:
            for c in courses:
                cursor.execute("INSERT INTO Courses (Name, Credits) VALUES (?, ?)", c)
            print("Fanlar qo'shildi.")
            
        # 3. Baholar qo'shish
        cursor.execute("SELECT COUNT(*) FROM Grades")
        if cursor.fetchone()[0] == 0:
            cursor.execute("SELECT ID FROM Students")
            student_ids = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT ID FROM Courses")
            course_ids = [row[0] for row in cursor.fetchall()]
            
            for s_id in student_ids:
                for c_id in course_ids:
                    grade = random.randint(60, 100)
                    cursor.execute("INSERT INTO Grades (StudentID, CourseID, Grade) VALUES (?, ?, ?)", (s_id, c_id, grade))
            print("Baholar qo'shildi.")
            
        conn.commit()
    print("Ma'lumotlarni yuklash yakunlandi!")

if __name__ == "__main__":
    seed_database()
