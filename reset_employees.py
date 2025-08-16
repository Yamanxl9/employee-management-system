from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

try:
    # الاتصال بقاعدة البيانات
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['employee_management']
    
    print("🗑️ مسح جميع بيانات الموظفين...")
    
    # مسح جميع الموظفين
    result = db.employees.delete_many({})
    print(f"✅ تم مسح {result.deleted_count} موظف")
    
    # إعادة تحميل الموظفين من Book1.json
    print("📂 تحميل الموظفين من Book1.json...")
    
    with open('Book1.json', 'r', encoding='utf-8') as f:
        employees_data = json.load(f)
    
    print(f"📁 قراءة {len(employees_data)} موظف من الملف")
    
    # تحويل البيانات للهيكل الصحيح
    employees_to_insert = []
    for emp in employees_data:
        try:
            # تحويل تاريخ انتهاء البطاقة
            card_expiry = None
            if emp.get('CardExpiryDate'):
                try:
                    card_expiry = datetime.strptime(emp['CardExpiryDate'], '%Y-%m-%d')
                except:
                    card_expiry = None
            
            # تحويل تاريخ الإنشاء
            create_date = None
            if emp.get('CreateDate'):
                try:
                    create_date = datetime.strptime(emp['CreateDate'], '%Y-%m-%d %H:%M:%S')
                except:
                    create_date = datetime.now()
            else:
                create_date = datetime.now()
            
            employee_doc = {
                'staff_no': str(emp['StaffNo']).strip(),
                'staff_name': emp['StaffName'].strip() if emp.get('StaffName') else '',
                'staff_name_ara': emp.get('StaffName_ara', '').strip(),
                'job_code': int(emp['Job_Code']) if emp.get('Job_Code') else 1,
                'nationality_code': emp.get('Nationality_Code', '').strip(),
                'company_code': emp.get('Company_Code', '').strip(),
                'pass_no': emp.get('PassNo', '').strip(),
                'card_no': emp.get('CardNo', '').strip(),
                'card_expiry_date': card_expiry,
                'create_date_time': create_date
            }
            
            employees_to_insert.append(employee_doc)
            
        except Exception as e:
            print(f"⚠️ خطأ في معالجة الموظف {emp.get('StaffNo', 'غير محدد')}: {e}")
            continue
    
    # إدراج الموظفين الجدد
    if employees_to_insert:
        result = db.employees.insert_many(employees_to_insert)
        print(f"✅ تم إدراج {len(result.inserted_ids)} موظف في قاعدة البيانات")
    
    # التحقق من النتائج
    total_employees = db.employees.count_documents({})
    print(f"📊 إجمالي الموظفين في قاعدة البيانات: {total_employees}")
    
    # عرض عينة
    sample_employees = list(db.employees.find().limit(3))
    print("\n🔍 عينة من الموظفين:")
    for emp in sample_employees:
        print(f"  {emp['staff_no']}: {emp['staff_name']} - {emp.get('staff_name_ara', 'غير محدد')}")
    
    print("\n✅ تم إعادة تحميل جميع البيانات بنجاح!")
    
except Exception as e:
    print(f"❌ خطأ عام: {e}")
finally:
    if 'client' in locals():
        client.close()
