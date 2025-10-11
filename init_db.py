#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, Company, Job
import sys

def init_database():
    with app.app_context():
        print("إنشاء الجداول...")
        db.create_all()
        
        # تحقق من وجود البيانات
        if Company.query.count() > 0:
            print("البيانات موجودة مسبقاً!")
            return
        
        print("تحميل الشركات...")
        companies_data = [
            {"company_code": "001", "company_name_eng": "Al-Aqeeli Trading", "company_name_ara": "العقيلي للتجارة"},
            {"company_code": "002", "company_name_eng": "Al-Aqeeli Construction", "company_name_ara": "العقيلي للإنشاءات"},
            {"company_code": "003", "company_name_eng": "Al-Aqeeli Services", "company_name_ara": "العقيلي للخدمات"},
            {"company_code": "004", "company_name_eng": "Al-Aqeeli Industries", "company_name_ara": "العقيلي للصناعات"},
            {"company_code": "005", "company_name_eng": "Al-Aqeeli Real Estate", "company_name_ara": "العقيلي للعقارات"},
            {"company_code": "006", "company_name_eng": "Al-Aqeeli Technology", "company_name_ara": "العقيلي للتكنولوجيا"},
            {"company_code": "007", "company_name_eng": "Al-Aqeeli Logistics", "company_name_ara": "العقيلي للنقل"}
        ]
        
        for comp_data in companies_data:
            company = Company(**comp_data)
            db.session.add(company)
        
        print("تحميل الوظائف...")
        jobs_data = [
            {"job_code": "MGR", "job_eng": "Manager", "job_ara": "مدير"},
            {"job_code": "ACC", "job_eng": "Accountant", "job_ara": "محاسب"},
            {"job_code": "ENG", "job_eng": "Engineer", "job_ara": "مهندس"},
            {"job_code": "SEC", "job_eng": "Secretary", "job_ara": "سكرتير"},
            {"job_code": "DR", "job_eng": "Driver", "job_ara": "سائق"},
            {"job_code": "GRD", "job_eng": "Guard", "job_ara": "حارس"},
            {"job_code": "CLN", "job_eng": "Cleaner", "job_ara": "عامل نظافة"},
            {"job_code": "TCH", "job_eng": "Technician", "job_ara": "فني"},
            {"job_code": "SAL", "job_eng": "Sales Representative", "job_ara": "مندوب مبيعات"},
            {"job_code": "HR", "job_eng": "HR Specialist", "job_ara": "أخصائي موارد بشرية"},
            {"job_code": "IT", "job_eng": "IT Specialist", "job_ara": "أخصائي تقنية معلومات"},
            {"job_code": "FIN", "job_eng": "Financial Analyst", "job_ara": "محلل مالي"},
            {"job_code": "MKT", "job_eng": "Marketing Specialist", "job_ara": "أخصائي تسويق"},
            {"job_code": "OPR", "job_eng": "Operations Officer", "job_ara": "ضابط عمليات"},
            {"job_code": "QC", "job_eng": "Quality Controller", "job_ara": "مراقب جودة"},
            {"job_code": "PRJ", "job_eng": "Project Coordinator", "job_ara": "منسق مشاريع"},
            {"job_code": "LOG", "job_eng": "Logistics Officer", "job_ara": "ضابط لوجستي"},
            {"job_code": "PUR", "job_eng": "Purchasing Officer", "job_ara": "ضابط مشتريات"},
            {"job_code": "REL", "job_eng": "Public Relations", "job_ara": "علاقات عامة"},
            {"job_code": "TRN", "job_eng": "Trainer", "job_ara": "مدرب"},
            {"job_code": "SOFF", "job_eng": "Sales Officer", "job_ara": "ضابط مبيعات"},
            {"job_code": "AST", "job_eng": "Assistant", "job_ara": "مساعد"}
        ]
        
        for job_data in jobs_data:
            job = Job(**job_data)
            db.session.add(job)
        
        try:
            db.session.commit()
            print(f"✅ تم تحميل {len(companies_data)} شركة و {len(jobs_data)} وظيفة بنجاح!")
            
            # التحقق من النتائج
            print(f"📊 الشركات في قاعدة البيانات: {Company.query.count()}")
            print(f"📊 الوظائف في قاعدة البيانات: {Job.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في تحميل البيانات: {e}")
            sys.exit(1)

if __name__ == "__main__":
    init_database()
