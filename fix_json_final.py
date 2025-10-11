#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

def fix_staff_numbers_in_json():
    """
    إصلاح أرقام الموظفين التي تبدأ بصفر في JSON
    """
    input_file = r"c:\Users\yaman_alne0q1\OneDrive\Desktop\3MO_A7A1\employees_raw.json"
    output_file = r"c:\Users\yaman_alne0q1\OneDrive\Desktop\3MO_A7A1\employees_fixed.json"
    
    print("🔧 إصلاح أرقام الموظفين في JSON...")
    
    try:
        # قراءة الملف كنص
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 حجم الملف: {len(content)} حرف")
        
        # إصلاح أرقام الموظفين التي تبدأ بصفر
        # البحث عن "staff_no": 0123456 وتحويلها إلى "staff_no": "0123456"
        content = re.sub(r'"staff_no":\s*(\d+)', r'"staff_no": "\1"', content)
        
        # إصلاح job_code أيضاً ليكون string
        content = re.sub(r'"job_code":\s*(\d+)', r'"job_code": "\1"', content)
        
        # إزالة الفاصلة الأخيرة قبل إغلاق المصفوفة
        content = re.sub(r',\s*]', ']', content)
        
        # إزالة الفواصل الزائدة قبل إغلاق الكائنات
        content = re.sub(r',\s*}', '}', content)
        
        # التأكد من وجود content
        content = content.strip()
        
        print("🔍 محاولة تحليل JSON المصحح...")
        
        # محاولة تحليل JSON
        data = json.loads(content)
        print(f"✅ تم تحليل JSON بنجاح - {len(data)} موظف")
        
        # حفظ النسخة المصححة
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ الملف المصحح: {output_file}")
        print(f"📊 عدد الموظفين: {len(data)}")
        
        # عرض عينة من البيانات
        if len(data) > 0:
            print(f"\n📋 عينة من البيانات:")
            sample = data[0]
            for key, value in sample.items():
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_staff_numbers_in_json()
    if success:
        print("🎉 تم إصلاح الملف بنجاح!")
    else:
        print("💥 فشل في إصلاح الملف!")
