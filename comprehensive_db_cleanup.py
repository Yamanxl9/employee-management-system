#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت شامل لتنظيف وتوحيد قاعدة بيانات الموظفين
"""

import os
import re
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone
from nationalities import NATIONALITIES
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()

# الاتصال بقاعدة البيانات
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
client = MongoClient(MONGODB_URI)
db = client.get_database()

def clean_staff_names():
    """تنظيف أسماء الموظفين"""
    print("🧹 تنظيف أسماء الموظفين...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        updates = {}
        
        # تنظيف الاسم الإنجليزي
        if emp.get('staff_name'):
            clean_name = emp['staff_name'].strip().upper()
            # إزالة المسافات الزائدة
            clean_name = re.sub(r'\s+', ' ', clean_name)
            if clean_name != emp['staff_name']:
                updates['staff_name'] = clean_name
        
        # تنظيف الاسم العربي
        if emp.get('staff_name_ara'):
            clean_name_ara = emp['staff_name_ara'].strip()
            # إزالة المسافات الزائدة
            clean_name_ara = re.sub(r'\s+', ' ', clean_name_ara)
            if clean_name_ara != emp['staff_name_ara']:
                updates['staff_name_ara'] = clean_name_ara
        
        if updates:
            db.employees.update_one({'_id': emp['_id']}, {'$set': updates})
            updated_count += 1
            print(f"   ✅ محدث: {emp.get('staff_no', 'N/A')}")
    
    print(f"✅ تم تحديث {updated_count} اسم موظف")

def standardize_staff_numbers():
    """توحيد أرقام الموظفين"""
    print("\n🔢 توحيد أرقام الموظفين...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        if emp.get('staff_no'):
            # إزالة المسافات والرموز الخاصة
            clean_staff_no = re.sub(r'[^\d]', '', str(emp['staff_no']))
            
            if clean_staff_no != str(emp['staff_no']):
                db.employees.update_one(
                    {'_id': emp['_id']}, 
                    {'$set': {'staff_no': clean_staff_no}}
                )
                updated_count += 1
                print(f"   ✅ محدث رقم الموظف: {emp['staff_no']} → {clean_staff_no}")
    
    print(f"✅ تم تحديث {updated_count} رقم موظف")

def standardize_passport_numbers():
    """توحيد أرقام الجوازات"""
    print("\n📘 توحيد أرقام الجوازات...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        if emp.get('pass_no'):
            # تنظيف رقم الجواز - إزالة المسافات والحفاظ على الأحرف والأرقام
            clean_pass_no = re.sub(r'\s+', '', str(emp['pass_no']).upper())
            
            if clean_pass_no != str(emp['pass_no']):
                db.employees.update_one(
                    {'_id': emp['_id']}, 
                    {'$set': {'pass_no': clean_pass_no}}
                )
                updated_count += 1
                print(f"   ✅ محدث رقم الجواز: {emp['staff_no']}")
    
    print(f"✅ تم تحديث {updated_count} رقم جواز")

def standardize_card_numbers():
    """توحيد أرقام البطاقات"""
    print("\n💳 توحيد أرقام البطاقات...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        if emp.get('card_no'):
            # تنظيف رقم البطاقة - أرقام فقط
            clean_card_no = re.sub(r'[^\d]', '', str(emp['card_no']))
            
            if clean_card_no != str(emp['card_no']):
                db.employees.update_one(
                    {'_id': emp['_id']}, 
                    {'$set': {'card_no': clean_card_no}}
                )
                updated_count += 1
                print(f"   ✅ محدث رقم البطاقة: {emp['staff_no']}")
    
    print(f"✅ تم تحديث {updated_count} رقم بطاقة")

def standardize_nationalities():
    """توحيد الجنسيات"""
    print("\n🌍 توحيد الجنسيات...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        nationality_code = emp.get('nationality_code', '').upper()
        
        if nationality_code and nationality_code in NATIONALITIES:
            nationality_info = NATIONALITIES[nationality_code]
            
            updates = {
                'nationality_code': nationality_code,
                'nationality_en': nationality_info['en'],
                'nationality_ar': nationality_info['ar']
            }
            
            # إزالة الحقول القديمة غير المرغوب فيها
            unset_fields = {}
            if emp.get('nationality_code_old'):
                unset_fields['nationality_code_old'] = ""
            if emp.get('nationality_display'):
                unset_fields['nationality_display'] = ""
            
            update_query = {'$set': updates}
            if unset_fields:
                update_query['$unset'] = unset_fields
            
            db.employees.update_one({'_id': emp['_id']}, update_query)
            updated_count += 1
            print(f"   ✅ محدث جنسية: {emp.get('staff_no', 'N/A')} - {nationality_info['ar']}")
        
        elif nationality_code:
            print(f"   ⚠️ جنسية غير معروفة: {nationality_code} للموظف {emp.get('staff_no', 'N/A')}")
    
    print(f"✅ تم تحديث {updated_count} جنسية")

def standardize_dates():
    """توحيد التواريخ"""
    print("\n📅 توحيد التواريخ...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        updates = {}
        
        # توحيد تاريخ انتهاء البطاقة
        if emp.get('card_expiry_date'):
            expiry_date = emp['card_expiry_date']
            
            if isinstance(expiry_date, str):
                try:
                    # تحويل التاريخ النصي إلى datetime
                    parsed_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
                    updates['card_expiry_date'] = parsed_date
                except:
                    print(f"   ⚠️ تاريخ غير صالح: {expiry_date} للموظف {emp.get('staff_no', 'N/A')}")
            
            elif hasattr(expiry_date, 'tzinfo') and expiry_date.tzinfo is None:
                # إضافة timezone للتواريخ التي لا تحتوي عليه
                updates['card_expiry_date'] = expiry_date.replace(tzinfo=timezone.utc)
        
        # توحيد تاريخ الإنشاء
        if emp.get('create_date_time'):
            create_date = emp['create_date_time']
            
            if isinstance(create_date, str):
                try:
                    parsed_date = datetime.fromisoformat(create_date.replace('Z', '+00:00'))
                    updates['create_date_time'] = parsed_date
                except:
                    # في حالة فشل التحويل، استخدم التاريخ الحالي
                    updates['create_date_time'] = datetime.now(timezone.utc)
            
            elif hasattr(create_date, 'tzinfo') and create_date.tzinfo is None:
                updates['create_date_time'] = create_date.replace(tzinfo=timezone.utc)
        else:
            # إضافة تاريخ الإنشاء إذا لم يكن موجوداً
            updates['create_date_time'] = datetime.now(timezone.utc)
        
        if updates:
            db.employees.update_one({'_id': emp['_id']}, {'$set': updates})
            updated_count += 1
    
    print(f"✅ تم تحديث {updated_count} تاريخ")

def validate_job_codes():
    """التحقق من صحة رموز الوظائف"""
    print("\n💼 التحقق من رموز الوظائف...")
    
    # الحصول على جميع رموز الوظائف الصحيحة
    valid_job_codes = set(job['job_code'] for job in db.jobs.find({}, {'job_code': 1}))
    
    employees = list(db.employees.find())
    invalid_count = 0
    
    for emp in employees:
        job_code = emp.get('job_code')
        if job_code and job_code not in valid_job_codes:
            print(f"   ⚠️ رمز وظيفة غير صالح: {job_code} للموظف {emp.get('staff_no', 'N/A')}")
            invalid_count += 1
    
    if invalid_count == 0:
        print("✅ جميع رموز الوظائف صحيحة")
    else:
        print(f"❌ وجد {invalid_count} رمز وظيفة غير صالح")

def validate_company_codes():
    """التحقق من صحة رموز الشركات"""
    print("\n🏢 التحقق من رموز الشركات...")
    
    # الحصول على جميع رموز الشركات الصحيحة
    valid_company_codes = set(company['company_code'] for company in db.companies.find({}, {'company_code': 1}))
    
    employees = list(db.employees.find())
    invalid_count = 0
    
    for emp in employees:
        company_code = emp.get('company_code')
        if company_code and company_code not in valid_company_codes:
            print(f"   ⚠️ رمز شركة غير صالح: {company_code} للموظف {emp.get('staff_no', 'N/A')}")
            invalid_count += 1
    
    if invalid_count == 0:
        print("✅ جميع رموز الشركات صحيحة")
    else:
        print(f"❌ وجد {invalid_count} رمز شركة غير صالح")

def remove_empty_fields():
    """إزالة الحقول الفارغة"""
    print("\n🗑️ إزالة الحقول الفارغة...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        unset_fields = {}
        
        for field, value in emp.items():
            if field != '_id' and (value is None or value == '' or value == 'null'):
                unset_fields[field] = ""
        
        if unset_fields:
            db.employees.update_one({'_id': emp['_id']}, {'$unset': unset_fields})
            updated_count += 1
    
    print(f"✅ تم تنظيف {updated_count} موظف من الحقول الفارغة")

def add_missing_fields():
    """إضافة الحقول المفقودة"""
    print("\n➕ إضافة الحقول المفقودة...")
    
    employees = list(db.employees.find())
    updated_count = 0
    
    for emp in employees:
        updates = {}
        
        # إضافة حقول مفقودة بقيم افتراضية
        if not emp.get('create_date_time'):
            updates['create_date_time'] = datetime.now(timezone.utc)
        
        # التأكد من وجود حقول الجنسية
        if emp.get('nationality_code') and not emp.get('nationality_en'):
            nationality_code = emp['nationality_code'].upper()
            if nationality_code in NATIONALITIES:
                updates['nationality_en'] = NATIONALITIES[nationality_code]['en']
                updates['nationality_ar'] = NATIONALITIES[nationality_code]['ar']
        
        if updates:
            db.employees.update_one({'_id': emp['_id']}, {'$set': updates})
            updated_count += 1
    
    print(f"✅ تم إضافة حقول مفقودة لـ {updated_count} موظف")

def remove_duplicate_employees():
    """إزالة الموظفين المكررين"""
    print("\n🔄 إزالة الموظفين المكررين...")
    
    pipeline = [
        {
            "$group": {
                "_id": "$staff_no",
                "count": {"$sum": 1},
                "docs": {"$push": "$$ROOT"}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]
    
    duplicates = list(db.employees.aggregate(pipeline))
    removed_count = 0
    
    for duplicate_group in duplicates:
        staff_no = duplicate_group["_id"]
        docs = duplicate_group["docs"]
        
        # الاحتفاظ بأحدث نسخة
        docs_sorted = sorted(docs, key=lambda x: x.get('create_date_time', datetime.min), reverse=True)
        keep_doc = docs_sorted[0]
        remove_docs = docs_sorted[1:]
        
        for doc in remove_docs:
            db.employees.delete_one({"_id": doc["_id"]})
            removed_count += 1
            print(f"   ❌ حُذفت نسخة مكررة للموظف: {staff_no}")
    
    if removed_count == 0:
        print("✅ لا توجد موظفين مكررين")
    else:
        print(f"✅ تم حذف {removed_count} موظف مكرر")

def create_data_consistency_report():
    """إنشاء تقرير تناسق البيانات"""
    print("\n📊 إنشاء تقرير تناسق البيانات...")
    
    employees = list(db.employees.find())
    report = {
        'total_employees': len(employees),
        'missing_names': 0,
        'missing_staff_no': 0,
        'missing_passport': 0,
        'missing_card': 0,
        'missing_company': 0,
        'missing_job': 0,
        'expired_cards': 0,
        'valid_records': 0
    }
    
    for emp in employees:
        if not emp.get('staff_name') or not emp.get('staff_name_ara'):
            report['missing_names'] += 1
        if not emp.get('staff_no'):
            report['missing_staff_no'] += 1
        if not emp.get('pass_no'):
            report['missing_passport'] += 1
        if not emp.get('card_no'):
            report['missing_card'] += 1
        if not emp.get('company_code'):
            report['missing_company'] += 1
        if not emp.get('job_code'):
            report['missing_job'] += 1
        
        # فحص انتهاء البطاقة
        if emp.get('card_expiry_date'):
            expiry_date = emp['card_expiry_date']
            if isinstance(expiry_date, str):
                try:
                    expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
                except:
                    continue
            
            if expiry_date.tzinfo is None:
                expiry_date = expiry_date.replace(tzinfo=timezone.utc)
            
            if expiry_date < datetime.now(timezone.utc):
                report['expired_cards'] += 1
        
        # تحديد السجلات الصحيحة
        if all([
            emp.get('staff_name'),
            emp.get('staff_name_ara'),
            emp.get('staff_no'),
            emp.get('company_code'),
            emp.get('job_code')
        ]):
            report['valid_records'] += 1
    
    print("\n📋 تقرير تناسق البيانات:")
    print(f"   📊 إجمالي الموظفين: {report['total_employees']}")
    print(f"   ✅ سجلات صحيحة: {report['valid_records']}")
    print(f"   ❌ أسماء مفقودة: {report['missing_names']}")
    print(f"   ❌ أرقام موظفين مفقودة: {report['missing_staff_no']}")
    print(f"   ❌ جوازات مفقودة: {report['missing_passport']}")
    print(f"   ❌ بطاقات مفقودة: {report['missing_card']}")
    print(f"   ❌ شركات مفقودة: {report['missing_company']}")
    print(f"   ❌ وظائف مفقودة: {report['missing_job']}")
    print(f"   🔴 بطاقات منتهية: {report['expired_cards']}")
    
    quality_percentage = (report['valid_records'] / report['total_employees'] * 100) if report['total_employees'] > 0 else 0
    print(f"\n🎯 نسبة جودة البيانات: {quality_percentage:.1f}%")
    
    return report

def main():
    """الدالة الرئيسية لتنظيف قاعدة البيانات"""
    print("🧹 بدء عملية التنظيف الشاملة لقاعدة بيانات الموظفين")
    print("=" * 80)
    
    try:
        # 1. تنظيف الأسماء
        clean_staff_names()
        
        # 2. توحيد أرقام الموظفين
        standardize_staff_numbers()
        
        # 3. توحيد أرقام الجوازات
        standardize_passport_numbers()
        
        # 4. توحيد أرقام البطاقات
        standardize_card_numbers()
        
        # 5. توحيد الجنسيات
        standardize_nationalities()
        
        # 6. توحيد التواريخ
        standardize_dates()
        
        # 7. إزالة الحقول الفارغة
        remove_empty_fields()
        
        # 8. إضافة الحقول المفقودة
        add_missing_fields()
        
        # 9. إزالة المكررات
        remove_duplicate_employees()
        
        # 10. التحقق من صحة البيانات
        validate_job_codes()
        validate_company_codes()
        
        # 11. إنشاء تقرير التناسق
        create_data_consistency_report()
        
        print("\n" + "=" * 80)
        print("✅ تم الانتهاء من التنظيف الشامل لقاعدة البيانات!")
        print("🎉 قاعدة البيانات أصبحت منظمة ومتناسقة")
        
    except Exception as e:
        print(f"❌ خطأ أثناء التنظيف: {e}")
        logger.error(f"Database cleanup error: {e}")

if __name__ == "__main__":
    main()
