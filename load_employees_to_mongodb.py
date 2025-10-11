import json
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import sys

# تحميل متغيرات البيئة
load_dotenv()

# الاتصال بـ MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
client = MongoClient(MONGODB_URI)
db = client.employees_db

def convert_timestamp_to_datetime(timestamp):
    """تحويل timestamp إلى datetime"""
    if timestamp and timestamp != 0:
        try:
            return datetime.fromtimestamp(timestamp / 1000)  # تحويل من milliseconds
        except:
            return None
    return None

def load_employees_from_load_data_py():
    """استخراج بيانات الموظفين من ملف load_data.py"""
    
    # استيراد البيانات من ملف load_data.py
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # قراءة محتوى الملف مباشرة
    with open('load_data.py', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # البحث عن بداية قائمة employees_data
    start_marker = 'employees_data = ['
    end_marker = '    ]'
    
    start_index = content.find(start_marker)
    if start_index == -1:
        print("❌ لم يتم العثور على بيانات الموظفين في الملف")
        return []
    
    # العثور على نهاية القائمة
    bracket_count = 0
    in_data_section = False
    employees_data = []
    
    # استخراج البيانات من الملف
    lines = content[start_index:].split('\n')
    current_employee = {}
    in_employee = False
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('{'):
            in_employee = True
            current_employee = {}
        elif line.startswith('}'):
            if in_employee and current_employee:
                employees_data.append(current_employee)
                current_employee = {}
            in_employee = False
        elif in_employee and ':' in line:
            # استخراج المفتاح والقيمة
            if line.endswith(','):
                line = line[:-1]
            
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip().strip('"')
                value = parts[1].strip()
                
                # تحويل القيم
                if value == 'None':
                    value = None
                elif value == 'null':
                    value = None
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]  # إزالة الاقتباس
                elif value.replace('.', '').isdigit():
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                
                current_employee[key] = value
        
        # التوقف عند نهاية قائمة البيانات
        if line.startswith(']') and 'employees_data' not in line:
            break
    
    print(f"📊 تم استخراج {len(employees_data)} موظف من الملف")
    return employees_data

def migrate_employees_to_mongodb():
    """نقل بيانات الموظفين إلى MongoDB"""
    
    print("🔄 بدء نقل بيانات الموظفين إلى MongoDB...")
    
    # جلب بيانات الموظفين
    employees_data = load_employees_from_load_data_py()
    
    if not employees_data:
        print("❌ لا توجد بيانات موظفين للنقل")
        return
    
    # تنظيف المجموعة الحالية
    db.employees.delete_many({})
    print("🗑️ تم مسح البيانات القديمة")
    
    # تحضير البيانات للإدراج
    employees_to_insert = []
    
    for emp_data in employees_data:
        try:
            # تحويل أسماء الحقول لتتطابق مع MongoDB schema
            employee = {
                'staff_no': str(emp_data.get('StaffNo', '')),
                'staff_name': emp_data.get('StaffName', ''),
                'staff_name_ara': emp_data.get('StaffName_ara', ''),
                'job_code': emp_data.get('Job_Code'),
                'pass_no': emp_data.get('PassNo'),
                'nationality_code': emp_data.get('Nationality_Code', ''),
                'company_code': emp_data.get('Company_Code', ''),
                'card_no': emp_data.get('CardNo'),
                'card_expiry_date': convert_timestamp_to_datetime(emp_data.get('CardExpiryDate')),
                'create_date_time': convert_timestamp_to_datetime(emp_data.get('CreateDateTime')) or datetime.now()
            }
            
            employees_to_insert.append(employee)
            
        except Exception as e:
            print(f"⚠️ خطأ في معالجة بيانات الموظف {emp_data.get('StaffName', 'غير معروف')}: {e}")
            continue
    
    if employees_to_insert:
        # إدراج البيانات
        result = db.employees.insert_many(employees_to_insert)
        print(f"✅ تم إدراج {len(result.inserted_ids)} موظف بنجاح في MongoDB")
        
        # إظهار إحصائيات
        total_employees = db.employees.count_documents({})
        employees_with_passports = db.employees.count_documents({'pass_no': {'$ne': None, '$ne': ''}})
        employees_with_cards = db.employees.count_documents({'card_no': {'$ne': None}})
        
        print(f"📊 إحصائيات البيانات:")
        print(f"   - إجمالي الموظفين: {total_employees}")
        print(f"   - موظفين لديهم جوازات: {employees_with_passports}")
        print(f"   - موظفين لديهم بطاقات: {employees_with_cards}")
        
        # عرض عينة من البيانات
        print(f"\n👥 عينة من الموظفين المضافين:")
        sample_employees = db.employees.find().limit(5)
        for emp in sample_employees:
            print(f"   - {emp.get('staff_name_ara', emp.get('staff_name', ''))} ({emp.get('staff_no')})")
    
    else:
        print("❌ لم يتم العثور على بيانات صالحة للإدراج")

def verify_data():
    """التحقق من البيانات المنقولة"""
    print("\n🔍 التحقق من البيانات...")
    
    total = db.employees.count_documents({})
    companies = db.employees.distinct('company_code')
    nationalities = db.employees.distinct('nationality_code')
    
    print(f"✅ إجمالي الموظفين: {total}")
    print(f"✅ الشركات: {companies}")
    print(f"✅ الجنسيات: {nationalities}")

if __name__ == "__main__":
    try:
        print("🚀 بدء عملية نقل البيانات إلى MongoDB Atlas...")
        migrate_employees_to_mongodb()
        verify_data()
        print("🎉 تمت عملية النقل بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في عملية النقل: {e}")
    finally:
        client.close()
