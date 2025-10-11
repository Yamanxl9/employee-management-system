# سكريپت استبدال بيانات الموظفين الجديدة في MongoDB
# يقوم بربط أسماء الوظائف مع أكوادها من قاعدة البيانات

from pymongo import MongoClient
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد الاتصال مع MongoDB Atlas
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongodb_uri)
db = client.get_default_database()

def load_employees_data():
    """تحميل بيانات الموظفين الجديدة من ملف JSON"""
    with open('employees_new.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_job_mapping():
    """إنشاء خريطة ربط بين أسماء الوظائف وأكوادها"""
    jobs_collection = db['jobs']
    jobs = list(jobs_collection.find())
    
    job_mapping = {}
    for job in jobs:
        # ربط بالاسم الإنجليزي
        if 'job_eng' in job and 'job_code' in job:
            job_mapping[job['job_eng'].lower()] = job['job_code']
        
        # ربط بالاسم العربي
        if 'job_ara' in job and 'job_code' in job:
            job_mapping[job['job_ara']] = job['job_code']
    
    # إضافة ربط يدوي للوظائف الجديدة التي قد لا تكون موجودة
    manual_mapping = {
        'secretary': 9,  # سكرتير
        'marketing manager': 6,  # مدير التسويق
        'filing clerk': 5,  # كاتب ملفات
        'storekeeper': 18,  # أمين مخزن
        'marketing specialist': 17,  # أخصائي تسويق
        'communications assistant': 5,  # مساعد اتصالات (نفس كاتب ملفات)
        'accountant': 1,  # محاسب
        'sales officer': 9,  # مندوب مبيعات (نفس مدير مبيعات)
        'general manager': 19,  # مدير عام
        'messenger': 7,  # مراسل
    }
    
    # دمج الخرائط
    job_mapping.update(manual_mapping)
    
    print("خريطة ربط الوظائف:")
    for job_name, job_code in job_mapping.items():
        print(f"  {job_name} -> {job_code}")
    
    return job_mapping

def convert_date(date_string):
    """تحويل تاريخ من صيغة ISO إلى YYYY-MM-DD"""
    if not date_string or date_string == "":
        return None
    
    try:
        # تحويل من ISO format
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return None

def process_employees(employees_data, job_mapping):
    """تحويل بيانات الموظفين للصيغة المطلوبة"""
    processed_employees = []
    
    for emp in employees_data:
        # البحث عن كود الوظيفة
        job_name_lower = emp['job_name'].lower() if emp.get('job_name') else ''
        job_code = job_mapping.get(job_name_lower)
        
        if not job_code:
            print(f"⚠️  لم يتم العثور على كود للوظيفة: {emp['job_name']}")
            job_code = 1  # افتراضي
        
        # تحويل التاريخ
        card_expiry = convert_date(emp.get('card_expiry_date'))
        
        # تحويل رقم البطاقة
        card_no = emp.get('card_no', '')
        if card_no and not card_no.isdigit():
            # إذا كان النص مثل "new on spouse/father sponsorship"
            card_no = ''
        
        processed_emp = {
            'staff_no': emp['staff_no'],
            'staff_name': emp['staff_name'],
            'staff_name_ara': emp['staff_name_ara'],
            'job_code': job_code,
            'pass_no': emp.get('pass_no', ''),
            'nationality_code': emp.get('nationality_code', ''),
            'company_code': emp.get('company_code', ''),
            'card_no': card_no,
            'card_expiry_date': card_expiry,
            'create_date_time': datetime.now().isoformat()
        }
        
        processed_employees.append(processed_emp)
        print(f"✅ تم تحويل: {emp['staff_name']} - {emp['job_name']} -> كود {job_code}")
    
    return processed_employees

def replace_employees():
    """استبدال جميع الموظفين في قاعدة البيانات"""
    print("🚀 بدء عملية استبدال الموظفين...")
    
    # تحميل البيانات
    employees_data = load_employees_data()
    print(f"📄 تم تحميل {len(employees_data)} موظف جديد")
    
    # إنشاء خريطة ربط الوظائف
    job_mapping = get_job_mapping()
    
    # تحويل البيانات
    processed_employees = process_employees(employees_data, job_mapping)
    
    # الحصول على مجموعة الموظفين
    employees_collection = db['employees']
    
    # حذف جميع الموظفين القدامى
    print("🗑️  جاري حذف الموظفين القدامى...")
    result = employees_collection.delete_many({})
    print(f"✅ تم حذف {result.deleted_count} موظف قديم")
    
    # إدراج الموظفين الجدد
    print("📥 جاري إدراج الموظفين الجدد...")
    result = employees_collection.insert_many(processed_employees)
    print(f"✅ تم إدراج {len(result.inserted_ids)} موظف جديد")
    
    print("🎉 تم استبدال بيانات الموظفين بنجاح!")
    
    # إحصائيات نهائية
    total_employees = employees_collection.count_documents({})
    print(f"📊 إجمالي الموظفين في قاعدة البيانات: {total_employees}")

if __name__ == "__main__":
    try:
        replace_employees()
    except Exception as e:
        print(f"❌ خطأ في العملية: {str(e)}")
        import traceback
        traceback.print_exc()
