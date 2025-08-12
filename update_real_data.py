#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لاستخدام البيانات الحقيقية للشركات والوظائف من الملفات المرسلة
Use Real Company and Job Data from Provided Files
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
        logging.FileHandler('update_real_data.log', encoding='utf-8')
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

def load_companies_from_file():
    """تحميل بيانات الشركات من الملف الحقيقي"""
    try:
        # نسخ الملف إلى مجلد المشروع أولاً
        import shutil
        source_file = "c:\\Users\\yaman_alne0q1\\OneDrive\\Desktop\\deepseek_json_20250806_6ce2a0.json"
        dest_file = "companies_real.json"
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, dest_file)
            logger.info(f"📂 تم نسخ ملف الشركات: {dest_file}")
        
        # قراءة البيانات
        with open(dest_file, 'r', encoding='utf-8') as file:
            companies_data = json.load(file)
        
        logger.info(f"📊 تم تحميل {len(companies_data)} شركة من الملف")
        
        # تحويل البيانات للتنسيق المطلوب
        companies = []
        for company in companies_data:
            company_record = {
                'company_code': company.get('Company_code', ''),
                'company_name_eng': company.get('CompanyName_eng', ''),
                'company_name_ara': company.get('CompanyName_ara', ''),
                'created_date': datetime.now()
            }
            companies.append(company_record)
            logger.info(f"   📋 {company_record['company_code']}: {company_record['company_name_ara']}")
        
        return companies
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحميل بيانات الشركات: {e}")
        return []

def load_jobs_from_file():
    """تحميل بيانات الوظائف من الملف الحقيقي"""
    try:
        # نسخ الملف إلى مجلد المشروع أولاً
        import shutil
        source_file = "c:\\Users\\yaman_alne0q1\\OneDrive\\Desktop\\deepseek_json_20250806_b1cd12.json"
        dest_file = "jobs_real.json"
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, dest_file)
            logger.info(f"📂 تم نسخ ملف الوظائف: {dest_file}")
        
        # قراءة البيانات
        with open(dest_file, 'r', encoding='utf-8') as file:
            jobs_data = json.load(file)
        
        logger.info(f"📊 تم تحميل {len(jobs_data)} وظيفة من الملف")
        
        # تحويل البيانات للتنسيق المطلوب
        jobs = []
        for job in jobs_data:
            job_record = {
                'job_code': job.get('Job_Code', 0),
                'job_eng': job.get('Job_Eng', ''),
                'job_ara': job.get('Job_Ara', ''),
                'created_date': datetime.now()
            }
            jobs.append(job_record)
            logger.info(f"   💼 {job_record['job_code']}: {job_record['job_ara']}")
        
        return jobs
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحميل بيانات الوظائف: {e}")
        return []

def update_companies(db, companies):
    """تحديث الشركات في قاعدة البيانات"""
    try:
        # حذف الشركات الموجودة
        db.companies.delete_many({})
        logger.info("🗑️ تم حذف الشركات الموجودة")
        
        # إدراج الشركات الجديدة
        if companies:
            result = db.companies.insert_many(companies)
            logger.info(f"✅ تم إدراج {len(result.inserted_ids)} شركة حقيقية")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث الشركات: {e}")
        return False

def update_jobs(db, jobs):
    """تحديث الوظائف في قاعدة البيانات"""
    try:
        # حذف الوظائف الموجودة
        db.jobs.delete_many({})
        logger.info("🗑️ تم حذف الوظائف الموجودة")
        
        # إدراج الوظائف الجديدة
        if jobs:
            result = db.jobs.insert_many(jobs)
            logger.info(f"✅ تم إدراج {len(result.inserted_ids)} وظيفة حقيقية")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث الوظائف: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء تحديث البيانات بالملفات الحقيقية...")
    
    # الاتصال بقاعدة البيانات
    client, db = get_database_connection()
    if db is None:
        return False
    
    try:
        # تحميل البيانات الحقيقية من الملفات
        companies = load_companies_from_file()
        jobs = load_jobs_from_file()
        
        if not companies or not jobs:
            logger.error("❌ لم يتم تحميل البيانات من الملفات")
            return False
        
        # تحديث قاعدة البيانات
        if not update_companies(db, companies):
            logger.error("❌ فشل في تحديث الشركات")
            return False
        
        if not update_jobs(db, jobs):
            logger.error("❌ فشل في تحديث الوظائف")
            return False
        
        logger.info("🎉 تم تحديث البيانات بالملفات الحقيقية بنجاح!")
        
        # عرض الإحصائيات النهائية
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
        print("\n✅ تم تحديث البيانات بالملفات الحقيقية بنجاح!")
        print("💡 الآن التطبيق يستخدم أسماء الشركات والوظائف الحقيقية تماماً كما أرسلتها")
    else:
        print("\n❌ فشل في تحديث البيانات!")
        exit(1)
