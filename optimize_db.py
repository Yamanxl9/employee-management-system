#!  /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحسين أداء قاعدة البيانات
يقوم بإنشاء فهارس للبحث السريع
"""

import os
from pymongo import MongoClient, ASCENDING, TEXT
from config import MONGODB_URI

def create_indexes():
    """إنشاء فهارس لتحسين الأداء"""
    try:
        # الاتصال بقاعدة البيانات
        client = MongoClient(MONGODB_URI)
        db = client.get_default_database()
        
        print("🔄 إنشاء فهارس لتحسين الأداء...")
        
        # فهارس مجموعة الموظفين
        employees = db.employees
        
        # فهرس نصي للبحث السريع
        employees.create_index([
            ("staff_name", TEXT),
            ("staff_name_ara", TEXT),
            ("staff_no", TEXT),
            ("pass_no", TEXT),
            ("card_no", TEXT),
            ("emirates_id", TEXT),
            ("residence_no", TEXT)
        ], name="text_search_index")
        
        # فهارس للحقول المستخدمة في البحث والفلترة
        employees.create_index([("staff_no", ASCENDING)], name="staff_no_index")
        employees.create_index([("nationality_code", ASCENDING)], name="nationality_index")
        employees.create_index([("company_code", ASCENDING)], name="company_index")
        employees.create_index([("job_code", ASCENDING)], name="job_index")
        employees.create_index([("department_code", ASCENDING)], name="department_index")
        employees.create_index([("card_expiry_date", ASCENDING)], name="card_expiry_index")
        employees.create_index([("emirates_id_expiry_date", ASCENDING)], name="emirates_expiry_index")
        employees.create_index([("residence_expiry_date", ASCENDING)], name="residence_expiry_index")
        
        # فهارس مركبة للاستعلامات المعقدة
        employees.create_index([
            ("company_code", ASCENDING),
            ("department_code", ASCENDING)
        ], name="company_department_index")
        
        employees.create_index([
            ("nationality_code", ASCENDING),
            ("job_code", ASCENDING)
        ], name="nationality_job_index")
        
        # فهارس للمجموعات الأخرى
        db.companies.create_index([("company_code", ASCENDING)], name="company_code_index")
        db.jobs.create_index([("job_code", ASCENDING)], name="job_code_index")
        db.department.create_index([("department_code", ASCENDING)], name="dept_code_index")
        db.audit_logs.create_index([("timestamp", ASCENDING)], name="timestamp_index")
        
        print("✅ تم إنشاء جميع الفهارس بنجاح!")
        
        # عرض الفهارس المُنشأة
        print("\n📊 الفهارس المُنشأة:")
        for index in employees.list_indexes():
            print(f"  - {index['name']}: {index.get('key', {})}")
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء الفهارس: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    create_indexes()
