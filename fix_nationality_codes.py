#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح رموز الجنسيات - تحويل الأسماء إلى رموز
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from nationalities import NATIONALITIES

# تحميل متغيرات البيئة
load_dotenv()

# الاتصال بقاعدة البيانات
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
client = MongoClient(MONGODB_URI)
db = client.get_database()

# قاموس تحويل أسماء الجنسيات إلى رموز
NATIONALITY_NAME_TO_CODE = {
    # العربية
    'سوري': 'SY',
    'سوريا': 'SY',
    'تركي': 'TR',
    'تركيا': 'TR',
    'هندي': 'IN',
    'الهند': 'IN',
    'باكستاني': 'PK',
    'باكستان': 'PK',
    'إيراني': 'IR',
    'إيران': 'IR',
    'فلبيني': 'PH',
    'الفلبين': 'PH',
    'مصري': 'EG',
    'مصر': 'EG',
    'أردني': 'JO',
    'الأردن': 'JO',
    'لبناني': 'LB',
    'لبنان': 'LB',
    'عراقي': 'IQ',
    'العراق': 'IQ',
    'سعودي': 'SA',
    'السعودية': 'SA',
    'إماراتي': 'AE',
    'الإمارات': 'AE',
    'كويتي': 'KW',
    'الكويت': 'KW',
    'قطري': 'QA',
    'قطر': 'QA',
    'بحريني': 'BH',
    'البحرين': 'BH',
    'عماني': 'OM',
    'عمان': 'OM',
    'يمني': 'YE',
    'اليمن': 'YE',
    'فلسطيني': 'PS',
    'فلسطين': 'PS',
    'بنغلاديشي': 'BD',
    'بنغلاديش': 'BD',
    'سريلانكي': 'LK',
    'سريلانكا': 'LK',
    'نيبالي': 'NP',
    'نيبال': 'NP',
    'أفغاني': 'AF',
    'أفغانستان': 'AF',
    
    # الإنجليزية
    'Syrian': 'SY',
    'Syria': 'SY',
    'Turkish': 'TR',
    'Turkey': 'TR',
    'Indian': 'IN',
    'India': 'IN',
    'Pakistani': 'PK',
    'Pakistan': 'PK',
    'Iranian': 'IR',
    'Iran': 'IR',
    'Filipino': 'PH',
    'Philippines': 'PH',
    'Egyptian': 'EG',
    'Egypt': 'EG',
    'Jordanian': 'JO',
    'Jordan': 'JO',
    'Lebanese': 'LB',
    'Lebanon': 'LB',
    'Iraqi': 'IQ',
    'Iraq': 'IQ',
    'Saudi': 'SA',
    'Emirati': 'AE',
    'Kuwaiti': 'KW',
    'Qatari': 'QA',
    'Bahraini': 'BH',
    'Omani': 'OM',
    'Yemeni': 'YE',
    'Palestinian': 'PS',
    'Bangladeshi': 'BD',
    'Sri Lankan': 'LK',
    'Nepalese': 'NP',
    'Afghan': 'AF'
}

def fix_nationality_codes():
    """إصلاح رموز الجنسيات"""
    print("🔧 إصلاح رموز الجنسيات...")
    
    employees = list(db.employees.find())
    fixed_count = 0
    unknown_nationalities = set()
    
    for emp in employees:
        nationality = emp.get('nationality_code', '').strip()
        
        if nationality and len(nationality) > 2:  # ليس كود - اسم جنسية
            # البحث عن الكود المناسب
            code = NATIONALITY_NAME_TO_CODE.get(nationality)
            
            if code:
                # تحديث البيانات
                nationality_info = NATIONALITIES[code]
                
                updates = {
                    'nationality_code': code,
                    'nationality_en': nationality_info['en'],
                    'nationality_ar': nationality_info['ar']
                }
                
                db.employees.update_one({'_id': emp['_id']}, {'$set': updates})
                fixed_count += 1
                print(f"   ✅ محدث: {emp.get('staff_no', 'N/A')} - {nationality} → {code} ({nationality_info['ar']})")
            else:
                unknown_nationalities.add(nationality)
                print(f"   ⚠️ جنسية غير معروفة: {nationality} للموظف {emp.get('staff_no', 'N/A')}")
    
    print(f"\n✅ تم إصلاح {fixed_count} رمز جنسية")
    
    if unknown_nationalities:
        print(f"\n❌ جنسيات غير معروفة ({len(unknown_nationalities)}):")
        for nat in sorted(unknown_nationalities):
            print(f"   - {nat}")
    
    return fixed_count, unknown_nationalities

def add_missing_nationalities_to_dict(unknown_nationalities):
    """إضافة الجنسيات المفقودة إلى القاموس"""
    if not unknown_nationalities:
        return
    
    print(f"\n📝 اقتراحات لإضافة الجنسيات المفقودة:")
    
    # اقتراحات محتملة
    suggestions = {
        'سوريا': 'SY',
        'تركيا': 'TR',
        'الهند': 'IN',
        'باكستان': 'PK',
        'إيران': 'IR',
        'الفلبين': 'PH'
    }
    
    for nationality in unknown_nationalities:
        if nationality in suggestions:
            code = suggestions[nationality]
            if code in NATIONALITIES:
                nationality_info = NATIONALITIES[code]
                print(f"   '{nationality}': '{code}',  # {nationality_info['ar']} - {nationality_info['en']}")

def verify_all_employees():
    """التحقق من جميع الموظفين"""
    print("\n📊 التحقق النهائي من جميع الموظفين...")
    
    employees = list(db.employees.find())
    valid_count = 0
    issues = []
    
    for emp in employees:
        nationality_code = emp.get('nationality_code', '')
        
        if nationality_code and len(nationality_code) == 2 and nationality_code in NATIONALITIES:
            valid_count += 1
        else:
            issues.append({
                'staff_no': emp.get('staff_no', 'N/A'),
                'nationality_code': nationality_code
            })
    
    print(f"   ✅ موظفين بجنسيات صحيحة: {valid_count}")
    print(f"   ❌ موظفين بمشاكل: {len(issues)}")
    
    if issues:
        print("\n   مشاكل موجودة:")
        for issue in issues[:10]:  # أول 10 فقط
            print(f"     - {issue['staff_no']}: {issue['nationality_code']}")
        if len(issues) > 10:
            print(f"     ... و {len(issues) - 10} أخرى")

def main():
    """الدالة الرئيسية"""
    print("🔧 إصلاح رموز الجنسيات في قاعدة البيانات")
    print("=" * 60)
    
    # إصلاح رموز الجنسيات
    fixed_count, unknown_nationalities = fix_nationality_codes()
    
    # اقتراح إضافات للقاموس
    add_missing_nationalities_to_dict(unknown_nationalities)
    
    # التحقق النهائي
    verify_all_employees()
    
    print("\n" + "=" * 60)
    print("✅ تم الانتهاء من إصلاح رموز الجنسيات!")

if __name__ == "__main__":
    main()
