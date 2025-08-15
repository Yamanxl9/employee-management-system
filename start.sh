#!/bin/bash

# إعداد بيئة النشر على Render
echo "🚀 بدء تشغيل نظام إدارة الموظفين..."

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip install -r requirements.txt

# تشغيل التطبيق
echo "▶️ تشغيل التطبيق..."
exec gunicorn app:app --config gunicorn.conf.py
