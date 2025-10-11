#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت بسيط لتحديث الجنسيات في قاعدة البيانات
"""

import os
from pymongo import MongoClient
from nationalities import NATIONALITIES

def main():
    print("🚀 بدء تحديث قاعدة البيانات...")
    
    try:
        # الاتصال بقاعدة البيانات
        # استخدام نفس الاتصال من متغير البيئة أو الافتراضي
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
        
        # إذا كان الـ URI يحتوي على atlas (MongoDB Cloud)
        if 'mongodb+srv' in mongo_uri or 'mongodb.net' in mongo_uri:
            # استخدام MongoDB Atlas
            mongo_uri = 'mongodb+srv://yamanxl9:1997@cluster0.uquwf.mongodb.net/employees_db?retryWrites=true&w=majority'
        
        print(f"🔌 الاتصال بقاعدة البيانات...")
        client = MongoClient(mongo_uri)
        db = client.employees_db
        
        # اختبار الاتصال
        db.command("ping")
        print("✅ تم الاتصال بنجاح!")
        
        # جلب الموظفين
        employees_collection = db.employees
        employees = list(employees_collection.find({}))
        print(f"📊 عدد الموظفين: {len(employees)}")
        
        if len(employees) == 0:
            print("❌ لا توجد بيانات موظفين!")
            return
        
        # عرض عينة من البيانات الحالية
        print("\n📝 عينة من البيانات الحالية:")
        for i, emp in enumerate(employees[:3]):
            print(f"   {i+1}. {emp.get('staff_name', 'غير محدد')} - الجنسية: {emp.get('nationality_code', 'غير محدد')}")
        
        # تأكيد التحديث
        confirm = input("\n⚠️  هل تريد المتابعة مع التحديث؟ (y/n): ").lower()
        if confirm not in ['y', 'yes', 'نعم']:
            print("❌ تم إلغاء التحديث.")
            return
        
        # تحديث الجنسيات
        updated_count = 0
        
        for employee in employees:
            current_nationality = employee.get('nationality_code', '')
            
            if current_nationality and current_nationality in NATIONALITIES:
                # تحويل إلى الاسم العربي الكامل
                new_nationality = NATIONALITIES[current_nationality]['ar']
                
                # تحديث المستند
                result = employees_collection.update_one(
                    {'_id': employee['_id']},
                    {
                        '$set': {
                            'nationality_code': new_nationality,
                            'nationality_code_old': current_nationality,
                            'nationality_en': NATIONALITIES[current_nationality]['en'],
                            'nationality_ar': new_nationality
                        }
                    }
                )
                
                if result.modified_count > 0:
                    updated_count += 1
                    print(f"✅ {employee.get('staff_name', 'غير محدد')}: {current_nationality} → {new_nationality}")
        
        print(f"\n🎉 تم تحديث {updated_count} موظف بنجاح!")
        
        # عرض الإحصائيات الجديدة
        print("\n📊 إحصائيات الجنسيات الجديدة:")
        nationality_stats = {}
        for emp in employees_collection.find({}):
            nat = emp.get('nationality_code', 'غير محدد')
            nationality_stats[nat] = nationality_stats.get(nat, 0) + 1
        
        for nat, count in sorted(nationality_stats.items()):
            print(f"   {nat}: {count} موظف")
        
        print("\n✅ تم الانتهاء من التحديث!")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
