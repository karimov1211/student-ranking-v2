from database.db_manager import DatabaseManager
import random

def seed_provided_students():
    db = DatabaseManager()
    # Jadvallarni tekshirish/yaratish
    db.init_db()
    
    students_list = [
        "Abdullayev Bahriddin Bekturdi o'g'li",
        "Artiqova Malika G'ayrat qizi",
        "Bog'ibekov Oybek Bekpo'lat o'g'li",
        "Baxtiyarova Nafisa Murod qizi",
        "Boltabayeva Zuxra Hamidjon qizi",
        "Gulimova Sarvinoz Mansurbek qizi",
        "Jabbarova Shaydo Anvar qizi",
        "Janibekov Sherzod Farxod o'g'li",
        "Komilova Nilufar Behzod qizi",
        "Kuryazova Laylo Bahodir qizi",
        "Nuraddinova Munira Dilshod qizi",
        "Ochilboyev Fayzulla Xayrulla o'g'li",
        "Ochilova Moxinur Xudayshukur qizi",
        "Olimboyeva Xolida Jamol qizi",
        "O'rinova O'g'iljon Umrbek qizi",
        "Qazaqova Gulruxsora Muzaffar qizi",
        "Raximova Mashxura Muzaffar qizi",
        "Romonberdiyev Farmon Diyor o'g'li",
        "Ro'ziboyeva Elnura Ergashbek qizi",
        "Ro'zimova Charosxon Ergash qizi",
        "Sa'dullayeva Oygul Muzaffar qizi",
        "Saparboyev Javoxir Shuxratjon o'g'li",
        "Sheripboyeva Gulmira Otabek qizi",
        "Tillayev Farruxbek Nodirbekovich"
    ]
    
    major = "Dasturiy muhandislik"
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Test kursini tekshirish
        cursor.execute("SELECT ID FROM Courses WHERE Name = 'Algoritmlar'")
        course_row = cursor.fetchone()
        if course_row:
            course_id = course_row[0]
        else:
            cursor.execute("INSERT INTO Courses (Name, Credits) OUTPUT INSERTED.ID VALUES ('Algoritmlar', 5)")
            course_id = cursor.fetchone()[0]
            
        for name in students_list:
            # Talabani qo'shish
            cursor.execute("INSERT INTO Students (FullName, Major) OUTPUT INSERTED.ID VALUES (?, ?)", (name, major))
            student_id = cursor.fetchone()[0]
            
            # Bahosini qo'shish (tasodifiy 70-98 oraliqda)
            grade = random.uniform(70, 98)
            cursor.execute("INSERT INTO Grades (StudentID, CourseID, Grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
            
        conn.commit()
    print(f"{len(students_list)} ta talaba muvaffaqiyatli qo'shildi!")

if __name__ == "__main__":
    seed_provided_students()
