#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت محدث لإضافة الموظفين الجدد مع معالجة الاختلافات في أسماء الحقول
"""

import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from nationalities import NATIONALITIES

# تحميل متغيرات البيئة
load_dotenv()

# الاتصال بقاعدة البيانات
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
client = MongoClient(MONGODB_URI)
db = client.get_database()

def get_job_code_from_name(job_name):
    """الحصول على job_code من job_name"""
    job = db.jobs.find_one({"job_eng": job_name})
    if job:
        return job['job_code']
    
    # إذا لم توجد الوظيفة، أنشئها
    max_job = db.jobs.find_one(sort=[("job_code", -1)])
    new_job_code = str(int(max_job['job_code']) + 1) if max_job else "21"
    
    new_job = {
        'job_code': new_job_code,
        'job_eng': job_name,
        'job_ara': job_name  # مؤقتاً حتى يتم ترجمتها يدوياً
    }
    
    db.jobs.insert_one(new_job)
    print(f"   ➕ أُضيفت وظيفة جديدة: {job_name} (كود: {new_job_code})")
    return new_job_code

def get_nationality_info(nationality_code):
    """الحصول على معلومات الجنسية"""
    if nationality_code in NATIONALITIES:
        return {
            'nationality_ar': NATIONALITIES[nationality_code]['ar'],
            'nationality_en': NATIONALITIES[nationality_code]['en']
        }
    else:
        return {
            'nationality_ar': nationality_code,
            'nationality_en': nationality_code
        }

def convert_new_employee_format(new_emp):
    """تحويل تنسيق الموظف الجديد إلى تنسيق قاعدة البيانات"""
    
    # الحصول على job_code من job_name
    job_code = get_job_code_from_name(new_emp.get('job_name', ''))
    
    # الحصول على معلومات الجنسية
    nationality_info = get_nationality_info(new_emp.get('nationality_code', ''))
    
    # تحويل التنسيق
    converted_emp = {
        'staff_no': new_emp.get('staff_no'),
        'staff_name': new_emp.get('staff_name'),
        'staff_name_ara': new_emp.get('staff_name_ara'),
        'job_code': job_code,
        'pass_no': new_emp.get('pass_no'),
        'nationality_code': new_emp.get('nationality_code'),
        'nationality_ar': nationality_info['nationality_ar'],
        'nationality_en': nationality_info['nationality_en'],
        'company_code': new_emp.get('company_code'),
        'card_no': new_emp.get('card_no'),
        'card_expiry_date': new_emp.get('card_expiry_date'),
        'create_date_time': new_emp.get('create_date_time', datetime.now().isoformat())
    }
    
    # إزالة القيم الفارغة
    converted_emp = {k: v for k, v in converted_emp.items() if v is not None and v != ''}
    
    return converted_emp

def add_new_employees():
    """إضافة الموظفين الجدد"""
    print("📂 قراءة الملف الجديد...")
    
    try:
        with open(r'c:\Users\yaman_alne0q1\Downloads\deepseek_json_20250815_15ef13.json', 'r', encoding='utf-8') as f:
            new_employees = json.load(f)
        
        print(f"📊 وجد {len(new_employees)} موظف في الملف الجديد")
        
        added_count = 0
        updated_count = 0
        error_count = 0
        
        for i, new_emp in enumerate(new_employees, 1):
            try:
                staff_no = new_emp.get('staff_no')
                if not staff_no:
                    print(f"   ❌ موظف رقم {i}: لا يوجد staff_no")
                    error_count += 1
                    continue
                
                # فحص إذا كان الموظف موجود
                existing_emp = db.employees.find_one({'staff_no': staff_no})
                
                # تحويل التنسيق
                converted_emp = convert_new_employee_format(new_emp)
                
                if existing_emp:
                    # تحديث الموظف الموجود
                    db.employees.update_one(
                        {'staff_no': staff_no},
                        {'$set': converted_emp}
                    )
                    updated_count += 1
                    print(f"   🔄 محدث: {staff_no} - {new_emp.get('staff_name', 'N/A')}")
                else:
                    # إضافة موظف جديد
                    db.employees.insert_one(converted_emp)
                    added_count += 1
                    print(f"   ✅ أُضيف: {staff_no} - {new_emp.get('staff_name', 'N/A')}")
                
            except Exception as e:
                error_count += 1
                print(f"   ❌ خطأ في الموظف رقم {i}: {e}")
        
        print(f"\n📈 النتائج النهائية:")
        print(f"   ✅ تمت إضافة: {added_count} موظف")
        print(f"   🔄 تم تحديث: {updated_count} موظف")
        print(f"   ❌ أخطاء: {error_count} موظف")
        
        return added_count + updated_count
        
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return 0

def show_final_stats():
    """عرض الإحصائيات النهائية"""
    print("\n📊 إحصائيات قاعدة البيانات بعد التحديث:")
    
    employees_count = db.employees.count_documents({})
    companies_count = db.companies.count_documents({})
    jobs_count = db.jobs.count_documents({})
    
    print(f"   👥 عدد الموظفين: {employees_count}")
    print(f"   🏢 عدد الشركات: {companies_count}")
    print(f"   💼 عدد الوظائف: {jobs_count}")

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إضافة الموظفين الجدد مع معالجة الاختلافات...")
    print("=" * 60)
    
    # إضافة الموظفين
    processed_count = add_new_employees()
    
    # عرض الإحصائيات النهائية
    show_final_stats()
    
    print(f"\n✅ تم الانتهاء! تمت معالجة {processed_count} موظف.")

if __name__ == "__main__":
    main()
