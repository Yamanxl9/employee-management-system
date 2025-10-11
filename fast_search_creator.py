#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحسينات فورية للأداء - سكريبت مؤقت
"""

from app import app, mongo
from datetime import datetime, timedelta, timezone
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

def create_fast_search_endpoint():
    """إنشاء endpoint محسن للبحث"""
    
    @app.route('/api/fast-search')
    def fast_search():
        """بحث محسن وسريع"""
        try:
            import time
            start_time = time.time()
            
            # جلب المعايير
            query = request.args.get('query', '').strip()
            nationality = request.args.get('nationality', '')
            company = request.args.get('company', '')
            job = request.args.get('job', '')
            department = request.args.get('department', '')
            passport_status = request.args.get('passport_status', '')
            card_status = request.args.get('card_status', '')
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
            
            # بناء استعلام محسن
            filter_query = {}
            
            # البحث النصي السريع
            if query:
                filter_query['$text'] = {'$search': query}
            
            # فلاتر مباشرة
            if nationality:
                filter_query['nationality_code'] = nationality
            if company:
                filter_query['company_code'] = company
            if job:
                try:
                    filter_query['job_code'] = int(job)
                except:
                    pass
            if department:
                filter_query['department_code'] = department
            
            # فلاتر الحالة المحسنة
            if passport_status == 'missing':
                filter_query['$or'] = [
                    {'pass_no': {'$exists': False}},
                    {'pass_no': None},
                    {'pass_no': ''}
                ]
            elif passport_status == 'available':
                filter_query['pass_no'] = {'$exists': True, '$ne': None, '$ne': ''}
            
            current_date = datetime.now()
            if card_status == 'missing':
                filter_query['$or'] = [
                    {'card_no': {'$exists': False}},
                    {'card_no': None},
                    {'card_no': ''}
                ]
            elif card_status == 'expired':
                filter_query.update({
                    'card_no': {'$exists': True, '$ne': None, '$ne': ''},
                    'card_expiry_date': {'$lt': current_date}
                })
            
            # حساب pagination
            skip = (page - 1) * per_page
            
            # استعلام محسن
            projection = {
                'staff_no': 1, 'staff_name': 1, 'staff_name_ara': 1,
                'nationality_code': 1, 'company_code': 1, 'job_code': 1,
                'department_code': 1, 'pass_no': 1, 'card_no': 1,
                'card_expiry_date': 1
            }
            
            employees = list(mongo.db.employees.find(
                filter_query, projection
            ).skip(skip).limit(per_page))
            
            total = mongo.db.employees.count_documents(filter_query)
            
            # معالجة سريعة للنتائج
            results = []
            for emp in employees:
                emp_data = {
                    'staff_no': emp.get('staff_no'),
                    'name': emp.get('staff_name_ara') or emp.get('staff_name', ''),
                    'nationality': emp.get('nationality_code', ''),
                    'company': emp.get('company_code', ''),
                    'job': emp.get('job_code', ''),
                    'department': emp.get('department_code', ''),
                    'passport': '✅' if emp.get('pass_no') else '❌',
                    'card': '🟢' if emp.get('card_no') else '❌'
                }
                
                # تحديد حالة البطاقة بسرعة
                if emp.get('card_no') and emp.get('card_expiry_date'):
                    try:
                        expiry = emp['card_expiry_date']
                        if isinstance(expiry, str):
                            expiry = datetime.fromisoformat(expiry.replace('Z', '+00:00'))
                        if expiry.tzinfo is None:
                            expiry = expiry.replace(tzinfo=timezone.utc)
                        
                        now = datetime.now(timezone.utc)
                        if expiry < now:
                            emp_data['card'] = '🔴'
                        elif expiry < now + timedelta(days=90):
                            emp_data['card'] = '🟡'
                        else:
                            emp_data['card'] = '🟢'
                    except:
                        emp_data['card'] = '⚠️'
                
                results.append(emp_data)
            
            pages = (total + per_page - 1) // per_page
            response_time = time.time() - start_time
            
            return jsonify({
                'employees': results,
                'total': total,
                'pages': pages,
                'current_page': page,
                'has_next': page < pages,
                'has_prev': page > 1,
                'response_time': f"{response_time:.3f}s"
            })
            
        except Exception as e:
            logger.error(f"Error in fast search: {e}")
            return jsonify({'error': str(e)}), 500

# تشغيل الدالة لإنشاء endpoint
if __name__ == "__main__":
    with app.app_context():
        create_fast_search_endpoint()
        print("✅ تم إنشاء endpoint البحث السريع!")
