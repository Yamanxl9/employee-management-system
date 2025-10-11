#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لاستيراد بيانات الموظفين من ملف JSON
Import Employees from JSON Script
"""

import json
import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('import_employees.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def get_database_connection():
    """الاتصال بقاعدة البيانات"""
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = os.getenv('MONGODB_DB', 'employees_db')
        
        logger.info(f"🔗 محاولة الاتصال بقاعدة البيانات: {database_name}")
        
        client = MongoClient(mongodb_uri)
        client.admin.command('ping')
        
        db = client[database_name]
        logger.info(f"✅ نجح الاتصال بقاعدة البيانات: {database_name}")
        
        return client, db
        
    except PyMongoError as e:
        logger.error(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
        return None, None
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
        return None, None

def parse_date(date_str):
    """تحويل التاريخ من التنسيق المعطى إلى datetime"""
    if not date_str or date_str.strip() == "":
        return None
    
    try:
        # إزالة المسافات والأسطر الجديدة
        date_str = date_str.strip()
        
        # تنسيق التاريخ: "16-Aug-25"
        if len(date_str.split('-')) == 3:
            day, month_abbr, year = date_str.split('-')
            
            # تحويل اختصار الشهر إلى رقم
            months = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            
            if month_abbr in months:
                month = months[month_abbr]
                
                # تحويل السنة (25 -> 2025)
                if len(year) == 2:
                    year = int('20' + year)
                else:
                    year = int(year)
                
                return datetime(year, month, int(day))
        
        # إذا كان التاريخ "01-Jan-25" أو مشابه لتاريخ افتراضي
        if date_str == "01-Jan-25":
            return None
            
    except Exception as e:
        logger.warning(f"⚠️ لا يمكن تحويل التاريخ: {date_str} - {e}")
    
    return None

def clean_string(text):
    """تنظيف النص من الأسطر الجديدة والمسافات الزائدة"""
    if not text:
        return ""
    
    # إزالة الأسطر الجديدة والمسافات الزائدة
    cleaned = text.replace('\n', ' ').replace('\r', '').strip()
    
    # إزالة المسافات المتعددة
    while '  ' in cleaned:
        cleaned = cleaned.replace('  ', ' ')
    
    return cleaned

def prepare_employee_data(employee_json):
    """تحضير بيانات الموظف للإدراج في قاعدة البيانات"""
    try:
        # تنظيف البيانات
        staff_no = str(employee_json.get('StaffNo', '')).strip()
        staff_name = clean_string(employee_json.get('StaffName', ''))
        staff_name_ara = clean_string(employee_json.get('StaffName_ara', ''))
        job_code = employee_json.get('Job_Code', 1)
        pass_no = clean_string(employee_json.get('PassNo', ''))
        nationality_code = employee_json.get('Nationality_Code', '').strip()
        company_code = employee_json.get('Company_Code', '').strip()
        card_no = clean_string(employee_json.get('CardNo', ''))
        card_expiry_date = parse_date(employee_json.get('CardExpiryDate', ''))
        
        # تحديد حالة الجواز
        passport_status = "متوفر" if pass_no and pass_no != "" else "مفقود"
        
        # تحديد حالة البطاقة
        card_status = "مفقودة"
        if card_no and card_no != "":
            if card_expiry_date:
                today = datetime.now()
                if card_expiry_date < today:
                    card_status = "منتهية الصلاحية"
                elif (card_expiry_date - today).days <= 30:
                    card_status = "تنتهي قريباً"
                else:
                    card_status = "سارية المفعول"
            else:
                card_status = "بدون تاريخ انتهاء"
        
        employee_data = {
            "staff_no": staff_no,
            "staff_name": staff_name,
            "staff_name_ara": staff_name_ara,
            "job_code": job_code,
            "pass_no": pass_no,
            "nationality_code": nationality_code,
            "company_code": company_code,
            "card_no": card_no,
            "card_expiry_date": card_expiry_date,
            "passport_status": passport_status,
            "card_status": card_status,
            "create_date_time": datetime.now(),
            "last_updated": datetime.now()
        }
        
        return employee_data
        
    except Exception as e:
        logger.error(f"❌ خطأ في تحضير بيانات الموظف: {e}")
        return None

def import_employees_from_json(db, json_file_path):
    """استيراد الموظفين من ملف JSON"""
    try:
        logger.info(f"📂 قراءة ملف: {json_file_path}")
        
        # قراءة ملف JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            employees_data = json.load(file)
        
        logger.info(f"📊 عدد الموظفين في الملف: {len(employees_data)}")
        
        # تحضير البيانات
        prepared_employees = []
        seen_staff_numbers = set()
        
        for i, employee_json in enumerate(employees_data):
            employee_data = prepare_employee_data(employee_json)
            if employee_data:
                staff_no = employee_data['staff_no']
                
                # التحقق من التكرار
                if staff_no in seen_staff_numbers:
                    logger.warning(f"⚠️ تخطي الموظف المكرر رقم {staff_no} في السطر {i+1}")
                    continue
                    
                seen_staff_numbers.add(staff_no)
                prepared_employees.append(employee_data)
            else:
                logger.warning(f"⚠️ تخطي الموظف رقم {i+1} بسبب خطأ في البيانات")
        
        logger.info(f"✅ تم تحضير {len(prepared_employees)} موظف للإدراج")
        
        # حذف الموظفين الموجودين أولاً
        logger.info("🗑️ حذف الموظفين الموجودين...")
        result = db.employees.delete_many({})
        logger.info(f"🗑️ تم حذف {result.deleted_count} موظف")
        
        # إدراج الموظفين الجدد
        if prepared_employees:
            logger.info("📥 إدراج الموظفين الجدد...")
            result = db.employees.insert_many(prepared_employees)
            logger.info(f"✅ تم إدراج {len(result.inserted_ids)} موظف بنجاح")
            
            # إحصائيات
            total_employees = db.employees.count_documents({})
            employees_with_passport = db.employees.count_documents({"passport_status": "متوفر"})
            employees_without_passport = db.employees.count_documents({"passport_status": "مفقود"})
            employees_with_valid_card = db.employees.count_documents({"card_status": "سارية المفعول"})
            employees_with_expired_card = db.employees.count_documents({"card_status": "منتهية الصلاحية"})
            employees_with_expiring_card = db.employees.count_documents({"card_status": "تنتهي قريباً"})
            employees_without_card = db.employees.count_documents({"card_status": "مفقودة"})
            
            logger.info("📊 إحصائيات الموظفين:")
            logger.info(f"   - إجمالي الموظفين: {total_employees}")
            logger.info(f"   - لديهم جواز: {employees_with_passport}")
            logger.info(f"   - بدون جواز: {employees_without_passport}")
            logger.info(f"   - بطاقة سارية: {employees_with_valid_card}")
            logger.info(f"   - بطاقة منتهية: {employees_with_expired_card}")
            logger.info(f"   - بطاقة تنتهي قريباً: {employees_with_expiring_card}")
            logger.info(f"   - بدون بطاقة: {employees_without_card}")
            
            return True
        else:
            logger.error("❌ لا توجد بيانات صحيحة للإدراج")
            return False
            
    except FileNotFoundError:
        logger.error(f"❌ الملف غير موجود: {json_file_path}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"❌ خطأ في تحليل ملف JSON: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ خطأ في استيراد الموظفين: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء استيراد بيانات الموظفين...")
    
    # الاتصال بقاعدة البيانات
    client, db = get_database_connection()
    if db is None:
        return False
    
    try:
        # مسار ملف JSON
        json_file_path = "Book1.json"
        
        # التحقق من وجود الملف
        if not os.path.exists(json_file_path):
            logger.error(f"❌ الملف غير موجود: {json_file_path}")
            return False
        
        # استيراد الموظفين
        if import_employees_from_json(db, json_file_path):
            logger.info("🎉 تم استيراد بيانات الموظفين بنجاح!")
            return True
        else:
            logger.error("❌ فشل في استيراد بيانات الموظفين!")
            return False
            
    except Exception as e:
        logger.error(f"❌ خطأ في العملية الرئيسية: {e}")
        return False
    finally:
        # إغلاق الاتصال
        if client:
            client.close()
            logger.info("🔐 تم إغلاق الاتصال بقاعدة البيانات")

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ تم استيراد بيانات الموظفين بنجاح!")
        print("💡 يمكنك الآن فتح التطبيق ومشاهدة جميع الموظفين")
    else:
        print("\n❌ فشل في استيراد بيانات الموظفين!")
        exit(1)
