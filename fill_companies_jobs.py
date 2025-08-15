# سكريپت تعبئة بيانات الشركات والوظائف في MongoDB
# يشترط وجود اتصال بقاعدة البيانات نفسها التي يستخدمها النظام

from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد الاتصال مع MongoDB Atlas
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongodb_uri)
db = client.get_default_database()  # استخدام قاعدة البيانات الافتراضية من URI

# قراءة بيانات الشركات من ملف JSON
with open('companies_new.json', 'r', encoding='utf-8') as f:
    companies_data = json.load(f)

# تحويل البيانات إلى الصيغة المطلوبة
companies = []
for company in companies_data:
    companies.append({
        "company_code": company["Company_code"],
        "company_name_eng": company["CompanyName_eng"],
        "company_name_ara": company["CompanyName_ara"]
    })

# قراءة بيانات الوظائف من ملف JSON
with open('jobs_new.json', 'r', encoding='utf-8') as f:
    jobs_data = json.load(f)

# تحويل البيانات إلى الصيغة المطلوبة  
jobs = []
for job in jobs_data:
    jobs.append({
        "job_code": job["Job_Code"],
        "job_eng": job["Job_Eng"],
        "job_ara": job["Job_Ara"]
    })

# حذف جميع الشركات القديمة واستبدالها بالجديدة
print("جاري حذف الشركات القديمة...")
db.companies.delete_many({})

print("جاري إضافة الشركات الجديدة...")
# إدخال الشركات الجديدة
for company in companies:
    db.companies.insert_one(company)
    print(f"تمت إضافة شركة: {company['company_name_ara']}")

print("جاري حذف/تحديث الوظائف...")
# حذف جميع الوظائف القديمة
db.jobs.delete_many({})

# إدخال الوظائف الجديدة
for job in jobs:
    db.jobs.insert_one(job)
    print(f"تمت إضافة وظيفة: {job['job_ara']}")

print("تمت تعبئة بيانات الشركات والوظائف بنجاح.")
