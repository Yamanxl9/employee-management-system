#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص ما قبل النشر على Render
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """فحص متغيرات البيئة"""
    print("🔍 فحص متغيرات البيئة...")
    
    load_dotenv()
    
    required_vars = ['MONGODB_URI', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"   ✅ {var}: متوفر")
    
    if missing_vars:
        print(f"   ❌ متغيرات مفقودة: {', '.join(missing_vars)}")
        return False
    
    return True

def check_mongodb_connection():
    """فحص الاتصال بقاعدة البيانات"""
    print("\n🗄️ فحص الاتصال بقاعدة البيانات...")
    
    try:
        from pymongo import MongoClient
        
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            print("   ❌ MONGODB_URI غير موجود")
            return False
        
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        
        print("   ✅ الاتصال بقاعدة البيانات ناجح")
        
        # فحص البيانات
        db = client.get_database()
        employees_count = db.employees.count_documents({})
        companies_count = db.companies.count_documents({})
        jobs_count = db.jobs.count_documents({})
        
        print(f"   📊 عدد الموظفين: {employees_count}")
        print(f"   📊 عدد الشركات: {companies_count}")
        print(f"   📊 عدد الوظائف: {jobs_count}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في الاتصال: {e}")
        return False

def check_required_files():
    """فحص الملفات المطلوبة للنشر"""
    print("\n📁 فحص الملفات المطلوبة...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'render.yaml',
        'Procfile',
        'gunicorn.conf.py',
        'nationalities.py',
        '.env'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            missing_files.append(file)
            print(f"   ❌ {file}")
    
    if missing_files:
        print(f"   ❌ ملفات مفقودة: {', '.join(missing_files)}")
        return False
    
    return True

def check_imports():
    """فحص استيراد المكتبات"""
    print("\n📦 فحص المكتبات المطلوبة...")
    
    required_modules = [
        'flask',
        'flask_pymongo',
        'pymongo',
        'pandas',
        'jwt',
        'dotenv'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"   ❌ {module}")
    
    if missing_modules:
        print(f"   ❌ مكتبات مفقودة: {', '.join(missing_modules)}")
        return False
    
    return True

def main():
    """الدالة الرئيسية"""
    print("🚀 فحص ما قبل النشر على Render")
    print("=" * 50)
    
    checks = [
        check_required_files(),
        check_imports(),
        check_environment(),
        check_mongodb_connection()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("✅ جميع الفحوصات نجحت! التطبيق جاهز للنشر على Render")
        print("\n📋 خطوات النشر:")
        print("1. ادفع الكود إلى GitHub")
        print("2. اذهب إلى Render.com")
        print("3. أنشئ خدمة ويب جديدة")
        print("4. اربطها بـ GitHub repository")
        print("5. أضف متغير MONGODB_URI في إعدادات البيئة")
        return True
    else:
        print("❌ هناك مشاكل يجب حلها قبل النشر")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
