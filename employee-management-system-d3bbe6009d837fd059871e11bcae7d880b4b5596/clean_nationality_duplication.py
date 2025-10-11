#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت تنظيف التكرار في بيانات الجنسيات
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, mongo
from nationalities import NATIONALITIES

def clean_nationality_duplication():
    """تنظيف التكرار في بيانات الجنسيات"""
    print("🧹 بدء تنظيف التكرار في بيانات الجنسيات...")
    
    with app.app_context():
        try:
            employees = list(mongo.db.employees.find({}))
            print(f"📊 عدد الموظفين: {len(employees)}")
            
            cleaned_count = 0
            
            for employee in employees:
                nationality_code = employee.get('nationality_code', '')
                nationality_ar = employee.get('nationality_ar', '')
                nationality_en = employee.get('nationality_en', '')
                nationality_code_old = employee.get('nationality_code_old', '')
                
                print(f"\n🔍 الموظف: {employee.get('staff_name', 'غير محدد')}")
                print(f"   nationality_code: {nationality_code}")
                print(f"   nationality_ar: {nationality_ar}")
                print(f"   nationality_en: {nationality_en}")
                print(f"   nationality_code_old: {nationality_code_old}")
                
                # إذا كان nationality_code هو اسم كامل (مثل "تركي")
                if nationality_code and nationality_code not in NATIONALITIES:
                    # البحث عن الرمز الأصلي
                    original_code = None
                    for code, names in NATIONALITIES.items():
                        if nationality_code == names['ar'] or nationality_code == names['en']:
                            original_code = code
                            break
                    
                    if original_code:
                        # تنظيف البيانات
                        update_data = {
                            'nationality_code': original_code,  # إرجاع الرمز الأصلي
                            'nationality_display': nationality_code  # حفظ الاسم للعرض
                        }
                        
                        # إزالة الحقول المكررة
                        unset_data = {
                            'nationality_ar': "",
                            'nationality_en': "",
                            'nationality_code_old': ""
                        }
                        
                        result = mongo.db.employees.update_one(
                            {'_id': employee['_id']},
                            {
                                '$set': update_data,
                                '$unset': unset_data
                            }
                        )
                        
                        if result.modified_count > 0:
                            cleaned_count += 1
                            print(f"   ✅ تم التنظيف: {nationality_code} → {original_code}")
                
                elif nationality_code in NATIONALITIES:
                    # إذا كان nationality_code رمز صحيح، نظف الحقول الإضافية
                    update_data = {
                        'nationality_display': NATIONALITIES[nationality_code]['ar']
                    }
                    
                    unset_data = {
                        'nationality_ar': "",
                        'nationality_en': "",
                        'nationality_code_old': ""
                    }
                    
                    result = mongo.db.employees.update_one(
                        {'_id': employee['_id']},
                        {
                            '$set': update_data,
                            '$unset': unset_data
                        }
                    )
                    
                    if result.modified_count > 0:
                        cleaned_count += 1
                        print(f"   ✅ تم تنظيف الحقول الإضافية")
            
            print(f"\n🎉 تم تنظيف {cleaned_count} موظف")
            
            # عرض النتائج بعد التنظيف
            print(f"\n📊 إحصائيات الجنسيات بعد التنظيف:")
            nationality_stats = {}
            for emp in mongo.db.employees.find({}):
                nat_display = emp.get('nationality_display', emp.get('nationality_code', 'غير محدد'))
                nationality_stats[nat_display] = nationality_stats.get(nat_display, 0) + 1
            
            for nat, count in sorted(nationality_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   {nat}: {count} موظف")
                
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("🧹 سكريپت تنظيف التكرار في بيانات الجنسيات")
    print("=" * 60)
    
    confirm = input("⚠️  هل تريد المتابعة مع التنظيف؟ (y/n): ").lower()
    if confirm in ['y', 'yes', 'نعم']:
        clean_nationality_duplication()
    else:
        print("❌ تم إلغاء التنظيف.")
