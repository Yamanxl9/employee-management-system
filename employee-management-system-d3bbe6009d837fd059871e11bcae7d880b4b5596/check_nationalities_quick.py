#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص سريع لرموز الجنسيات في قاعدة البيانات
"""

from app import mongo, NATIONALITIES

if __name__ == "__main__":
    try:
        if mongo:
            print("✅ MongoDB متصل")
            
            # جلب عينة من رموز الجنسيات
            codes = mongo.db.employees.distinct('nationality_code')
            print(f"\n📊 إجمالي رموز الجنسيات: {len(codes)}")
            print("\n🔍 عينة من رموز الجنسيات في قاعدة البيانات:")
            for i, code in enumerate(sorted(codes)[:15]):
                if code:
                    print(f"  {i+1:2}. '{code}'")
            
            print(f"\n📚 عدد الجنسيات في قاموس NATIONALITIES: {len(NATIONALITIES)}")
            print("\n🔍 عينة من قاموس NATIONALITIES:")
            for i, (code, names) in enumerate(list(NATIONALITIES.items())[:10]):
                print(f"  {i+1:2}. '{code}' -> EN: '{names['en']}', AR: '{names['ar']}'")
            
            # تحليل التطابق
            db_codes = set(codes)
            dict_codes = set(NATIONALITIES.keys())
            
            print(f"\n🔗 التطابق:")
            print(f"  - موجود في كلاهما: {len(db_codes & dict_codes)}")
            print(f"  - موجود في DB فقط: {len(db_codes - dict_codes)}")
            print(f"  - موجود في DICT فقط: {len(dict_codes - db_codes)}")
            
            if db_codes - dict_codes:
                print("\n⚠️  رموز موجودة في DB لكن ليس في DICT:")
                for code in sorted(db_codes - dict_codes)[:10]:
                    if code:
                        print(f"    '{code}'")
                        
        else:
            print("❌ MongoDB غير متصل")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
