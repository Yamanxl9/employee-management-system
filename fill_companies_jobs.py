# سكريبت تعبئة بيانات الشركات والوظائف في MongoDB
# يشترط وجود اتصال بقاعدة البيانات نفسها التي يستخدمها النظام

from pymongo import MongoClient
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد الاتصال مع MongoDB Atlas
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongodb_uri)
db = client.get_default_database()  # استخدام قاعدة البيانات الافتراضية من URI

# بيانات الشركات التجريبية
companies = [
    {"company_code": "IN", "company_name_eng": "IN Company", "company_name_ara": "شركة IN"},
    {"company_code": "OUT", "company_name_eng": "OUT Company", "company_name_ara": "شركة OUT"},
    {"company_code": "SCM", "company_name_eng": "SCM General Stores", "company_name_ara": "اس كيو اف تي للمخازن العامة"},
    {"company_code": "YONIFOOD", "company_name_eng": "YONIFOOD Trading", "company_name_ara": "يونيفود للتجارة"},
    {"company_code": "REX", "company_name_eng": "REX DUBAI (L.L.C)", "company_name_ara": "ركس دبي (ش.ذ.م.م)"},
    {"company_code": "AQEELI", "company_name_eng": "Al-Aqeeli Group", "company_name_ara": "مجموعة شركات العقيلي"},
    {"company_code": "TRADING", "company_name_eng": "Trading Company", "company_name_ara": "شركة التجارة"},
    {"company_code": "GENERAL", "company_name_eng": "General Services", "company_name_ara": "الخدمات العامة"}
]

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

# حذف البيانات القديمة (معطل لتجنب حذف البيانات الموجودة)
# db.companies.delete_many({})
# db.jobs.delete_many({})

# إدخال البيانات الجديدة (مع تجنب التكرار)
for company in companies:
    existing = db.companies.find_one({"company_code": company["company_code"]})
    if not existing:
        db.companies.insert_one(company)
        print(f"تمت إضافة شركة: {company['company_name_ara']}")
    else:
        print(f"شركة موجودة مسبقاً: {company['company_name_ara']}")

for job in jobs:
    existing = db.jobs.find_one({"job_code": job["job_code"]})
    if not existing:
        db.jobs.insert_one(job)
        print(f"تمت إضافة وظيفة: {job['job_ara']}")
    else:
        print(f"وظيفة موجودة مسبقاً: {job['job_ara']}")

print("تمت تعبئة بيانات الشركات والوظائف بنجاح.")
