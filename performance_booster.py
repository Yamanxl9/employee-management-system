#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحسينات شاملة لأداء البحث والتقارير
Performance Optimizations for Search and Reports
"""

import os
import time
from pymongo import MongoClient, ASCENDING, TEXT, DESCENDING
from config import MONGO_URI

def create_performance_indexes():
    """إنشاء فهارس محسنة للأداء"""
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        
        print("🔄 إنشاء فهارس الأداء...")
        
        # فهرس نصي شامل للبحث السريع
        try:
            db.employees.drop_index("text_search_index")
        except:
            pass
            
        db.employees.create_index([
            ("staff_name", TEXT),
            ("staff_name_ara", TEXT),
            ("staff_no", TEXT),
            ("pass_no", TEXT),
            ("card_no", TEXT),
            ("emirates_id", TEXT),
            ("residence_no", TEXT)
        ], name="optimized_text_search")
        
        # فهارس مفردة للفلاتر
        db.employees.create_index([("nationality_code", ASCENDING)], name="nationality_idx")
        db.employees.create_index([("company_code", ASCENDING)], name="company_idx") 
        db.employees.create_index([("job_code", ASCENDING)], name="job_idx")
        db.employees.create_index([("department_code", ASCENDING)], name="department_idx")
        
        # فهارس للتواريخ
        db.employees.create_index([("card_expiry_date", ASCENDING)], name="card_expiry_idx")
        db.employees.create_index([("emirates_id_expiry", ASCENDING)], name="emirates_expiry_idx")
        db.employees.create_index([("residence_expiry_date", ASCENDING)], name="residence_expiry_idx")
        
        # فهارس مركبة للاستعلامات المعقدة
        db.employees.create_index([
            ("company_code", ASCENDING),
            ("department_code", ASCENDING),
            ("job_code", ASCENDING)
        ], name="company_dept_job_idx")
        
        # فهرس للترقيم والصفحات
        db.employees.create_index([("staff_no", ASCENDING)], name="staff_no_idx")
        
        # فهارس للجداول المرجعية
        db.companies.create_index([("company_code", ASCENDING)], name="companies_code_idx")
        db.jobs.create_index([("job_code", ASCENDING)], name="jobs_code_idx")
        db.department.create_index([("department_code", ASCENDING)], name="dept_code_idx")
        
        print("✅ تم إنشاء جميع فهارس الأداء بنجاح!")
        
        # عرض إحصائيات الفهارس
        indexes = list(db.employees.list_indexes())
        print(f"📊 عدد الفهارس: {len(indexes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الفهارس: {e}")
        return False
    finally:
        client.close()

def optimize_collection_settings():
    """تحسين إعدادات المجموعات"""
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        
        print("🔄 تحسين إعدادات المجموعات...")
        
        # تحسين مجموعة الموظفين
        db.employees.create_index([("_id", ASCENDING)])
        
        # إحصائيات سريعة
        employee_count = db.employees.count_documents({})
        company_count = db.companies.count_documents({})
        job_count = db.jobs.count_documents({})
        dept_count = db.department.count_documents({})
        
        print(f"📈 إحصائيات البيانات:")
        print(f"   - الموظفين: {employee_count:,}")
        print(f"   - الشركات: {company_count}")
        print(f"   - الوظائف: {job_count}")
        print(f"   - الأقسام: {dept_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحسين الإعدادات: {e}")
        return False
    finally:
        client.close()

def test_search_performance():
    """اختبار أداء البحث"""
    try:
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        
        print("🧪 اختبار أداء البحث...")
        
        # اختبار البحث النصي
        start_time = time.time()
        results = list(db.employees.find({"$text": {"$search": "محمد"}}).limit(10))
        text_search_time = time.time() - start_time
        
        # اختبار البحث بالفلتر
        start_time = time.time()
        results = list(db.employees.find({"nationality_code": "ARE"}).limit(10))
        filter_search_time = time.time() - start_time
        
        # اختبار البحث المركب
        start_time = time.time()
        results = list(db.employees.find({
            "company_code": "001",
            "department_code": "HR"
        }).limit(10))
        compound_search_time = time.time() - start_time
        
        print(f"⚡ نتائج اختبار الأداء:")
        print(f"   - البحث النصي: {text_search_time:.3f} ثانية")
        print(f"   - البحث بالفلتر: {filter_search_time:.3f} ثانية") 
        print(f"   - البحث المركب: {compound_search_time:.3f} ثانية")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الأداء: {e}")
        return False
    finally:
        client.close()

if __name__ == "__main__":
    print("🚀 بدء تحسين الأداء الشامل...")
    
    success = True
    
    # إنشاء الفهارس
    if not create_performance_indexes():
        success = False
    
    # تحسين الإعدادات  
    if not optimize_collection_settings():
        success = False
        
    # اختبار الأداء
    if not test_search_performance():
        success = False
    
    if success:
        print("✅ تم إكمال تحسين الأداء بنجاح!")
        print("🎯 الموقع سيكون أسرع بشكل ملحوظ الآن!")
    else:
        print("❌ حدثت بعض الأخطاء أثناء التحسين")
