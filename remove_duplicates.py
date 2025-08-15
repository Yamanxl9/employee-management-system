#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت لإزالة التكرارات من قاعدة البيانات
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from collections import defaultdict

# تحميل متغيرات البيئة
load_dotenv()

# الاتصال بقاعدة البيانات
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
client = MongoClient(MONGODB_URI)
db = client.get_database()

def remove_employee_duplicates():
    """إزالة الموظفين المكررين بناءً على staff_no"""
    print("بدء فحص الموظفين المكررين...")
    
    # العثور على الموظفين المكررين
    pipeline = [
        {
            "$group": {
                "_id": "$staff_no",
                "count": {"$sum": 1},
                "docs": {"$push": "$$ROOT"}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]
    
    duplicates = list(db.employees.aggregate(pipeline))
    
    if not duplicates:
        print("✅ لا توجد موظفين مكررين")
        return
    
    total_removed = 0
    
    for duplicate_group in duplicates:
        staff_no = duplicate_group["_id"]
        docs = duplicate_group["docs"]
        count = duplicate_group["count"]
        
        print(f"🔍 وجد {count} نسخ للموظف رقم: {staff_no}")
        
        # الاحتفاظ بأحدث نسخة وحذف الباقي
        docs_sorted = sorted(docs, key=lambda x: x.get('create_date_time', ''), reverse=True)
        keep_doc = docs_sorted[0]
        remove_docs = docs_sorted[1:]
        
        for doc in remove_docs:
            result = db.employees.delete_one({"_id": doc["_id"]})
            if result.deleted_count > 0:
                total_removed += 1
                print(f"   ❌ حُذفت نسخة مكررة للموظف: {staff_no}")
    
    print(f"✅ تم حذف {total_removed} موظف مكرر")

def remove_company_duplicates():
    """إزالة الشركات المكررة بناءً على company_code"""
    print("\nبدء فحص الشركات المكررة...")
    
    pipeline = [
        {
            "$group": {
                "_id": "$company_code",
                "count": {"$sum": 1},
                "docs": {"$push": "$$ROOT"}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]
    
    duplicates = list(db.companies.aggregate(pipeline))
    
    if not duplicates:
        print("✅ لا توجد شركات مكررة")
        return
    
    total_removed = 0
    
    for duplicate_group in duplicates:
        company_code = duplicate_group["_id"]
        docs = duplicate_group["docs"]
        count = duplicate_group["count"]
        
        print(f"🔍 وجد {count} نسخ للشركة رقم: {company_code}")
        
        # الاحتفاظ بأول نسخة وحذف الباقي
        keep_doc = docs[0]
        remove_docs = docs[1:]
        
        for doc in remove_docs:
            result = db.companies.delete_one({"_id": doc["_id"]})
            if result.deleted_count > 0:
                total_removed += 1
                print(f"   ❌ حُذفت نسخة مكررة للشركة: {company_code}")
    
    print(f"✅ تم حذف {total_removed} شركة مكررة")

def remove_job_duplicates():
    """إزالة الوظائف المكررة بناءً على job_code"""
    print("\nبدء فحص الوظائف المكررة...")
    
    pipeline = [
        {
            "$group": {
                "_id": "$job_code",
                "count": {"$sum": 1},
                "docs": {"$push": "$$ROOT"}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]
    
    duplicates = list(db.jobs.aggregate(pipeline))
    
    if not duplicates:
        print("✅ لا توجد وظائف مكررة")
        return
    
    total_removed = 0
    
    for duplicate_group in duplicates:
        job_code = duplicate_group["_id"]
        docs = duplicate_group["docs"]
        count = duplicate_group["count"]
        
        print(f"🔍 وجد {count} نسخ للوظيفة رقم: {job_code}")
        
        # الاحتفاظ بأول نسخة وحذف الباقي
        keep_doc = docs[0]
        remove_docs = docs[1:]
        
        for doc in remove_docs:
            result = db.jobs.delete_one({"_id": doc["_id"]})
            if result.deleted_count > 0:
                total_removed += 1
                print(f"   ❌ حُذفت نسخة مكررة للوظيفة: {job_code}")
    
    print(f"✅ تم حذف {total_removed} وظيفة مكررة")

def show_statistics():
    """عرض إحصائيات قاعدة البيانات"""
    print("\n📊 إحصائيات قاعدة البيانات:")
    
    employees_count = db.employees.count_documents({})
    companies_count = db.companies.count_documents({})
    jobs_count = db.jobs.count_documents({})
    
    print(f"   👥 عدد الموظفين: {employees_count}")
    print(f"   🏢 عدد الشركات: {companies_count}")
    print(f"   💼 عدد الوظائف: {jobs_count}")

def main():
    """الدالة الرئيسية"""
    print("🧹 بدء عملية تنظيف قاعدة البيانات...")
    print("=" * 50)
    
    # عرض الإحصائيات قبل التنظيف
    print("📈 الإحصائيات قبل التنظيف:")
    show_statistics()
    
    # إزالة التكرارات
    remove_employee_duplicates()
    remove_company_duplicates()
    remove_job_duplicates()
    
    # عرض الإحصائيات بعد التنظيف
    print("\n📉 الإحصائيات بعد التنظيف:")
    show_statistics()
    
    print("\n✅ تم الانتهاء من تنظيف قاعدة البيانات!")

if __name__ == "__main__":
    main()
