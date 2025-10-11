"""
سكريبت لنقل البيانات من SQLite إلى MongoDB
"""
import sqlite3
import json
from datetime import datetime
from pymongo import MongoClient
import os

def migrate_sqlite_to_mongodb():
    """نقل البيانات من SQLite إلى MongoDB"""
    
    # الاتصال بـ SQLite
    sqlite_conn = sqlite3.connect('employees.db')
    sqlite_conn.row_factory = sqlite3.Row  # للحصول على النتائج كقواميس
    
    # الاتصال بـ MongoDB
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
    mongo_client = MongoClient(mongodb_uri)
    mongo_db = mongo_client.get_database()
    
    print("🔄 بدء نقل البيانات من SQLite إلى MongoDB...")
    
    # نقل الشركات
    print("📋 نقل بيانات الشركات...")
    companies = sqlite_conn.execute("SELECT * FROM companies").fetchall()
    if companies:
        companies_data = [dict(company) for company in companies]
        mongo_db.companies.delete_many({})  # مسح البيانات القديمة
        mongo_db.companies.insert_many(companies_data)
        print(f"✅ تم نقل {len(companies_data)} شركة")
    
    # نقل الوظائف
    print("💼 نقل بيانات الوظائف...")
    jobs = sqlite_conn.execute("SELECT * FROM jobs").fetchall()
    if jobs:
        jobs_data = [dict(job) for job in jobs]
        mongo_db.jobs.delete_many({})  # مسح البيانات القديمة
        mongo_db.jobs.insert_many(jobs_data)
        print(f"✅ تم نقل {len(jobs_data)} وظيفة")
    
    # نقل الموظفين
    print("👥 نقل بيانات الموظفين...")
    employees = sqlite_conn.execute("SELECT * FROM employees").fetchall()
    if employees:
        employees_data = []
        for emp in employees:
            emp_dict = dict(emp)
            
            # تحويل التواريخ
            if emp_dict['card_expiry_date']:
                try:
                    emp_dict['card_expiry_date'] = datetime.fromisoformat(emp_dict['card_expiry_date'])
                except:
                    emp_dict['card_expiry_date'] = None
            
            if emp_dict['create_date_time']:
                try:
                    emp_dict['create_date_time'] = datetime.fromisoformat(emp_dict['create_date_time'])
                except:
                    emp_dict['create_date_time'] = datetime.now()
            else:
                emp_dict['create_date_time'] = datetime.now()
            
            # تحويل الأرقام
            if emp_dict['job_code']:
                emp_dict['job_code'] = int(emp_dict['job_code'])
            
            employees_data.append(emp_dict)
        
        mongo_db.employees.delete_many({})  # مسح البيانات القديمة
        mongo_db.employees.insert_many(employees_data)
        print(f"✅ تم نقل {len(employees_data)} موظف")
    
    # إغلاق الاتصالات
    sqlite_conn.close()
    mongo_client.close()
    
    print("🎉 تم نقل جميع البيانات بنجاح إلى MongoDB!")

if __name__ == "__main__":
    migrate_sqlite_to_mongodb()
