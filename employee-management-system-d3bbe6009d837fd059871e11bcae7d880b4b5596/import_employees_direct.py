#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os
from pymongo import MongoClient
from datetime import datetime

# إضافة مسار التطبيق
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد إعدادات قاعدة البيانات
import config

def import_employees_to_mongodb():
    """
    استيراد الموظفين من ملف JSON إلى MongoDB
    """
    json_file = r"c:\Users\yaman_alne0q1\OneDrive\Desktop\3MO_A7A1\employees_fixed.json"
    
    print("🚀 بدء استيراد الموظفين إلى MongoDB...")
    print("=" * 50)
    
    # التحقق من وجود الملف
    if not os.path.exists(json_file):
        print(f"❌ الملف غير موجود: {json_file}")
        return False
    
    try:
        # الاتصال بقاعدة البيانات
        print("🔗 الاتصال بقاعدة البيانات MongoDB Atlas...")
        client = MongoClient(config.MONGO_URI)
        db = client.employees_db  # استخدام اسم قاعدة البيانات الافتراضي
        employees_collection = db.employees
        
        # اختبار الاتصال
        client.admin.command('ismaster')
        print("✅ تم الاتصال بنجاح!")
        
        # قراءة البيانات
        print("📖 قراءة البيانات من JSON...")
        with open(json_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        print(f"📊 تم العثور على {len(raw_data)} موظف في الملف")
        
        # التحقق من الموظفين الموجودين
        print("🔍 التحقق من الموظفين الموجودين...")
        existing_staff_numbers = set()
        for emp in employees_collection.find({}, {"staff_no": 1}):
            existing_staff_numbers.add(str(emp.get("staff_no")))
        
        print(f"📋 يوجد {len(existing_staff_numbers)} موظف في قاعدة البيانات حالياً")
        
        # تنظيف وتحويل البيانات
        print("🔧 تنظيف وتحويل البيانات...")
        cleaned_employees = []
        new_employees = []
        updated_employees = []
        errors = []
        
        for i, emp in enumerate(raw_data, 1):
            try:
                # تنظيف البيانات
                cleaned_emp = {}
                
                # رقم الموظف - تحويل إلى string
                staff_no = str(emp.get('staff_no', ''))
                if not staff_no:
                    errors.append(f"موظف #{i}: رقم الموظف مفقود")
                    continue
                
                cleaned_emp['staff_no'] = staff_no
                
                # اسم الموظف
                staff_name = emp.get('staff_name', '').strip()
                if staff_name == 'Loading and unloading worker':
                    # استخدام الاسم العربي إذا كان الإنجليزي وصف وظيفة
                    staff_name = emp.get('staff_name_ara', staff_name)
                cleaned_emp['staff_name'] = staff_name
                
                # الاسم العربي
                cleaned_emp['staff_name_ara'] = emp.get('staff_name_ara', '').strip()
                
                # كود الوظيفة - تحويل إلى string
                cleaned_emp['job_code'] = str(emp.get('job_code', ''))
                
                # الجنسية
                cleaned_emp['nationality_code'] = emp.get('nationality_code', '').strip()
                
                # كود الشركة
                cleaned_emp['company_code'] = emp.get('company_code', '').strip()
                
                # رقم الجواز
                pass_no = emp.get('pass_no', '').strip()
                cleaned_emp['pass_no'] = pass_no if pass_no else None
                
                # رقم البطاقة وحالتها
                card_no = emp.get('card_no', '').strip()
                special_card_statuses = [
                    'تجديد بطاقة عمل', 
                    'بطاقة عمل جديدة', 
                    'بطاقة عمل للمواطنين و دول الخليج'
                ]
                
                if card_no in special_card_statuses:
                    cleaned_emp['card_no'] = None
                    cleaned_emp['card_status'] = card_no
                elif card_no:
                    cleaned_emp['card_no'] = card_no
                else:
                    cleaned_emp['card_no'] = None
                
                # تاريخ انتهاء البطاقة
                expiry_date_str = emp.get('card_expiry_date', '').strip()
                if expiry_date_str:
                    try:
                        # تحويل التاريخ
                        if 'T' in expiry_date_str:
                            date_part = expiry_date_str.split('T')[0]
                        else:
                            date_part = expiry_date_str
                        
                        expiry_date = datetime.strptime(date_part, '%Y-%m-%d')
                        cleaned_emp['card_expiry_date'] = expiry_date
                        
                        # تحديد حالة البطاقة بناءً على التاريخ
                        if 'card_status' not in cleaned_emp:
                            today = datetime.now()
                            if expiry_date < today:
                                cleaned_emp['card_status'] = 'expired'
                            elif (expiry_date - today).days <= 30:
                                cleaned_emp['card_status'] = 'expiring'
                            else:
                                cleaned_emp['card_status'] = 'valid'
                    except Exception as e:
                        errors.append(f"موظف #{i}: تاريخ انتهاء البطاقة غير صحيح: {expiry_date_str}")
                        cleaned_emp['card_expiry_date'] = None
                else:
                    cleaned_emp['card_expiry_date'] = None
                
                # تحديد حالة البطاقة إذا لم تحدد
                if 'card_status' not in cleaned_emp:
                    cleaned_emp['card_status'] = 'missing'
                
                # تاريخ الإنشاء
                create_date_str = emp.get('create_date_time', '').strip()
                if create_date_str:
                    try:
                        if 'T' in create_date_str:
                            date_part = create_date_str.split('T')[0]
                        else:
                            date_part = create_date_str
                        cleaned_emp['create_date_time'] = datetime.strptime(date_part, '%Y-%m-%d')
                    except:
                        cleaned_emp['create_date_time'] = datetime.now()
                else:
                    cleaned_emp['create_date_time'] = datetime.now()
                
                # حالة الجواز
                if cleaned_emp.get('pass_no'):
                    cleaned_emp['passport_status'] = 'available'
                else:
                    cleaned_emp['passport_status'] = 'missing'
                
                # تصنيف الموظف (جديد أم موجود)
                if staff_no in existing_staff_numbers:
                    updated_employees.append(cleaned_emp)
                else:
                    new_employees.append(cleaned_emp)
                
                cleaned_employees.append(cleaned_emp)
                
            except Exception as e:
                errors.append(f"موظف #{i}: خطأ في معالجة البيانات: {str(e)}")
                continue
        
        print(f"\n📈 إحصائيات التنظيف:")
        print(f"  ✅ تم تنظيف: {len(cleaned_employees)} موظف")
        print(f"  🆕 موظفين جدد: {len(new_employees)}")
        print(f"  🔄 موظفين للتحديث: {len(updated_employees)}")
        print(f"  ❌ أخطاء: {len(errors)}")
        
        if errors:
            print(f"\n⚠️ أول 5 أخطاء:")
            for error in errors[:5]:
                print(f"  - {error}")
        
        # إدراج الموظفين الجدد
        if new_employees:
            print(f"\n➕ إدراج {len(new_employees)} موظف جديد...")
            result = employees_collection.insert_many(new_employees)
            print(f"✅ تم إدراج {len(result.inserted_ids)} موظف جديد")
        
        # تحديث الموظفين الموجودين
        if updated_employees:
            print(f"\n🔄 تحديث {len(updated_employees)} موظف موجود...")
            updated_count = 0
            for emp in updated_employees:
                staff_no = emp['staff_no']
                # إزالة _id إذا كان موجوداً
                emp.pop('_id', None)
                result = employees_collection.replace_one(
                    {"staff_no": staff_no}, 
                    emp
                )
                if result.modified_count > 0:
                    updated_count += 1
            print(f"✅ تم تحديث {updated_count} موظف")
        
        # إحصائيات نهائية
        total_employees = employees_collection.count_documents({})
        print(f"\n📊 إحصائيات نهائية:")
        print(f"  👥 إجمالي الموظفين في قاعدة البيانات: {total_employees}")
        
        # إحصائيات مفصلة
        print(f"\n📋 إحصائيات الجوازات:")
        passport_stats = list(employees_collection.aggregate([
            {"$group": {"_id": "$passport_status", "count": {"$sum": 1}}}
        ]))
        for stat in passport_stats:
            status = stat['_id'] or 'غير محدد'
            count = stat['count']
            print(f"  📖 {status}: {count}")
        
        print(f"\n🆔 إحصائيات البطاقات:")
        card_stats = list(employees_collection.aggregate([
            {"$group": {"_id": "$card_status", "count": {"$sum": 1}}}
        ]))
        for stat in card_stats:
            status = stat['_id'] or 'غير محدد'
            count = stat['count']
            print(f"  💳 {status}: {count}")
        
        print(f"\n🏢 إحصائيات الشركات:")
        company_stats = list(employees_collection.aggregate([
            {"$group": {"_id": "$company_code", "count": {"$sum": 1}}}
        ]))
        for stat in company_stats:
            company = stat['_id'] or 'غير محدد'
            count = stat['count']
            print(f"  🏢 {company}: {count}")
        
        print(f"\n🎉 تم استيراد البيانات بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في استيراد البيانات: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = import_employees_to_mongodb()
    
    if success:
        print("\n✅ انتهى الاستيراد بنجاح!")
        print("🚀 يمكنك الآن تشغيل النظام وستجد البيانات الجديدة")
    else:
        print("\n💥 فشل في استيراد البيانات!")
        print("🔧 تحقق من الأخطاء أعلاه وحاول مرة أخرى")
