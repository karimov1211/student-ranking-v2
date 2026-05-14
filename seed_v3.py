from database.db_manager import DatabaseManager
from datetime import date

def seed_extended_data():
    db = DatabaseManager()
    db.init_db()
    
    # 1. Imtihonlarni qo'shish (Rasmga asosan)
    exams = [
        ("Oraliq nazorat", "Ehtimollar nazariyasi", date(2026, 4, 15), "14:00", "BEKMETOVA SADOQAT", "5-2-Zal"),
        ("Oraliq nazorat", "Nazariy mexanika", date(2026, 4, 16), "12:30", "SHARIPOVA SHOHISTA", "5-2-Zal"),
        ("Oraliq nazorat", "Dinshunoslik", date(2026, 4, 16), "14:00", "KOMILOV ABROR", "S-6-Zal"),
        ("Oraliq nazorat", "Algoritmik tillar", date(2026, 4, 17), "14:00", "AVEZMATOV IXTIYOR", "5-2-Zal"),
        ("Oraliq nazorat", "Differensial tenglamalar", date(2026, 4, 18), "12:30", "BABAJANOV BAZAR", "S-6-Zal"),
        ("Oraliq nazorat", "Umumiy pedagogika", date(2026, 4, 24), "15:30", "XAMRAYEVA UMIDA", "S-6-Zal"),
        ("Yakuniy nazorat", "Umumiy pedagogika", date(2026, 5, 18), "09:00", "SHERJANOVA NODIRA", "S-4-Zal")
    ]
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Imtihonlarni kiritish
        for ex in exams:
            cursor.execute("""
                INSERT INTO Exams (ExamType, CourseName, ExamDate, ExamTime, Teacher, Room)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ex)
        
        # 2. Moliya ma'lumotlarini kiritish (Talabalar bo'lsa)
        cursor.execute("SELECT ID FROM Students")
        student_ids = [row[0] for row in cursor.fetchall()]
        
        if student_ids:
            for s_id in student_ids:
                # Tasodifiy Grant yoki Kontrakt
                f_type = "Grant" if s_id % 5 == 0 else "Kontrakt"
                total = 0 if f_type == "Grant" else 9800000
                paid = 0 if f_type == "Grant" else (total if s_id % 2 == 0 else 5000000)
                
                cursor.execute("""
                    INSERT INTO Finances (StudentID, FundingType, TotalAmount, PaidAmount)
                    VALUES (?, ?, ?, ?)
                """, (s_id, f_type, total, paid))
        
        conn.commit()
    print("Yangi ma'lumotlar muvaffaqiyatli kiritildi!")

if __name__ == "__main__":
    seed_extended_data()
