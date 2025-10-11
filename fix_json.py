#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

def fix_and_clean_json():
    """
    إصلاح وتنظيف ملف JSON
    """
    input_file = r"c:\Users\yaman_alne0q1\OneDrive\Desktop\3MO_A7A1\employees_raw.json"
    output_file = r"c:\Users\yaman_alne0q1\OneDrive\Desktop\3MO_A7A1\employees_fixed.json"
    
    print("🔧 إصلاح وتنظيف ملف JSON...")
    
    try:
        # قراءة الملف كنص أولاً
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 حجم الملف: {len(content)} حرف")
        
        # إصلاح المشاكل الشائعة في JSON
        # إزالة الفاصلة الأخيرة قبل إغلاق المصفوفة
        content = re.sub(r',\s*]', ']', content)
        
        # إزالة الأسطر الفارغة في البداية
        content = content.strip()
        
        # التأكد من أن الملف يبدأ بـ [
        if not content.startswith('['):
            print("❌ الملف لا يبدأ بمصفوفة صحيحة")
            return False
        
        # محاولة تحليل JSON
        try:
            data = json.loads(content)
            print(f"✅ تم تحليل JSON بنجاح - {len(data)} عنصر")
        except json.JSONDecodeError as e:
            print(f"❌ خطأ في JSON: {e}")
            print(f"📍 السطر {e.lineno}, العمود {e.colno}")
            
            # محاولة إصلاح الخطأ
            lines = content.split('\n')
            if e.lineno <= len(lines):
                problem_line = lines[e.lineno - 1]
                print(f"🔍 السطر المشكل: {problem_line}")
                
                # إصلاح مشاكل شائعة
                if e.msg == "Expecting ',' delimiter":
                    # إضافة فاصلة مفقودة
                    lines[e.lineno - 1] = problem_line.rstrip() + ','
                    content = '\n'.join(lines)
                    
                    # محاولة تحليل مرة أخرى
                    try:
                        data = json.loads(content)
                        print("✅ تم إصلاح الخطأ بنجاح!")
                    except:
                        print("❌ فشل في إصلاح الخطأ تلقائياً")
                        return False
        
        # حفظ النسخة المصححة
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ الملف المصحح: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_and_clean_json()
    if success:
        print("🎉 تم إصلاح الملف بنجاح!")
    else:
        print("💥 فشل في إصلاح الملف!")
