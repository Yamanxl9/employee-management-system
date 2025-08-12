import os
from pymongo import MongoClient
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# جلب رابط MongoDB من ملف .env
mongodb_uri = os.getenv('MONGODB_URI')
print(f"رابط MongoDB: {mongodb_uri}")

try:
    # محاولة الاتصال
    client = MongoClient(mongodb_uri)
    db = client['employees_db']
    
    # اختبار الاتصال
    client.admin.command('ping')
    print("✅ الاتصال بـ MongoDB Atlas نجح!")
    
    # فحص المجموعات الموجودة
    collections = db.list_collection_names()
    print(f"المجموعات الموجودة: {collections}")
    
    # فحص عدد السجلات في كل مجموعة
    for collection_name in collections:
        count = db[collection_name].count_documents({})
        print(f"عدد السجلات في {collection_name}: {count}")
    
    # عرض عينة من بيانات الموظفين إذا كانت موجودة
    if 'employees' in collections:
        print("\nعينة من بيانات الموظفين:")
        sample = list(db.employees.find().limit(3))
        for emp in sample:
            print(f"- {emp.get('staff_name_ara', 'غير محدد')} ({emp.get('staff_no', 'غير محدد')})")
    
    client.close()
    
except Exception as e:
    print(f"❌ خطأ في الاتصال: {e}")
