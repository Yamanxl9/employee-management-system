#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار البحث بالجنسيات الإنجليزية
"""

from nationalities import NATIONALITIES

def test_nationality_search(query):
    """اختبار البحث في الجنسيات"""
    print(f"🔍 البحث عن: '{query}'")
    
    matching_nationality_codes = []
    for code, names in NATIONALITIES.items():
        en_match = query.lower() in names['en'].lower()
        ar_match = query.lower() in names['ar'].lower()
        code_match = query.lower() in code.lower()
        
        if en_match or ar_match or code_match:
            matching_nationality_codes.append(code)
            print(f"   ✅ وجد: {code} - {names['en']} - {names['ar']}")
            print(f"      EN match: {en_match}, AR match: {ar_match}, Code match: {code_match}")
    
    print(f"📊 إجمالي النتائج: {len(matching_nationality_codes)}")
    print(f"الرموز المطابقة: {matching_nationality_codes}")
    return matching_nationality_codes

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 اختبار البحث في الجنسيات")
    print("=" * 60)
    
    # اختبار البحث بالعربية
    print("\n1️⃣ اختبار البحث بالعربية:")
    test_nationality_search("تركي")
    
    # اختبار البحث بالإنجليزية
    print("\n2️⃣ اختبار البحث بالإنجليزية:")
    test_nationality_search("Turkish")
    
    # اختبار البحث بالرمز
    print("\n3️⃣ اختبار البحث بالرمز:")
    test_nationality_search("TR")
    
    # اختبار البحث الجزئي
    print("\n4️⃣ اختبار البحث الجزئي:")
    test_nationality_search("Turk")
    
    print("\n" + "=" * 60)
