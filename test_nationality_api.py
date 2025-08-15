#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nationalities import get_nationality_name, get_all_nationalities

def test_nationality_functions():
    """اختبار دوال الجنسيات"""
    
    print("=== اختبار دوال الجنسيات ===")
    
    # اختبار البحث عن جنسيات محددة
    test_codes = ['SY', 'EG', 'SA', 'JO', 'LB', 'US', 'GB', 'DE', 'FR']
    
    print("\n🔍 اختبار البحث عن أسماء الجنسيات:")
    for code in test_codes:
        name_en = get_nationality_name(code, 'en')
        name_ar = get_nationality_name(code, 'ar')
        print(f"  {code}: {name_en} / {name_ar}")
    
    # اختبار الحصول على جميع الجنسيات
    print("\n📋 جميع الجنسيات المتاحة:")
    all_nationalities = get_all_nationalities()
    
    for nationality in all_nationalities[:10]:  # أول 10 فقط للاختبار
        print(f"  {nationality['code']}: {nationality['name_en']} / {nationality['name_ar']}")
    
    print(f"\n📊 إجمالي عدد الجنسيات: {len(all_nationalities)}")
    
    # اختبار كود غير موجود
    print(f"\n❓ اختبار كود غير موجود (XX): {get_nationality_name('XX', 'en')}")

if __name__ == '__main__':
    test_nationality_functions()
