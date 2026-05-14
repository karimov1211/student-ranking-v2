import pandas as pd

class RatingCalculator:
    @staticmethod
    def calculate_gpa(grades_list: list) -> pd.DataFrame:
        """
        Ma'lumotlar ro'yxatini Pandas DataFrame-ga o'tkazadi va 
        vaznli GPA hisoblaydi.
        
        grades_list struktura: 
        [{'student_id': 1, 'grade': 85, 'credits': 5}, ...]
        """
        if not grades_list:
            return pd.DataFrame()

        df = pd.DataFrame(grades_list)
        
        # Vaznli ballni hisoblash (Baho * Kredit)
        df['weighted_score'] = df['grade'] * df['credits']
        
        # Talabalar bo'yicha jamlash
        result = df.groupby('student_id').agg({
            'weighted_score': 'sum',
            'credits': 'sum'
        })
        
        # GPA = Umumiy vaznli ball / Umumiy kreditlar
        result['gpa'] = result['weighted_score'] / result['credits']
        
        return result[['gpa']].reset_index()
