#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت للتحقق من بنية قاعدة البيانات ومقارنتها مع الملف الجديد
"""

import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# الاتصال بقاعدة البيانات
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
client = MongoClient(MONGODB_URI)
db = client.get_database()

def check_current_structure():
    """فحص بنية قاعدة البيانات الحالية"""
    print("🔍 فحص بنية قاعدة البيانات الحالية...")
    
    # فحص بنية الموظفين
    emp = db.employees.find_one()
    if emp:
        print("\n📋 حقول الموظفين الحالية:")
        for key in sorted(emp.keys()):
            print(f"   - {key}")
    
    # فحص بنية الوظائف
    job = db.jobs.find_one()
    if job:
        print("\n💼 حقول الوظائف الحالية:")
        for key in sorted(job.keys()):
            print(f"   - {key}")
    
    return emp

def check_new_file_structure():
    """فحص بنية الملف الجديد"""
    print("\n🆕 فحص بنية الملف الجديد...")
    
    try:
        with open(r'c:\Users\yaman_alne0q1\Downloads\deepseek_json_20250815_15ef13.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data and len(data) > 0:
            new_emp = data[0]
            print(f"\n📄 حقول الملف الجديد (عدد السجلات: {len(data)}):")
            for key in sorted(new_emp.keys()):
                print(f"   - {key}")
            
            return new_emp, data
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        return None, None

def compare_structures(current_emp, new_emp):
    """مقارنة البنيتين"""
    print("\n🔄 مقارنة البنيتين...")
    
    current_fields = set(current_emp.keys()) if current_emp else set()
    new_fields = set(new_emp.keys()) if new_emp else set()
    
    # الحقول الموجودة في الحالي وليس في الجديد
    missing_in_new = current_fields - new_fields
    if missing_in_new:
        print(f"\n❌ حقول موجودة في قاعدة البيانات وغير موجودة في الملف الجديد:")
        for field in sorted(missing_in_new):
            print(f"   - {field}")
    
    # الحقول الموجودة في الجديد وليس في الحالي
    new_fields_only = new_fields - current_fields
    if new_fields_only:
        print(f"\n🆕 حقول جديدة في الملف:")
        for field in sorted(new_fields_only):
            print(f"   - {field}")
    
    # الحقول المشتركة
    common_fields = current_fields & new_fields
    if common_fields:
        print(f"\n✅ حقول مشتركة ({len(common_fields)}):")
        for field in sorted(common_fields):
            print(f"   - {field}")

def check_job_mapping():
    """فحص تطابق الوظائف"""
    print("\n💼 فحص تطابق الوظائف...")
    
    # جمع جميع job_name من الملف الجديد
    try:
        with open(r'c:\Users\yaman_alne0q1\Downloads\deepseek_json_20250815_15ef13.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        job_names = set()
        for emp in data:
            if emp.get('job_name'):
                job_names.add(emp['job_name'])
        
        print(f"🔍 وجدت {len(job_names)} وظيفة فريدة في الملف الجديد:")
        for job in sorted(job_names):
            print(f"   - {job}")
        
        # فحص الوظائف الموجودة في قاعدة البيانات
        existing_jobs = list(db.jobs.find({}, {'job_eng': 1, 'job_ara': 1, 'job_code': 1}))
        print(f"\n💾 الوظائف الموجودة في قاعدة البيانات ({len(existing_jobs)}):")
        for job in existing_jobs:
            print(f"   - {job.get('job_code', 'N/A')}: {job.get('job_eng', 'N/A')} | {job.get('job_ara', 'N/A')}")
        
        return job_names, existing_jobs
        
    except Exception as e:
        print(f"❌ خطأ في فحص الوظائف: {e}")
        return set(), []

def main():
    """الدالة الرئيسية"""
    print("🔍 تحليل بنية البيانات والاختلافات...")
    print("=" * 60)
    
    # فحص البنية الحالية
    current_emp = check_current_structure()
    
    # فحص الملف الجديد
    new_emp, new_data = check_new_file_structure()
    
    # مقارنة البنيتين
    if current_emp and new_emp:
        compare_structures(current_emp, new_emp)
    
    # فحص تطابق الوظائف
    check_job_mapping()
    
    print("\n" + "=" * 60)
    print("✅ انتهى التحليل!")

if __name__ == "__main__":
    main()
