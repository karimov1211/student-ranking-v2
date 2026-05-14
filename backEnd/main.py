from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# Modellarni import qilish
from models.rating import RatingCalculator

app = FastAPI()

# Fayl yo'llarini sozlash (frontEnd papkasiga yo'naltiramiz)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "frontEnd", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "frontEnd", "static")), name="static")

@app.get("/")
async def read_root(request: Request):
    # Test ma'lumotlari (Hozircha baza yo'q)
    test_grades = [
        {'student_id': 1, 'grade': 90, 'credits': 5},
        {'student_id': 1, 'grade': 80, 'credits': 3},
        {'student_id': 2, 'grade': 95, 'credits': 5},
        {'student_id': 2, 'grade': 70, 'credits': 3},
    ]
    
    # Pandas orqali GPA hisoblash
    gpa_results = RatingCalculator.calculate_gpa(test_grades)
    ranking_data = gpa_results.to_dict(orient='records')
    
    return templates.TemplateResponse("index.html", {"request": request, "ranking": ranking_data})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
