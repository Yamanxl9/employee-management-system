#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تحديث فلتر الوظائف مع الوظائف الجديدة من الملف المرفق
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# تحميل متغيرات البيئة
load_dotenv()

def update_jobs_filter():
    """تحديث فلتر الوظائف مع البيانات الجديدة"""
    
    # الاتصال بـ MongoDB
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client.employees_db
    
    # الوظائف الجديدة من الملف المرفق
    new_jobs = [
        {"job_code": 1, "job_eng": "Accountant", "job_ara": "محاسب"},
        {"job_code": 2, "job_eng": "Archive Clerk", "job_ara": "كاتب الأرشیف"},
        {"job_code": 3, "job_eng": "Commercial Sales Representative", "job_ara": "ممثل مبيعات تجاري"},
        {"job_code": 4, "job_eng": "Computer Engineer", "job_ara": "مھندس كومبیوتر"},
        {"job_code": 5, "job_eng": "Filing Clerk", "job_ara": "كاتب ملفات"},
        {"job_code": 6, "job_eng": "Marketing Manager", "job_ara": "مدير التسويق"},
        {"job_code": 7, "job_eng": "Messenger", "job_ara": "مراسل"},
        {"job_code": 8, "job_eng": "Operations Manager", "job_ara": "مدير عمليات"},
        {"job_code": 9, "job_eng": "Sales Manager", "job_ara": "مدیر المبیعات"},
        {"job_code": 10, "job_eng": "Shop Assistant", "job_ara": "عامل مساعد بمتجر"},
        {"job_code": 11, "job_eng": "Stall and Market Salesperson", "job_ara": "مندوب مبيعات الأكشاك والسوق"},
        {"job_code": 12, "job_eng": "Stevedore", "job_ara": "محمل سفن"},
        {"job_code": 13, "job_eng": "Legal Consultant", "job_ara": "استشاري قانوني"},
        {"job_code": 14, "job_eng": "Finance Director", "job_ara": "مدیر المالیة"},
        {"job_code": 15, "job_eng": "Administration Manager", "job_ara": "مدير ادارة"},
        {"job_code": 16, "job_eng": "Loading and unloading worker", "job_ara": "عامل الشحن والتفريغ"},
        {"job_code": 17, "job_eng": "Marketing Specialist", "job_ara": "أخصائي تسويق"},
        {"job_code": 18, "job_eng": "Storekeeper", "job_ara": "أمين مخزن"},
        {"job_code": 19, "job_eng": "General Manager", "job_ara": "مدير عام"}
    ]
    
    print("🔄 تحديث مجموعة الوظائف...")
    
    # حذف جميع الوظائف الموجودة
    result = db.jobs.delete_many({})
    print(f"✅ تم حذف {result.deleted_count} وظيفة قديمة")
    
    # إدراج الوظائف الجديدة
    result = db.jobs.insert_many(new_jobs)
    print(f"✅ تم إدراج {len(result.inserted_ids)} وظيفة جديدة")
    
    print("\n📋 الوظائف المحدثة:")
    jobs = list(db.jobs.find({}, {"_id": 0}).sort("job_code", 1))
    for job in jobs:
        print(f"   {job['job_code']:2d}: {job['job_ara']} ({job['job_eng']})")
    
    # التحقق من الموظفين الذين يحتاجون تحديث job_code
    print("\n🔍 التحقق من job_codes للموظفين...")
    employees_with_invalid_jobs = list(db.employees.find(
        {"job_code": {"$nin": [job["job_code"] for job in new_jobs]}},
        {"staff_no": 1, "staff_name_ara": 1, "job_code": 1}
    ).limit(10))
    
    if employees_with_invalid_jobs:
        print(f"⚠️  وُجد {len(employees_with_invalid_jobs)} موظف مع job_code غير صحيح:")
        for emp in employees_with_invalid_jobs:
            print(f"   - {emp.get('staff_name_ara', '?')}: job_code = {emp.get('job_code', '?')}")
    else:
        print("✅ جميع الموظفين لديهم job_codes صحيحة")
    
    client.close()
    print("\n🎉 تم تحديث فلتر الوظائف بنجاح!")

if __name__ == "__main__":
    update_jobs_filter()
