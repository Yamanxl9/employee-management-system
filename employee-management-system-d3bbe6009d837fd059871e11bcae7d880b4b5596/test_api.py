#!/usr/bin/env python3
"""
اختبار API الإحصائيات
"""
import requests
import json

# الحصول على token
login_data = {
    "username": "admin",
    "password": "admin123"
}

# تسجيل الدخول
try:
    login_response = requests.post('http://127.0.0.1:5000/api/login', json=login_data)
    print("Login response status:", login_response.status_code)
    print("Login response:", login_response.text)
    
    if login_response.status_code == 200:
        token = login_response.json().get('token')
        print("Token received:", token[:20] + "..." if token else "None")
        
        # اختبار API الإحصائيات
        headers = {"Authorization": f"Bearer {token}"}
        stats_response = requests.get('http://127.0.0.1:5000/api/statistics', headers=headers)
        print("\nStatistics response status:", stats_response.status_code)
        print("Statistics response:", stats_response.text)
        
        # اختبار API الفلاتر
        filters_response = requests.get('http://127.0.0.1:5000/api/filters', headers=headers)
        print("\nFilters response status:", filters_response.status_code)
        print("Filters response:", filters_response.text)
        
    else:
        print("Login failed!")
        
except Exception as e:
    print(f"Error: {e}")
