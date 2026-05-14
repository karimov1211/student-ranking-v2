from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from models.rating import RatingCalculator
from database.db_manager import DatabaseManager
import pandas as pd

app = FastAPI(title="Student Ranking API")

# Fayl yo'llarini sozlash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontEnd", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontEnd", "static")), name="static")

# Next.js Front-end bilan ulanish uchun CORS ruxsatnomasi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Barcha (jumladan Next.js) manbalarga ruxsat
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root(request: Request):
    """Saytning asosiy UI qismini ochadi"""
    try:
        db = DatabaseManager()
        grades_data = db.get_all_grades()
        students_data = db.get_students()
        
        if not grades_data:
            return templates.TemplateResponse(request=request, name="index.html", context={"ranking": []})

        gpa_results = RatingCalculator.calculate_gpa(grades_data)
        students_df = pd.DataFrame(students_data)
        final_df = pd.merge(students_df, gpa_results, left_on='id', right_on='student_id', how='inner')
        final_df['gpa'] = final_df['gpa'].round(2)
        final_df = final_df.sort_values(by='gpa', ascending=False)
        
        ranking_data = final_df.to_dict(orient='records')
        return templates.TemplateResponse(request=request, name="index.html", context={"ranking": ranking_data})
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

@app.get("/api/ranking")
async def get_ranking():
    """Pandas orqali hisoblangan barcha talabalar reytingini qaytaradi"""
    db = DatabaseManager()
    grades_data = db.get_all_grades()
    students_data = db.get_students()
    
    if not grades_data:
        return {"status": "success", "data": []}

    gpa_results = RatingCalculator.calculate_gpa(grades_data)
    students_df = pd.DataFrame(students_data)
    
    final_df = pd.merge(students_df, gpa_results, left_on='id', right_on='student_id', how='inner')
    final_df['gpa'] = final_df['gpa'].round(2)
    final_df = final_df.sort_values(by='gpa', ascending=False)
    
    return {"status": "success", "data": final_df.to_dict(orient='records')}

@app.post("/api/add_student")
async def add_student(full_name: str = Form(...), major: str = Form(...), grade: float = Form(...)):
    """Yangi talaba qo'shish API'si"""
    db = DatabaseManager()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Students (FullName, Major) OUTPUT INSERTED.ID VALUES (?, ?)", (full_name, major))
        student_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT ID FROM Courses WHERE Name = 'General Test'")
        course_row = cursor.fetchone()
        if course_row:
            course_id = course_row[0]
        else:
            cursor.execute("INSERT INTO Courses (Name, Credits) OUTPUT INSERTED.ID VALUES ('General Test', 5)")
            course_id = cursor.fetchone()[0]
            
        cursor.execute("INSERT INTO Grades (StudentID, CourseID, Grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
        conn.commit()
        
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
