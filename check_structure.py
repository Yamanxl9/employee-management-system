from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['employee_management']
    
    print("🔍 فحص بنية البيانات:")
    
    # فحص الوظائف
    jobs = list(db.jobs.find().limit(3))
    print(f"\n✅ الوظائف ({db.jobs.count_documents({})} إجمالي):")
    for job in jobs:
        print(f"  Code: {job.get('code')}, Name_Ara: {job.get('name_ara')}, Name_Eng: {job.get('name_eng')}")
    
    # فحص الشركات
    companies = list(db.companies.find())
    print(f"\n✅ جميع الشركات ({db.companies.count_documents({})} إجمالي):")
    for company in companies:
        print(f"  Code: {company.get('code')}, Name_Ara: {company.get('name_ara')}")
    
    # فحص أكواد الشركات المستخدمة في الموظفين
    employee_companies = db.employees.distinct('company_code')
    print(f"\n📋 أكواد الشركات المستخدمة في الموظفين: {employee_companies}")
    
    # فحص التطابق
    company_codes = [c['code'] for c in companies]
    print(f"📋 أكواد الشركات الموجودة: {company_codes}")
    
    missing_companies = [code for code in employee_companies if code not in company_codes and code]
    if missing_companies:
        print(f"⚠️ شركات مفقودة: {missing_companies}")
    else:
        print("✅ جميع أكواد الشركات متطابقة")
    
    # فحص الموظفين
    employees = list(db.employees.find().limit(3))
    print(f"\n✅ الموظفين ({db.employees.count_documents({})} إجمالي):")
    for emp in employees:
        print(f"  Staff_No: {emp.get('staff_no')}, Name: {emp.get('staff_name')}, Job_Code: {emp.get('job_code')}, Company_Code: {emp.get('company_code')}")

except Exception as e:
    print(f"❌ خطأ: {e}")
finally:
    if 'client' in locals():
        client.close()
