from app.db_helper import DBHelper

db = DBHelper()

questions = [
    {"question": "حاصل ۵ + ۳ × ۲ چیست؟", "options": ["۱۶", "۱۳", "۱۰", "۸"]},
    {"question": "عدد اول کدام است؟", "options": ["۴", "۶", "۹", "۷"]},
    {"question": "کدام عدد بر ۳ و ۴ بخش‌پذیر است؟", "options": ["۱۲", "۱۵", "۱۸", "۲۴"]},
    {"question": "۳/۴ به صورت اعشاری چیست؟", "options": ["۰.۲۵", "۰.۵", "۰.۷۵", "۱"]},
    {"question": "مساحت مربع با ضلع ۶ چیست؟", "options": ["۱۲", "۱۸", "۲۴", "۳۶"]},
    {"question": "مضرب ۵ بین ۲۵ تا ۳۵؟", "options": ["۲۶", "۲۷", "۳۰", "۳۳"]},
    {"question": "۱۲۳ منهای ۸۵ چند می‌شود؟", "options": ["۳۸", "۴۸", "۵۸", "۶۸"]},
    {"question": "زاویه قائمه چند درجه است؟", "options": ["۴۵", "۶۰", "۹۰", "۱۸۰"]},
    {"question": "۴۵٪ از ۲۰۰ چقدر می‌شود؟", "options": ["۷۰", "۸۰", "۹۰", "۱۰۰"]},
    {"question": "اگر محیط مستطیل ۲۰ و طول ۶ باشد، عرض چیست؟", "options": ["۲", "۴", "۵", "۶"]},
]
correct_answers = {
    "q1": 2, "q2": 4, "q3": 1, "q4": 3, "q5": 4,
    "q6": 3, "q7": 1, "q8": 3, "q9": 3, "q10": 3
}

success = db.exam.add_exam(planet_id=1, questions=questions, correct_answers=correct_answers)

if success:
    print("✅")
else:
    print("❌")
