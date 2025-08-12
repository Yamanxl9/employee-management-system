# سكريبت تعبئة بيانات الشركات والوظائف في MongoDB
# يشترط وجود اتصال بقاعدة البيانات نفسها التي يستخدمها النظام

from pymongo import MongoClient

# إعداد الاتصال (تأكد من ضبط الرابط إذا كان مختلفًا)
client = MongoClient('mongodb://localhost:27017/')
db = client['employees_db']

# بيانات الشركات التجريبية
companies = [
    {"company_code": "IN", "company_name_eng": "IN Company", "company_name_ara": "شركة IN"},
    {"company_code": "OUT", "company_name_eng": "OUT Company", "company_name_ara": "شركة OUT"},
    {"company_code": "SCM", "company_name_eng": "SCM General Stores", "company_name_ara": "اس كيو اف تي للمخازن العامة"},
    {"company_code": "YONIFOOD", "company_name_eng": "YONIFOOD Trading", "company_name_ara": "يونيفود للتجارة"}
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
