#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريپت تحديث الجنسيات باستخدام نفس إعدادات التطبيق
"""

# استيراد المكتبات المطلوبة
import sys
import os

# إضافة مجلد المشروع للمسار
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد التطبيق والإعدادات
from app import app, mongo
from nationalities import NATIONALITIES

def update_nationalities():
    """تحديث الجنسيات في قاعدة البيانات"""
    print("🚀 بدء تحديث أسماء الجنسيات...")
    
    with app.app_context():
        try:
            # جلب جميع الموظفين
            employees = list(mongo.db.employees.find({}))
            print(f"📊 عدد الموظفين في قاعدة البيانات: {len(employees)}")
            
            if len(employees) == 0:
                print("❌ لا توجد بيانات موظفين!")
                return False
            
            # عرض عينة من البيانات الحالية
            print("\n📝 عينة من البيانات الحالية:")
            for i, emp in enumerate(employees[:3]):
                print(f"   {i+1}. {emp.get('staff_name', 'غير محدد')} - الجنسية: {emp.get('nationality_code', 'غير محدد')}")
            
            # التأكيد من المستخدم
            print(f"\n⚠️  سيتم تحديث {len(employees)} موظف")
            confirm = input("هل تريد المتابعة؟ (y/n): ").lower()
            
            if confirm not in ['y', 'yes', 'نعم']:
                print("❌ تم إلغاء التحديث.")
                return False
            
            # بدء التحديث
            updated_count = 0
            errors_count = 0
            
            for employee in employees:
                try:
                    current_nationality = employee.get('nationality_code', '')
                    
                    if current_nationality and current_nationality in NATIONALITIES:
                        # الحصول على الأسماء الكاملة
                        nationality_ar = NATIONALITIES[current_nationality]['ar']
                        nationality_en = NATIONALITIES[current_nationality]['en']
                        
                        # تحديث البيانات
                        result = mongo.db.employees.update_one(
                            {'_id': employee['_id']},
                            {
                                '$set': {
                                    'nationality_code': nationality_ar,  # تحويل إلى الاسم العربي الكامل
                                    'nationality_code_old': current_nationality,  # حفظ الرمز القديم
                                    'nationality_ar': nationality_ar,
                                    'nationality_en': nationality_en
                                }
                            }
                        )
                        
                        if result.modified_count > 0:
                            updated_count += 1
                            staff_name = employee.get('staff_name', 'غير محدد')
                            print(f"✅ {staff_name}: {current_nationality} → {nationality_ar}")
                        
                    elif current_nationality:
                        print(f"⚠️  جنسية غير معروفة: {current_nationality} للموظف: {employee.get('staff_name', 'غير محدد')}")
                        
                except Exception as e:
                    errors_count += 1
                    print(f"❌ خطأ في تحديث الموظف {employee.get('staff_name', 'غير محدد')}: {e}")
            
            print(f"\n🎉 النتائج:")
            print(f"   ✅ تم تحديث: {updated_count} موظف")
            print(f"   ❌ أخطاء: {errors_count}")
            
            # عرض الإحصائيات الجديدة
            print(f"\n📊 إحصائيات الجنسيات بعد التحديث:")
            nationality_stats = {}
            
            for emp in mongo.db.employees.find({}):
                nat = emp.get('nationality_code', 'غير محدد')
                nationality_stats[nat] = nationality_stats.get(nat, 0) + 1
            
            for nat, count in sorted(nationality_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   {nat}: {count} موظف")
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ عام في التحديث: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_search():
    """اختبار البحث بعد التحديث"""
    print(f"\n🔍 اختبار البحث بعد التحديث...")
    
    with app.app_context():
        try:
            # البحث عن الموظفين الأتراك
            turkish_employees = list(mongo.db.employees.find({'nationality_code': 'تركي'}))
            print(f"🇹🇷 عدد الموظفين الأتراك: {len(turkish_employees)}")
            
            for emp in turkish_employees:
                print(f"   - {emp.get('staff_name', 'غير محدد')} (جنسية: {emp.get('nationality_code')})")
            
            # البحث عن الموظفين الهنود
            indian_employees = list(mongo.db.employees.find({'nationality_code': 'هندي'}))
            print(f"🇮🇳 عدد الموظفين الهنود: {len(indian_employees)}")
            
        except Exception as e:
            print(f"❌ خطأ في الاختبار: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 سكريپت تحديث أسماء الجنسيات إلى الأسماء الكاملة")
    print("=" * 60)
    
    # تنفيذ التحديث
    if update_nationalities():
        # اختبار البحث
        test_search()
        
        print(f"\n✅ تم الانتهاء من التحديث بنجاح!")
        print(f"📝 يمكنك الآن البحث باستخدام:")
        print(f"   - 'تركي' بدلاً من 'TR'")
        print(f"   - 'هندي' بدلاً من 'IN'")
        print(f"   - 'فلبيني' بدلاً من 'PH'")
        
    else:
        print(f"\n❌ فشل في التحديث!")
        sys.exit(1)
