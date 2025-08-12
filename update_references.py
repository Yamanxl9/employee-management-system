#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لإضافة الشركات والوظائف المناسبة لبيانات الموظفين
Add Companies and Jobs for Employee Data Script
"""

import json
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('update_references.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def get_database_connection():
    """الاتصال بقاعدة البيانات"""
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = os.getenv('MONGODB_DB', 'employees_db')
        
        logger.info(f"🔗 محاولة الاتصال بقاعدة البيانات: {database_name}")
        
        client = MongoClient(mongodb_uri)
        client.admin.command('ping')
        
        db = client[database_name]
        logger.info(f"✅ نجح الاتصال بقاعدة البيانات: {database_name}")
        
        return client, db
        
    except PyMongoError as e:
        logger.error(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
        return None, None
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
        return None, None

def analyze_employee_data():
    """تحليل بيانات الموظفين لاستخراج الشركات والوظائف"""
    try:
        with open('Book1.json', 'r', encoding='utf-8') as file:
            employees_data = json.load(file)
        
        # استخراج رموز الشركات الفريدة
        company_codes = set()
        job_codes = set()
        
        for employee in employees_data:
            company_code = employee.get('Company_Code', '').strip()
            job_code = employee.get('Job_Code', 0)
            
            if company_code:
                company_codes.add(company_code)
            if job_code:
                job_codes.add(job_code)
        
        logger.info(f"📊 تم العثور على {len(company_codes)} شركة: {sorted(company_codes)}")
        logger.info(f"📊 تم العثور على {len(job_codes)} وظيفة: {sorted(job_codes)}")
        
        return sorted(company_codes), sorted(job_codes)
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحليل بيانات الموظفين: {e}")
        return [], []

def create_companies(db, company_codes):
    """إنشاء الشركات"""
    try:
        # تعريف أسماء الشركات
        company_names = {
            'SQF': {'eng': 'SQF Company', 'ara': 'شركة SQF'},
            'UNI': {'eng': 'United Industries', 'ara': 'الصناعات المتحدة'},
            'MNT': {'eng': 'Maintenance Services', 'ara': 'خدمات الصيانة'},
            'TAM': {'eng': 'TAM Corporation', 'ara': 'شركة TAM'},
            'LIV': {'eng': 'Living Services', 'ara': 'خدمات المعيشة'},
            'BRG': {'eng': 'Bridge Construction', 'ara': 'إنشاءات الجسور'},
            'HON': {'eng': 'Honor Group', 'ara': 'مجموعة الشرف'}
        }
        
        # حذف الشركات الموجودة
        db.companies.delete_many({})
        logger.info("🗑️ تم حذف الشركات الموجودة")
        
        # إنشاء الشركات الجديدة
        companies = []
        for code in company_codes:
            if code in company_names:
                company = {
                    'company_code': code,
                    'company_name_eng': company_names[code]['eng'],
                    'company_name_ara': company_names[code]['ara'],
                    'created_date': datetime.now()
                }
            else:
                company = {
                    'company_code': code,
                    'company_name_eng': f'{code} Company',
                    'company_name_ara': f'شركة {code}',
                    'created_date': datetime.now()
                }
            companies.append(company)
        
        if companies:
            result = db.companies.insert_many(companies)
            logger.info(f"✅ تم إنشاء {len(result.inserted_ids)} شركة")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"❌ خطأ في إنشاء الشركات: {e}")
        return False

def create_jobs(db, job_codes):
    """إنشاء الوظائف"""
    try:
        # تعريف أسماء الوظائف
        job_names = {
            1: {'eng': 'General Manager', 'ara': 'مدير عام'},
            2: {'eng': 'Operations Manager', 'ara': 'مدير العمليات'},
            3: {'eng': 'Project Manager', 'ara': 'مدير مشروع'},
            4: {'eng': 'Team Leader', 'ara': 'قائد فريق'},
            5: {'eng': 'Senior Engineer', 'ara': 'مهندس أول'},
            6: {'eng': 'Engineer', 'ara': 'مهندس'},
            7: {'eng': 'Senior Technician', 'ara': 'فني أول'},
            8: {'eng': 'Technician', 'ara': 'فني'},
            9: {'eng': 'Senior Specialist', 'ara': 'أخصائي أول'},
            10: {'eng': 'Specialist', 'ara': 'أخصائي'},
            11: {'eng': 'Senior Operator', 'ara': 'مشغل أول'},
            12: {'eng': 'Operator', 'ara': 'مشغل'},
            13: {'eng': 'Senior Supervisor', 'ara': 'مشرف أول'},
            14: {'eng': 'Supervisor', 'ara': 'مشرف'},
            15: {'eng': 'Coordinator', 'ara': 'منسق'},
            16: {'eng': 'Worker', 'ara': 'عامل'},
            17: {'eng': 'Assistant', 'ara': 'مساعد'},
            18: {'eng': 'Secretary', 'ara': 'سكرتير'},
            19: {'eng': 'Consultant', 'ara': 'استشاري'},
            20: {'eng': 'Trainee', 'ara': 'متدرب'}
        }
        
        # حذف الوظائف الموجودة
        db.jobs.delete_many({})
        logger.info("🗑️ تم حذف الوظائف الموجودة")
        
        # إنشاء الوظائف الجديدة
        jobs = []
        for code in job_codes:
            if code in job_names:
                job = {
                    'job_code': code,
                    'job_eng': job_names[code]['eng'],
                    'job_ara': job_names[code]['ara'],
                    'created_date': datetime.now()
                }
            else:
                job = {
                    'job_code': code,
                    'job_eng': f'Position {code}',
                    'job_ara': f'منصب {code}',
                    'created_date': datetime.now()
                }
            jobs.append(job)
        
        if jobs:
            result = db.jobs.insert_many(jobs)
            logger.info(f"✅ تم إنشاء {len(result.inserted_ids)} وظيفة")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"❌ خطأ في إنشاء الوظائف: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء تحديث البيانات المرجعية...")
    
    # الاتصال بقاعدة البيانات
    client, db = get_database_connection()
    if db is None:
        return False
    
    try:
        # تحليل بيانات الموظفين
        company_codes, job_codes = analyze_employee_data()
        
        if not company_codes or not job_codes:
            logger.error("❌ لم يتم العثور على بيانات كافية")
            return False
        
        # إنشاء الشركات
        if not create_companies(db, company_codes):
            logger.error("❌ فشل في إنشاء الشركات")
            return False
        
        # إنشاء الوظائف
        if not create_jobs(db, job_codes):
            logger.error("❌ فشل في إنشاء الوظائف")
            return False
        
        logger.info("🎉 تم تحديث البيانات المرجعية بنجاح!")
        
        # عرض الإحصائيات
        companies_count = db.companies.count_documents({})
        jobs_count = db.jobs.count_documents({})
        employees_count = db.employees.count_documents({})
        
        logger.info("📊 الإحصائيات النهائية:")
        logger.info(f"   - الشركات: {companies_count}")
        logger.info(f"   - الوظائف: {jobs_count}")
        logger.info(f"   - الموظفين: {employees_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في العملية الرئيسية: {e}")
        return False
    finally:
        # إغلاق الاتصال
        if client:
            client.close()
            logger.info("🔐 تم إغلاق الاتصال بقاعدة البيانات")

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ تم تحديث البيانات المرجعية بنجاح!")
        print("💡 الآن سيتمكن التطبيق من عرض أسماء الشركات والوظائف بشكل صحيح")
    else:
        print("\n❌ فشل في تحديث البيانات المرجعية!")
        exit(1)
