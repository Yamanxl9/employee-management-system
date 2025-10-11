#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتحديث قاعدة البيانات وتحويل رموز الجنسيات إلى أسماء كاملة
"""

from flask_pymongo import PyMongo
from flask import Flask
import os
from dotenv import load_dotenv
from nationalities import NATIONALITIES

# تحميل متغيرات البيئة
load_dotenv()

# إعداد Flask و MongoDB
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
mongo = PyMongo(app)

def update_nationalities_in_database():
    """تحديث رموز الجنسيات إلى أسماء كاملة في قاعدة البيانات"""
    print("🔄 بدء تحديث قاعدة البيانات...")
    
    with app.app_context():
        try:
            # التحقق من الاتصال بقاعدة البيانات
            print("🔌 اختبار الاتصال بقاعدة البيانات...")
            db_status = mongo.db.command("ping")
            print(f"✅ تم الاتصال بقاعدة البيانات بنجاح: {db_status}")
            
            # جلب جميع الموظفين
            employees = list(mongo.db.employees.find({}))
            print(f"📊 تم العثور على {len(employees)} موظف")
            
            if len(employees) == 0:
                print("⚠️  لا توجد بيانات موظفين في قاعدة البيانات!")
                return False
            
            updated_count = 0
            
            for employee in employees:
                nationality_code = employee.get('nationality_code', '')
                
                if nationality_code and nationality_code in NATIONALITIES:
                    # الحصول على الاسم الكامل للجنسية
                    nationality_ar = NATIONALITIES[nationality_code]['ar']
                    nationality_en = NATIONALITIES[nationality_code]['en']
                    
                    # تحديث بيانات الموظف - تغيير nationality_code إلى الاسم العربي
                    update_data = {
                        'nationality_code': nationality_ar,    # تحويل إلى الاسم العربي
                        'nationality_code_old': nationality_code,  # حفظ الرمز القديم للمرجع
                        'nationality_ar': nationality_ar,     # الاسم العربي
                        'nationality_en': nationality_en      # الاسم الإنجليزي
                    }
                    
                    # تحديث قاعدة البيانات
                    result = mongo.db.employees.update_one(
                        {'_id': employee['_id']},
                        {'$set': update_data}
                    )
                    
                    if result.modified_count > 0:
                        updated_count += 1
                        print(f"✅ تم تحديث: {employee.get('staff_name', 'غير محدد')} - {nationality_code} → {nationality_ar}")
                
                elif nationality_code:
                    print(f"⚠️  رمز جنسية غير معروف: {nationality_code} للموظف: {employee.get('staff_name', 'غير محدد')}")
            
            print(f"\n🎉 تم تحديث {updated_count} موظف بنجاح!")
            
            # إحصائيات الجنسيات بعد التحديث
            print("\n📈 إحصائيات الجنسيات بعد التحديث:")
            try:
                nationalities_stats = mongo.db.employees.aggregate([
                    {'$group': {
                        '_id': '$nationality_code', 
                        'count': {'$sum': 1}
                    }},
                    {'$sort': {'count': -1}}
                ])
                
                for stat in nationalities_stats:
                    print(f"- {stat['_id']}: {stat['count']} موظف")
                    
            except Exception as e:
                print(f"⚠️  خطأ في جلب الإحصائيات: {e}")
                
        except Exception as e:
            print(f"❌ خطأ في تحديث قاعدة البيانات: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

def update_companies_collection():
    """تحديث مجموعة الشركات لإضافة أسماء إنجليزية إذا لم تكن موجودة"""
    print("\n🔄 تحديث بيانات الشركات...")
    
    with app.app_context():
        try:
            companies = list(mongo.db.companies.find({}))
            
            for company in companies:
                if 'company_name_eng' not in company:
                    # إضافة اسم إنجليزي افتراضي إذا لم يكن موجوداً
                    english_name = company.get('company_name_ara', company.get('company_code', 'Unknown'))
                    
                    mongo.db.companies.update_one(
                        {'_id': company['_id']},
                        {'$set': {'company_name_eng': english_name}}
                    )
                    
                    print(f"✅ تم إضافة اسم إنجليزي للشركة: {company.get('company_code')}")
                    
        except Exception as e:
            print(f"❌ خطأ في تحديث الشركات: {e}")

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🚀 سكريبت تحديث قاعدة البيانات - نظام إدارة الموظفين")
    print("=" * 60)
    
    # تحديث الجنسيات
    if update_nationalities_in_database():
        print("\n✅ تم تحديث الجنسيات بنجاح!")
    else:
        print("\n❌ فشل في تحديث الجنسيات!")
        return
    
    # تحديث الشركات
    update_companies_collection()
    
    print("\n" + "=" * 60)
    print("🎉 تم الانتهاء من تحديث قاعدة البيانات بنجاح!")
    print("=" * 60)

if __name__ == "__main__":
    main()
