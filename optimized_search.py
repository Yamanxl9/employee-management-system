#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نسخة محسنة لدالة البحث
Optimized Search Function
"""

# API للبحث عن الموظفين - محسن للأداء العالي
@app.route('/api/search-optimized')
def search_employees_optimized():
    """
    نسخة محسنة من البحث لتحسين الأداء
    - استخدام فهارس النص للبحث السريع
    - تقليل عدد الاستعلامات
    - تحسين الفلاتر
    """
    import time
    start_time = time.time()
    
    try:
        # جلب المعايير
        query = request.args.get('query', '').strip()
        nationality = request.args.get('nationality', '')
        company = request.args.get('company', '')
        job = request.args.get('job', '')
        department = request.args.get('department', '')
        passport_status = request.args.get('passport_status', '')
        card_status = request.args.get('card_status', '')
        emirates_id_status = request.args.get('emirates_id_status', '')
        residence_status = request.args.get('residence_status', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # بناء استعلام محسن
        filter_query = {}
        
        # البحث النصي السريع باستخدام فهرس النص
        if query:
            filter_query['$text'] = {'$search': query}
        
        # فلاتر مباشرة وسريعة
        if nationality:
            filter_query['nationality_code'] = nationality
        
        if company:
            filter_query['company_code'] = company
        
        if job:
            try:
                filter_query['job_code'] = int(job)
            except (ValueError, TypeError):
                pass
        
        if department:
            filter_query['department_code'] = department
        
        # فلاتر حالة الجواز المحسنة
        if passport_status == 'missing':
            filter_query['$or'] = [
                {'pass_no': {'$exists': False}},
                {'pass_no': None},
                {'pass_no': ''}
            ]
        elif passport_status == 'available':
            filter_query['pass_no'] = {'$exists': True, '$ne': None, '$ne': ''}
        
        # فلاتر حالة البطاقة المحسنة
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
        elif card_status == 'expiring_soon':
            future_date = current_date + timedelta(days=90)
            filter_query.update({
                'card_no': {'$exists': True, '$ne': None, '$ne': ''},
                'card_expiry_date': {'$gte': current_date, '$lt': future_date}
            })
        elif card_status == 'valid':
            future_date = current_date + timedelta(days=90)
            filter_query.update({
                'card_no': {'$exists': True, '$ne': None, '$ne': ''},
                'card_expiry_date': {'$gte': future_date}
            })
        
        # حساب pagination
        skip = (page - 1) * per_page
        
        # استعلام محسن مع فهارس
        cursor = mongo.db.employees.find(
            filter_query,
            {
                'staff_no': 1,
                'staff_name': 1,
                'staff_name_ara': 1,
                'nationality_code': 1,
                'company_code': 1,
                'job_code': 1,
                'department_code': 1,
                'pass_no': 1,
                'card_no': 1,
                'card_expiry_date': 1,
                'emirates_id': 1,
                'emirates_id_expiry': 1,
                'residence_no': 1,
                'residence_expiry_date': 1
            }
        ).skip(skip).limit(per_page)
        
        employees = list(cursor)
        
        # عد النتائج بطريقة محسنة
        total = mongo.db.employees.count_documents(filter_query)
        
        # معالجة سريعة للنتائج
        results = []
        for emp in employees:
            # معلومات إضافية محسنة
            emp_data = {
                'staff_no': emp.get('staff_no'),
                'staff_name': emp.get('staff_name_ara') or emp.get('staff_name', ''),
                'staff_name_ara': emp.get('staff_name_ara', ''),
                'staff_name_eng': emp.get('staff_name', ''),
                'nationality_code': emp.get('nationality_code', ''),
                'company_code': emp.get('company_code', ''),
                'job_code': emp.get('job_code', ''),
                'department_code': emp.get('department_code', ''),
                'pass_no': emp.get('pass_no', ''),
                'card_no': emp.get('card_no', ''),
                'emirates_id': emp.get('emirates_id', ''),
                'residence_no': emp.get('residence_no', ''),
            }
            
            # حالة الجواز السريعة
            emp_data['passport_status'] = '✅' if emp.get('pass_no') else '❌'
            
            # حالة البطاقة السريعة
            if not emp.get('card_no'):
                emp_data['card_status'] = '❌'
            elif not emp.get('card_expiry_date'):
                emp_data['card_status'] = '⚠️'
            else:
                expiry_date = emp['card_expiry_date']
                if isinstance(expiry_date, str):
                    try:
                        expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
                    except:
                        expiry_date = datetime.now()
                
                if expiry_date.tzinfo is None:
                    expiry_date = expiry_date.replace(tzinfo=timezone.utc)
                
                now = datetime.now(timezone.utc)
                if expiry_date < now:
                    emp_data['card_status'] = '🔴'
                elif expiry_date < now + timedelta(days=90):
                    emp_data['card_status'] = '🟡'
                else:
                    emp_data['card_status'] = '🟢'
            
            # التواريخ المنسقة
            if emp.get('card_expiry_date'):
                emp_data['card_expiry_date'] = emp['card_expiry_date'].strftime('%Y-%m-%d') if isinstance(emp['card_expiry_date'], datetime) else str(emp['card_expiry_date'])
            
            results.append(emp_data)
        
        # حساب عدد الصفحات
        pages = (total + per_page - 1) // per_page
        
        # وقت الاستجابة
        response_time = time.time() - start_time
        
        return jsonify({
            'employees': results,
            'total': total,
            'pages': pages,
            'current_page': page,
            'has_next': page < pages,
            'has_prev': page > 1,
            'per_page': per_page,
            'response_time': f"{response_time:.3f}s"
        })
        
    except Exception as e:
        logger.error(f"Error in optimized search: {str(e)}")
        return jsonify({'error': f'خطأ في البحث: {str(e)}'}), 500
