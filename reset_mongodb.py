#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سكريبت لإعادة تعيين قاعدة البيانات MongoDB
Reset MongoDB Database Script
"""

import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('reset_mongodb.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def get_database_connection():
    """الاتصال بقاعدة البيانات"""
    try:
        # قراءة معلومات الاتصال من متغيرات البيئة أو استخدام القيم الافتراضية
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        database_name = os.getenv('MONGODB_DB', 'employees_db')
        
        logger.info(f"🔗 محاولة الاتصال بقاعدة البيانات: {database_name}")
        
        # الاتصال بقاعدة البيانات
        client = MongoClient(mongodb_uri)
        
        # اختبار الاتصال
        client.admin.command('ping')
        
        db = client[database_name]
        logger.info(f"✅ نجح الاتصال بقاعدة البيانات: {database_name}")
        
        return client, db
        
    except PyMongoError as e:
        logger.error(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
        return None, None
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
        return None, None

def reset_database(db):
    """إعادة تعيين قاعدة البيانات بالكامل"""
    try:
        logger.info("🗑️ بدء إعادة تعيين قاعدة البيانات...")
        
        # الحصول على قائمة بجميع المجموعات
        collections = db.list_collection_names()
        
        if not collections:
            logger.info("📋 قاعدة البيانات فارغة بالفعل")
            return True
        
        logger.info(f"📋 المجموعات الموجودة: {collections}")
        
        # حذف جميع المجموعات
        for collection_name in collections:
            logger.info(f"🗑️ حذف مجموعة: {collection_name}")
            db.drop_collection(collection_name)
        
        logger.info("✅ تم حذف جميع المجموعات بنجاح")
        return True
        
    except PyMongoError as e:
        logger.error(f"❌ خطأ في إعادة تعيين قاعدة البيانات: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء إعادة تعيين قاعدة البيانات MongoDB...")
    
    # الاتصال بقاعدة البيانات
    client, db = get_database_connection()
    if db is None:
        return False
    
    try:
        # إعادة تعيين قاعدة البيانات
        if not reset_database(db):
            return False
        
        logger.info("🎉 تم إعادة تعيين قاعدة البيانات بنجاح!")
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في العملية الرئيسية: {e}")
        return False
    finally:
        # إغلاق الاتصال
        if client:
            client.close()
            logger.info("🔐 تم إغلاق الاتصال بقاعدة البيانات")

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ تم إعادة تعيين قاعدة البيانات بنجاح!")
        print("💡 يمكنك الآن تشغيل setup_mongodb.py لإعداد قاعدة البيانات من جديد")
    else:
        print("\n❌ فشل في إعادة تعيين قاعدة البيانات!")
        exit(1)
