#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحسينات أداء التطبيق
"""

from app import app, mongo
import logging

# إعداد التخزين المؤقت للبيانات الثابتة
from functools import lru_cache
import time

# تخزين مؤقت للبيانات الثابتة
_cache = {}
_cache_timeout = 300  # 5 دقائق

def get_cached_data(key, fetch_function):
    """جلب البيانات مع التخزين المؤقت"""
    current_time = time.time()
    
    if key in _cache:
        data, timestamp = _cache[key]
        if current_time - timestamp < _cache_timeout:
            return data
    
    # جلب البيانات الجديدة
    data = fetch_function()
    _cache[key] = (data, current_time)
    return data

@lru_cache(maxsize=100)
def get_nationality_name(code):
    """جلب اسم الجنسية بالتخزين المؤقت"""
    from nationalities import NATIONALITIES
    return NATIONALITIES.get(code, code)

# تحسين استعلامات قاعدة البيانات
def create_optimized_indexes():
    """إنشاء فهارس محسنة لتحسين الأداء"""
    try:
        # فهارس البحث السريع
        mongo.db.employees.create_index([
            ("staff_name", "text"),
            ("staff_name_ara", "text"),
            ("staff_no", "text"),
            ("pass_no", "text"),
            ("card_no", "text")
        ])
        
        # فهارس للفلاتر
        mongo.db.employees.create_index("nationality_code")
        mongo.db.employees.create_index("company_code")
        mongo.db.employees.create_index("job_code")
        mongo.db.employees.create_index("department_code")
        mongo.db.employees.create_index("card_expiry_date")
        
        print("✅ تم إنشاء الفهارس المحسنة")
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الفهارس: {e}")

# تحسين الذاكرة
import gc

def optimize_memory():
    """تحسين استخدام الذاكرة"""
    gc.collect()

if __name__ == "__main__":
    print("🚀 تشغيل تحسينات الأداء...")
    with app.app_context():
        create_optimized_indexes()
        optimize_memory()
    print("✅ تم تطبيق جميع التحسينات!")
