import pymongo
from pymongo import MongoClient

try:
    client = MongoClient('mongodb+srv://yamanxl9:1997@cluster0.uquwf.mongodb.net/?retryWrites=true&w=majority')
    db = client.employees_db
    
    # البحث عن الموظف التركي
    turkish_emp = list(db.employees.find({'nationality_code': 'TR'}))
    print(f'عدد الموظفين برمز TR: {len(turkish_emp)}')
    
    if turkish_emp:
        for emp in turkish_emp:
            print(f'الاسم: {emp.get("staff_name", "")} - الجنسية: {emp.get("nationality_code", "")}')
    
    # البحث عن أي موظف يحتوي على كلمة Turkish في أي حقل
    turkish_search = list(db.employees.find({
        '$or': [
            {'nationality_code': {'$regex': 'Turkish', '$options': 'i'}},
            {'staff_name': {'$regex': 'Turkish', '$options': 'i'}},
            {'staff_name_ara': {'$regex': 'Turkish', '$options': 'i'}}
        ]
    }))
    print(f'عدد الموظفين بكلمة Turkish: {len(turkish_search)}')
    
    print('جميع الجنسيات الموجودة:')
    nationalities = db.employees.distinct('nationality_code')
    for nat in sorted(nationalities):
        if nat:
            print(f'- {nat}')
            
except Exception as e:
    print(f'خطأ: {e}')
