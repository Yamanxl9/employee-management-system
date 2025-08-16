#!/usr/bin/env python3
# اختبار سريع لقاعدة البيانات

from config import MONGO_URI
from pymongo import MongoClient

try:
    client = MongoClient(MONGO_URI)
    db = client.employee_management
    
    jobs_count = db.jobs.count_documents({})
    companies_count = db.companies.count_documents({})
    employees_count = db.employees.count_documents({})
    
    print("🗃️ حالة قاعدة البيانات:")
    print(f"📋 الوظائف: {jobs_count} وظيفة")
    print(f"🏢 الشركات: {companies_count} شركة") 
    print(f"👥 الموظفين: {employees_count} موظف")
    
    print("\n✅ قاعدة البيانات جاهزة للاستخدام!")
    
    if jobs_count >= 22 and companies_count >= 7:
        print("🎉 جميع البيانات متوفرة - النظام جاهز 100%!")
    else:
        print("⚠️ قد تكون هناك بيانات مفقودة")
        
    client.close()
        
except Exception as e:
    print(f"❌ خطأ في قاعدة البيانات: {e}")
