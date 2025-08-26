#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import os
import sys
from datetime import datetime

# إضافة مسار التطبيق
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def add_new_fields_to_employees():
    """
    إضافة الحقول الجديدة لجميع الموظفين في قاعدة البيانات
    """
    print("🔧 إضافة الحقول الجديدة للموظفين...")
    print("=" * 50)
    
    try:
        # الاتصال بقاعدة البيانات (نفس الرابط المستخدم في app.py)
        mongodb_uri = 'mongodb+srv://yamanxl9:SgIhE4u0FbzRhbyp@cluster0.lqokm.mongodb.net/employee_management?retryWrites=true&w=majority&appName=Cluster0'
        client = MongoClient(mongodb_uri)
        db = client.employee_management
        employees_collection = db.employees
        
        print("✅ تم الاتصال بقاعدة البيانات")
        
        # الحقول الجديدة
        new_fields = {
            'emirates_id': None,              # رقم الهوية الإماراتي
            'emirates_id_expiry': None,       # تاريخ انتهاء الهوية
            'residence_no': None,             # رقم الإقامة
            'residence_issue_date': None,     # تاريخ إصدار الإقامة
            'residence_expiry_date': None     # تاريخ انتهاء الإقامة
        }
        
        print(f"📋 الحقول الجديدة: {list(new_fields.keys())}")
        
        # تحديث جميع الوثائق التي لا تحتوي على هذه الحقول
        result = employees_collection.update_many(
            {},  # تحديث جميع الوثائق
            {'$set': new_fields}
        )
        
        print(f"✅ تم تحديث {result.modified_count} موظف")
        
        # التحقق من العدد الإجمالي
        total_employees = employees_collection.count_documents({})
        print(f"📊 إجمالي عدد الموظفين: {total_employees}")
        
        # عرض عينة من الموظف الأول مع الحقول الجديدة
        sample_employee = employees_collection.find_one({})
        if sample_employee:
            print(f"\n📋 عينة من الموظف (أول موظف):")
            print(f"  الاسم: {sample_employee.get('staff_name', 'غير محدد')}")
            print(f"  رقم الموظف: {sample_employee.get('staff_no', 'غير محدد')}")
            print(f"  رقم الهوية الإماراتي: {sample_employee.get('emirates_id', 'غير محدد')}")
            print(f"  تاريخ انتهاء الهوية: {sample_employee.get('emirates_id_expiry', 'غير محدد')}")
            print(f"  رقم الإقامة: {sample_employee.get('residence_no', 'غير محدد')}")
            print(f"  تاريخ إصدار الإقامة: {sample_employee.get('residence_issue_date', 'غير محدد')}")
            print(f"  تاريخ انتهاء الإقامة: {sample_employee.get('residence_expiry_date', 'غير محدد')}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إضافة الحقول: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = add_new_fields_to_employees()
    if success:
        print("\n🎉 تم إضافة الحقول الجديدة بنجاح!")
        print("يمكنك الآن استخدام هذه الحقول في النظام:")
        print("• رقم الهوية الإماراتي")
        print("• تاريخ انتهاء الهوية") 
        print("• رقم الإقامة")
        print("• تاريخ إصدار الإقامة")
        print("• تاريخ انتهاء الإقامة")
    else:
        print("\n💥 فشل في إضافة الحقول!")
