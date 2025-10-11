#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت لإضافة الموظفين الجدد من ملف JSON إلى قاعدة البيانات
"""

import json
import os
from datetime import datetime
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from nationalities import NATIONALITIES

# تحميل متغيرات البيئة
load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
mongo = PyMongo(app)

def get_nationality_display(nationality_code):
    """الحصول على اسم الجنسية للعرض"""
    if not nationality_code:
        return ""
    
    nationality_info = NATIONALITIES.get(nationality_code, {})
    arabic_name = nationality_info.get('ar', '')
    english_name = nationality_info.get('en', '')
    
    if arabic_name and english_name:
        return f"{arabic_name} - {english_name}"
    elif arabic_name:
        return arabic_name
    elif english_name:
        return english_name
    else:
        return nationality_code

def add_employees_from_json(json_file_path):
    """إضافة الموظفين من ملف JSON"""
    
    try:
        # قراءة ملف JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            employees_data = json.load(file)
        
        print(f"تم العثور على {len(employees_data)} موظف في الملف")
        
        # إحصائيات
        added_count = 0
        updated_count = 0
        skipped_count = 0
        
        with app.app_context():
            for employee in employees_data:
                try:
                    # التحقق من وجود الموظف
                    existing_employee = mongo.db.employees.find_one({
                        'staff_no': employee['staff_no']
                    })
                    
                    # تحضير بيانات الموظف
                    employee_data = {
                        'staff_no': employee['staff_no'],
                        'staff_name': employee['staff_name'],
                        'staff_name_ara': employee['staff_name_ara'],
                        'job_name': employee['job_name'],
                        'pass_no': employee['pass_no'],
                        'nationality_code': employee['nationality_code'],
                        'nationality_display': get_nationality_display(employee['nationality_code']),
                        'company_code': employee['company_code'],
                        'card_no': employee['card_no'],
                        'card_expiry_date': employee['card_expiry_date'],
                        'passport_status': employee.get('passport_status', ''),
                        'card_status': employee.get('card_status', ''),
                        'create_date_time': employee['create_date_time'],
                        'last_updated': datetime.utcnow().isoformat()
                    }
                    
                    if existing_employee:
                        # تحديث الموظف الموجود
                        result = mongo.db.employees.update_one(
                            {'staff_no': employee['staff_no']},
                            {'$set': employee_data}
                        )
                        if result.modified_count > 0:
                            updated_count += 1
                            print(f"تم تحديث الموظف: {employee['staff_name']}")
                        else:
                            skipped_count += 1
                    else:
                        # إضافة موظف جديد
                        mongo.db.employees.insert_one(employee_data)
                        added_count += 1
                        print(f"تم إضافة الموظف الجديد: {employee['staff_name']}")
                        
                except Exception as e:
                    print(f"خطأ في معالجة الموظف {employee.get('staff_name', 'غير معروف')}: {str(e)}")
                    skipped_count += 1
        
        print(f"\n=== ملخص العملية ===")
        print(f"تم إضافة {added_count} موظف جديد")
        print(f"تم تحديث {updated_count} موظف موجود")
        print(f"تم تخطي {skipped_count} موظف")
        print(f"إجمالي المعالجة: {added_count + updated_count + skipped_count}")
        
        return True
        
    except Exception as e:
        print(f"خطأ في قراءة الملف أو الاتصال بقاعدة البيانات: {str(e)}")
        return False

if __name__ == "__main__":
    # مسار ملف JSON
    json_file = r"c:\Users\yaman_alne0q1\Downloads\deepseek_json_20250815_15ef13.json"
    
    if os.path.exists(json_file):
        print("بدء إضافة الموظفين...")
        success = add_employees_from_json(json_file)
        if success:
            print("تمت العملية بنجاح! ✅")
        else:
            print("فشلت العملية! ❌")
    else:
        print(f"لم يتم العثور على الملف: {json_file}")
