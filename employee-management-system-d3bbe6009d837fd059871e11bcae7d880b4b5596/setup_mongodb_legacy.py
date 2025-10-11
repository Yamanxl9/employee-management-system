#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعداد قاعدة بيانات MongoDB لتطبيق إدارة الموظفين
إصدار متوافق مع الكود القديم باستخدام Flask-PyMongo
"""

import os
import json
from datetime import datetime
from flask import Flask
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['MONGO_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')

# إعداد MongoDB
mongo = PyMongo(app)

def setup_database():
    """إعداد قاعدة البيانات مع البيانات الأساسية"""
    print("🔧 بدء إعداد قاعدة البيانات...")
    
    # 1. إنشاء مستخدم مدير
    setup_admin_user()
    
    # 2. إنشاء بيانات الشركات
    setup_companies()
    
    # 3. إنشاء بيانات الوظائف
    setup_jobs()
    
    # 4. إنشاء بيانات الموظفين التجريبية
    setup_sample_employees()
    
    print("✅ تم إعداد قاعدة البيانات بنجاح!")

def setup_admin_user():
    """إنشاء مستخدم المدير"""
    print("👤 إعداد مستخدم المدير...")
    
    # التحقق من وجود المدير
    admin = mongo.db.users.find_one({'username': 'admin'})
    if admin:
        print("✅ مستخدم المدير موجود مسبقاً")
        return
    
    # إنشاء مستخدم المدير
    admin_data = {
        'username': 'admin',
        'password': generate_password_hash('admin123'),
        'role': 'admin',
        'created_at': datetime.now()
    }
    
    mongo.db.users.insert_one(admin_data)
    print("✅ تم إنشاء مستخدم المدير: admin/admin123")

def setup_companies():
    """إنشاء بيانات الشركات"""
    print("🏢 إعداد بيانات الشركات...")
    
    # مسح البيانات القديمة
    mongo.db.companies.delete_many({})
    
    companies = [
        {
            'company_code': 'ALQ001',
            'company_name_eng': 'Al-Aqeeli Trading Company',
            'company_name_ara': 'شركة العقيلي للتجارة',
            'created_at': datetime.now()
        },
        {
            'company_code': 'ALQ002', 
            'company_name_eng': 'Al-Aqeeli Construction',
            'company_name_ara': 'شركة العقيلي للمقاولات',
            'created_at': datetime.now()
        },
        {
            'company_code': 'ALQ003',
            'company_name_eng': 'Al-Aqeeli Real Estate',
            'company_name_ara': 'شركة العقيلي للعقارات',
            'created_at': datetime.now()
        },
        {
            'company_code': 'ALQ004',
            'company_name_eng': 'Al-Aqeeli Services',
            'company_name_ara': 'شركة العقيلي للخدمات',
            'created_at': datetime.now()
        }
    ]
    
    mongo.db.companies.insert_many(companies)
    print(f"✅ تم إنشاء {len(companies)} شركة")

def setup_jobs():
    """إنشاء بيانات الوظائف"""
    print("💼 إعداد بيانات الوظائف...")
    
    # مسح البيانات القديمة
    mongo.db.jobs.delete_many({})
    
    jobs = [
        {
            'job_code': 1001,
            'job_eng': 'General Manager',
            'job_ara': 'مدير عام',
            'created_at': datetime.now()
        },
        {
            'job_code': 1002,
            'job_eng': 'Operations Manager',
            'job_ara': 'مدير العمليات',
            'created_at': datetime.now()
        },
        {
            'job_code': 1003,
            'job_eng': 'Financial Manager',
            'job_ara': 'مدير مالي',
            'created_at': datetime.now()
        },
        {
            'job_code': 1004,
            'job_eng': 'HR Manager',
            'job_ara': 'مدير الموارد البشرية',
            'created_at': datetime.now()
        },
        {
            'job_code': 2001,
            'job_eng': 'Senior Accountant',
            'job_ara': 'محاسب أول',
            'created_at': datetime.now()
        },
        {
            'job_code': 2002,
            'job_eng': 'Project Engineer',
            'job_ara': 'مهندس مشاريع',
            'created_at': datetime.now()
        },
        {
            'job_code': 2003,
            'job_eng': 'Sales Representative',
            'job_ara': 'مندوب مبيعات',
            'created_at': datetime.now()
        },
        {
            'job_code': 3001,
            'job_eng': 'Administrative Assistant',
            'job_ara': 'مساعد إداري',
            'created_at': datetime.now()
        },
        {
            'job_code': 3002,
            'job_eng': 'Security Guard',
            'job_ara': 'حارس أمن',
            'created_at': datetime.now()
        },
        {
            'job_code': 3003,
            'job_eng': 'Driver',
            'job_ara': 'سائق',
            'created_at': datetime.now()
        }
    ]
    
    mongo.db.jobs.insert_many(jobs)
    print(f"✅ تم إنشاء {len(jobs)} وظيفة")

def setup_sample_employees():
    """إنشاء بيانات الموظفين التجريبية"""
    print("👥 إعداد بيانات الموظفين التجريبية...")
    
    # مسح البيانات القديمة
    mongo.db.employees.delete_many({})
    
    sample_employees = [
        {
            'staff_no': 101001,
            'staff_name': 'Ahmed Mohammed Al-Aqeeli',
            'staff_name_ara': 'أحمد محمد العقيلي',
            'job_code': 1001,
            'nationality_code': 'SA',
            'company_code': 'ALQ001',
            'pass_no': 'A12345678',
            'card_no': '1234567890',
            'card_expiry_date': '2025-12-31',
            'create_date_time': datetime.now()
        },
        {
            'staff_no': 101002,
            'staff_name': 'Fatima Ali Hassan',
            'staff_name_ara': 'فاطمة علي حسن',
            'job_code': 1004,
            'nationality_code': 'SA',
            'company_code': 'ALQ001',
            'pass_no': 'B87654321',
            'card_no': '0987654321',
            'card_expiry_date': '2024-06-30',
            'create_date_time': datetime.now()
        },
        {
            'staff_no': 102001,
            'staff_name': 'Omar Khalid Rahman',
            'staff_name_ara': 'عمر خالد الرحمن',
            'job_code': 2002,
            'nationality_code': 'EG',
            'company_code': 'ALQ002',
            'pass_no': 'C11223344',
            'card_no': '1122334455',
            'card_expiry_date': '2026-03-15',
            'create_date_time': datetime.now()
        },
        {
            'staff_no': 102002,
            'staff_name': 'Sarah Ahmed Mahmoud',
            'staff_name_ara': 'سارة أحمد محمود',
            'job_code': 2001,
            'nationality_code': 'EG',
            'company_code': 'ALQ002',
            'pass_no': '',  # بدون جواز
            'card_no': '2233445566',
            'card_expiry_date': '2023-12-31',  # منتهية
            'create_date_time': datetime.now()
        },
        {
            'staff_no': 103001,
            'staff_name': 'Mohammad Raza Khan',
            'staff_name_ara': 'محمد رضا خان',
            'job_code': 3003,
            'nationality_code': 'PK',
            'company_code': 'ALQ003',
            'pass_no': 'P55667788',
            'card_no': '',  # بدون بطاقة
            'card_expiry_date': '',
            'create_date_time': datetime.now()
        },
        {
            'staff_no': 103002,
            'staff_name': 'Priya Sharma',
            'staff_name_ara': 'بريا شارما',
            'job_code': 3001,
            'nationality_code': 'IN',
            'company_code': 'ALQ003',
            'pass_no': 'I99887766',
            'card_no': '9988776655',
            'card_expiry_date': '2025-08-20',  # تنتهي قريباً
            'create_date_time': datetime.now()
        },
        {
            'staff_no': 104001,
            'staff_name': 'Hassan Ali Osman',
            'staff_name_ara': 'حسن علي عثمان',
            'job_code': 2003,
            'nationality_code': 'SD',
            'company_code': 'ALQ004',
            'pass_no': 'S44556677',
            'card_no': '4455667788',
            'card_expiry_date': '2027-01-10',
            'create_date_time': datetime.now()
        }
    ]
    
    mongo.db.employees.insert_many(sample_employees)
    print(f"✅ تم إنشاء {len(sample_employees)} موظف تجريبي")

def create_indexes():
    """إنشاء الفهارس لتحسين الأداء"""
    print("🔍 إنشاء الفهارس...")
    
    # فهارس collection الموظفين
    mongo.db.employees.create_index([('staff_no', 1)], unique=True)
    mongo.db.employees.create_index([('staff_name', 'text'), ('staff_name_ara', 'text')])
    mongo.db.employees.create_index([('nationality_code', 1)])
    mongo.db.employees.create_index([('company_code', 1)])
    mongo.db.employees.create_index([('job_code', 1)])
    mongo.db.employees.create_index([('card_expiry_date', 1)])
    
    # فهارس collection الشركات
    mongo.db.companies.create_index([('company_code', 1)], unique=True)
    
    # فهارس collection الوظائف
    mongo.db.jobs.create_index([('job_code', 1)], unique=True)
    
    # فهارس collection المستخدمين
    mongo.db.users.create_index([('username', 1)], unique=True)
    
    print("✅ تم إنشاء الفهارس بنجاح")

def verify_data():
    """التحقق من البيانات المنشأة"""
    print("\n📊 التحقق من البيانات:")
    
    users_count = mongo.db.users.count_documents({})
    companies_count = mongo.db.companies.count_documents({})
    jobs_count = mongo.db.jobs.count_documents({})
    employees_count = mongo.db.employees.count_documents({})
    
    print(f"👤 المستخدمين: {users_count}")
    print(f"🏢 الشركات: {companies_count}")
    print(f"💼 الوظائف: {jobs_count}")
    print(f"👥 الموظفين: {employees_count}")
    
    # عرض عينة من البيانات
    print("\n📋 عينة من الموظفين:")
    for emp in mongo.db.employees.find().limit(3):
        print(f"  - {emp['staff_name_ara']} ({emp['staff_no']})")

if __name__ == '__main__':
    with app.app_context():
        try:
            setup_database()
            create_indexes()
            verify_data()
            print("\n🎉 تم إعداد قاعدة البيانات بنجاح!")
        except Exception as e:
            print(f"❌ خطأ في إعداد قاعدة البيانات: {e}")
            import traceback
            traceback.print_exc()
