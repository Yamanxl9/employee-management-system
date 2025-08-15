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

# بيانات الوظائف التجريبية
jobs = [
    {"job_code": 1, "job_eng": "Accountant", "job_ara": "محاسب"},
    {"job_code": 2, "job_eng": "Sales Representative", "job_ara": "مندوب مبيعات"},
    {"job_code": 3, "job_eng": "Store Keeper", "job_ara": "أمين مخزن"},
    {"job_code": 4, "job_eng": "Manager", "job_ara": "مدير"},
    {"job_code": 5, "job_eng": "Assistant", "job_ara": "مساعد"},
    {"job_code": 6, "job_eng": "Supervisor", "job_ara": "مشرف"},
    {"job_code": 7, "job_eng": "Driver", "job_ara": "سائق"},
    {"job_code": 8, "job_eng": "Cashier", "job_ara": "أمين صندوق"},
    {"job_code": 9, "job_eng": "Secretary", "job_ara": "سكرتير"},
    {"job_code": 10, "job_eng": "Technician", "job_ara": "فني"},
    {"job_code": 11, "job_eng": "Security Guard", "job_ara": "حارس أمن"},
    {"job_code": 12, "job_eng": "Cleaner", "job_ara": "عامل نظافة"}
]

# حذف جميع الشركات القديمة واستبدالها بالجديدة
print("جاري حذف الشركات القديمة...")
db.companies.delete_many({})

print("جاري إضافة الشركات الجديدة...")
# إدخال الشركات الجديدة
for company in companies:
    db.companies.insert_one(company)
    print(f"تمت إضافة شركة: {company['company_name_ara']}")

print("جاري إضافة/تحديث الوظائف...")
# إدخال الوظائف (مع تجنب التكرار)
for job in jobs:
    existing = db.jobs.find_one({"job_code": job["job_code"]})
    if not existing:
        db.jobs.insert_one(job)
        print(f"تمت إضافة وظيفة: {job['job_ara']}")
    else:
        print(f"وظيفة موجودة مسبقاً: {job['job_ara']}")

print("تمت تعبئة بيانات الشركات والوظائف بنجاح.")
