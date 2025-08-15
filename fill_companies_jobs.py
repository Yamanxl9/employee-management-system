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
    {"company_code": "REX", "company_name_eng": "REX DUBAI (L.L.C)", "company_name_ara": "ركس دبي (ش.ذ.م.م)"}
]

# بيانات الوظائف التجريبية
jobs = [
    {"job_code": 1, "job_eng": "Accountant", "job_ara": "محاسب"},
    {"job_code": 2, "job_eng": "Sales Representative", "job_ara": "مندوب مبيعات"},
    {"job_code": 3, "job_eng": "Store Keeper", "job_ara": "أمين مخزن"},
    {"job_code": 4, "job_eng": "Manager", "job_ara": "مدير"}
]

# حذف البيانات القديمة (اختياري)
db.companies.delete_many({})
db.jobs.delete_many({})

# إدخال البيانات الجديدة
db.companies.insert_many(companies)
db.jobs.insert_many(jobs)

print("تمت تعبئة بيانات الشركات والوظائف بنجاح.")
