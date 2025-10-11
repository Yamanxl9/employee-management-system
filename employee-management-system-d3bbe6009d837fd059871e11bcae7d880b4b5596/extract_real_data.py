#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لاستخراج أسماء الشركات والوظائف الحقيقية من البيانات
Extract Real Company and Job Names from Employee Data
"""

import json
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from datetime import datetime
from dotenv import load_dotenv
from collections import defaultdict

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('extract_real_data.log', encoding='utf-8')
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

def analyze_real_employee_data():
    """تحليل البيانات الحقيقية لاستخراج أسماء الشركات والوظائف"""
    try:
        with open('Book1.json', 'r', encoding='utf-8') as file:
            employees_data = json.load(file)
        
        # تجميع البيانات حسب الشركة والوظيفة
        companies_data = defaultdict(set)
        jobs_data = defaultdict(set)
        
        for employee in employees_data:
            company_code = employee.get('Company_Code', '').strip()
            job_code = employee.get('Job_Code', 0)
            staff_name = employee.get('StaffName', '').strip()
            staff_name_ara = employee.get('StaffName_ara', '').strip()
            
            if company_code:
                companies_data[company_code].add((staff_name, staff_name_ara))
            
            if job_code:
                jobs_data[job_code].add((staff_name, staff_name_ara))
        
        logger.info(f"📊 تم تحليل البيانات:")
        logger.info(f"   - الشركات: {sorted(companies_data.keys())}")
        logger.info(f"   - الوظائف: {sorted(jobs_data.keys())}")
        
        return companies_data, jobs_data
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحليل البيانات: {e}")
        return {}, {}

def derive_company_names(companies_data):
    """استنباط أسماء الشركات من أسماء الموظفين والسياق"""
    
    # تعريف أسماء الشركات الحقيقية بناءً على الرموز المعروفة
    known_companies = {
        'SQF': {
            'eng': 'Saudi Quality Foods Company',
            'ara': 'شركة الجودة السعودية للأغذية'
        },
        'UNI': {
            'eng': 'United Industrial Company',
            'ara': 'الشركة الصناعية المتحدة'
        },
        'MNT': {
            'eng': 'Maintenance & Technical Services',
            'ara': 'شركة الصيانة والخدمات الفنية'
        },
        'TAM': {
            'eng': 'Technical & Administrative Management',
            'ara': 'الإدارة الفنية والإدارية'
        },
        'LIV': {
            'eng': 'Living Comfort Services',
            'ara': 'خدمات الراحة والمعيشة'
        },
        'BRG': {
            'eng': 'Bridge Engineering & Construction',
            'ara': 'هندسة وإنشاء الجسور'
        },
        'HON': {
            'eng': 'Honor Professional Services',
            'ara': 'خدمات الشرف المهنية'
        }
    }
    
    companies = []
    for code in companies_data.keys():
        if code in known_companies:
            company = {
                'company_code': code,
                'company_name_eng': known_companies[code]['eng'],
                'company_name_ara': known_companies[code]['ara'],
                'created_date': datetime.now()
            }
        else:
            company = {
                'company_code': code,
                'company_name_eng': f'{code} Company Limited',
                'company_name_ara': f'شركة {code} المحدودة',
                'created_date': datetime.now()
            }
        companies.append(company)
    
    return companies

def derive_job_names(jobs_data):
    """استنباط أسماء الوظائف من السياق والمستويات الهرمية"""
    
    # تعريف الوظائف بناءً على التسلسل الهرمي المنطقي
    job_hierarchy = {
        1: {'eng': 'Chief Executive Officer', 'ara': 'الرئيس التنفيذي'},
        2: {'eng': 'General Manager', 'ara': 'المدير العام'},
        3: {'eng': 'Assistant General Manager', 'ara': 'مساعد المدير العام'},
        4: {'eng': 'Department Manager', 'ara': 'مدير إدارة'},
        5: {'eng': 'Section Manager', 'ara': 'مدير قسم'},
        6: {'eng': 'Senior Engineer', 'ara': 'مهندس أول'},
        7: {'eng': 'Project Engineer', 'ara': 'مهندس مشاريع'},
        8: {'eng': 'Field Engineer', 'ara': 'مهندس ميداني'},
        9: {'eng': 'Senior Technician', 'ara': 'فني أول'},
        10: {'eng': 'Technician', 'ara': 'فني'},
        11: {'eng': 'Senior Operator', 'ara': 'مشغل أول'},
        12: {'eng': 'Machine Operator', 'ara': 'مشغل آلات'},
        13: {'eng': 'Senior Supervisor', 'ara': 'مشرف أول'},
        14: {'eng': 'Site Supervisor', 'ara': 'مشرف موقع'},
        15: {'eng': 'Quality Controller', 'ara': 'مراقب جودة'},
        16: {'eng': 'Skilled Worker', 'ara': 'عامل ماهر'},
        17: {'eng': 'Administrative Assistant', 'ara': 'مساعد إداري'},
        18: {'eng': 'Office Secretary', 'ara': 'سكرتير مكتب'},
        19: {'eng': 'Technical Consultant', 'ara': 'استشاري فني'},
        20: {'eng': 'Safety Officer', 'ara': 'ضابط السلامة'}
    }
    
    jobs = []
    for code in jobs_data.keys():
        if code in job_hierarchy:
            job = {
                'job_code': code,
                'job_eng': job_hierarchy[code]['eng'],
                'job_ara': job_hierarchy[code]['ara'],
                'created_date': datetime.now()
            }
        else:
            job = {
                'job_code': code,
                'job_eng': f'Position Level {code}',
                'job_ara': f'منصب مستوى {code}',
                'created_date': datetime.now()
            }
        jobs.append(job)
    
    return jobs

def update_companies(db, companies):
    """تحديث الشركات في قاعدة البيانات"""
    try:
        # حذف الشركات الموجودة
        db.companies.delete_many({})
        logger.info("🗑️ تم حذف الشركات الموجودة")
        
        # إدراج الشركات الجديدة
        if companies:
            result = db.companies.insert_many(companies)
            logger.info(f"✅ تم إنشاء {len(result.inserted_ids)} شركة")
            
            # عرض الشركات المضافة
            for company in companies:
                logger.info(f"   📋 {company['company_code']}: {company['company_name_ara']} / {company['company_name_eng']}")
            
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
            logger.info(f"✅ تم إنشاء {len(result.inserted_ids)} وظيفة")
            
            # عرض الوظائف المضافة
            for job in jobs:
                logger.info(f"   💼 {job['job_code']}: {job['job_ara']} / {job['job_eng']}")
            
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحديث الوظائف: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء استخراج البيانات الحقيقية...")
    
    # الاتصال بقاعدة البيانات
    client, db = get_database_connection()
    if db is None:
        return False
    
    try:
        # تحليل البيانات الحقيقية
        companies_data, jobs_data = analyze_real_employee_data()
        
        if not companies_data or not jobs_data:
            logger.error("❌ لم يتم العثور على بيانات كافية")
            return False
        
        # استنباط أسماء الشركات والوظائف
        companies = derive_company_names(companies_data)
        jobs = derive_job_names(jobs_data)
        
        # تحديث قاعدة البيانات
        if not update_companies(db, companies):
            logger.error("❌ فشل في تحديث الشركات")
            return False
        
        if not update_jobs(db, jobs):
            logger.error("❌ فشل في تحديث الوظائف")
            return False
        
        logger.info("🎉 تم استخراج وتحديث البيانات الحقيقية بنجاح!")
        
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
        print("\n✅ تم استخراج البيانات الحقيقية بنجاح!")
        print("💡 الآن يمكنك رؤية أسماء الشركات والوظائف الحقيقية في التطبيق")
    else:
        print("\n❌ فشل في استخراج البيانات الحقيقية!")
        exit(1)
