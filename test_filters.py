#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for debugging filter issues
"""

import os
from pymongo import MongoClient
from datetime import datetime, timedelta

# قراءة URI من المتغيرات البيئية أو استخدام القيمة الافتراضية
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://yamantest:yaman123@cluster0.v9cqt.mongodb.net/employees_db?retryWrites=true&w=majority')

def test_filters():
    """اختبار فلاتر الإقامة والهوية الإماراتية"""
    try:
        # الاتصال بقاعدة البيانات
        client = MongoClient(MONGO_URI)
        db = client['employees_db']
        
        print("🔍 اختبار فلاتر الإقامة والهوية الإماراتية")
        print("=" * 60)
        
        # عدد الموظفين الإجمالي
        total_employees = db.employees.count_documents({})
        print(f"📊 إجمالي الموظفين: {total_employees}")
        
        # اختبار فلتر الهوية الإماراتية - مفقودة
        emirates_missing_filter = {
            '$or': [
                {'emirates_id': {'$exists': False}}, 
                {'emirates_id': None}, 
                {'emirates_id': ''}
            ]
        }
        emirates_missing_count = db.employees.count_documents(emirates_missing_filter)
        print(f"🆔 الهوية الإماراتية مفقودة: {emirates_missing_count}")
        
        # اختبار فلتر الهوية الإماراتية - موجودة
        emirates_exists_filter = {
            'emirates_id': {'$exists': True, '$ne': None, '$ne': ''}
        }
        emirates_exists_count = db.employees.count_documents(emirates_exists_filter)
        print(f"🆔 الهوية الإماراتية موجودة: {emirates_exists_count}")
        
        # اختبار فلتر الإقامة - مفقودة
        residence_missing_filter = {
            '$or': [
                {'residence_no': {'$exists': False}}, 
                {'residence_no': None}, 
                {'residence_no': ''}
            ]
        }
        residence_missing_count = db.employees.count_documents(residence_missing_filter)
        print(f"🏠 الإقامة مفقودة: {residence_missing_count}")
        
        # اختبار فلتر الإقامة - موجودة
        residence_exists_filter = {
            'residence_no': {'$exists': True, '$ne': None, '$ne': ''}
        }
        residence_exists_count = db.employees.count_documents(residence_exists_filter)
        print(f"🏠 الإقامة موجودة: {residence_exists_count}")
        
        # أمثلة من البيانات
        print("\n📋 عينة من البيانات:")
        sample = list(db.employees.find({}, {
            'staff_no': 1, 
            'staff_name': 1,
            'emirates_id': 1,
            'residence_no': 1
        }).limit(5))
        
        for emp in sample:
            print(f"  {emp.get('staff_no', 'N/A')}: {emp.get('staff_name', 'N/A')}")
            print(f"    - الهوية: {emp.get('emirates_id', 'غير متوفر')}")
            print(f"    - الإقامة: {emp.get('residence_no', 'غير متوفر')}")
        
        # اختبار query مركب
        print("\n🔬 اختبار query مركب (هوية مفقودة):")
        complex_filter = {
            '$and': [
                {'$or': [
                    {'emirates_id': {'$exists': False}}, 
                    {'emirates_id': None}, 
                    {'emirates_id': ''}
                ]}
            ]
        }
        complex_count = db.employees.count_documents(complex_filter)
        print(f"نتيجة الـ query المركب: {complex_count}")
        
        client.close()
        print("\n✅ انتهى الاختبار")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")

if __name__ == "__main__":
    test_filters()
