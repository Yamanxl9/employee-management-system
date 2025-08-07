from flask import Flask, render_template, request, jsonify, send_file
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
import pandas as pd
import io
import os
import json
from dotenv import load_dotenv
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# تحميل متغيرات البيئة
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['MONGO_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')

# إعداد MongoDB
mongo = PyMongo(app)

# Helper functions for MongoDB
def serialize_doc(doc):
    """تحويل وثيقة MongoDB إلى قاموس قابل للتسلسل"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    
    # تحويل datetime objects
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, ObjectId):
            doc[key] = str(value)
    
    return doc

def get_employee_status(employee):
    """حساب حالة الجواز والبطاقة للموظف"""
    passport_status = 'available' if employee.get('pass_no') else 'missing'
    passport_text = 'متوفر' if employee.get('pass_no') else 'غير متوفر'
    passport_class = 'success' if employee.get('pass_no') else 'danger'
    
    # حالة البطاقة
    if not employee.get('card_no'):
        card_status, card_text, card_class = 'missing', 'غير متوفرة', 'danger'
    elif not employee.get('card_expiry_date'):
        card_status, card_text, card_class = 'no_expiry', 'بدون تاريخ انتهاء', 'warning'
    else:
        expiry_date = employee['card_expiry_date']
        if isinstance(expiry_date, str):
            expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
        
        today = datetime.now()
        if expiry_date < today:
            card_status, card_text, card_class = 'expired', 'منتهية الصلاحية', 'danger'
        elif expiry_date < today + timedelta(days=90):
            card_status, card_text, card_class = 'expiring_soon', 'تنتهي قريباً', 'warning'
        else:
            card_status, card_text, card_class = 'valid', 'سارية', 'success'
    
    return {
        'passport_status': passport_status,
        'passport_text': passport_text,
        'passport_class': passport_class,
        'card_status': card_status,
        'card_text': card_text,
        'card_class': card_class
    }

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# API للبحث عن الموظفين
@app.route('/api/search')
def search_employees():
    query = request.args.get('query', '').strip()
    nationality = request.args.get('nationality', '')
    company = request.args.get('company', '')
    passport_status = request.args.get('passport_status', '')
    card_status = request.args.get('card_status', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    # بناء الاستعلام
    filter_query = {}
    
    if query:
        filter_query['$or'] = [
            {'staff_name': {'$regex': query, '$options': 'i'}},
            {'staff_name_ara': {'$regex': query, '$options': 'i'}},
            {'staff_no': {'$regex': query, '$options': 'i'}},
            {'pass_no': {'$regex': query, '$options': 'i'}}
        ]
    
    if nationality:
        filter_query['nationality_code'] = nationality
    
    if company:
        filter_query['company_code'] = company
    
    # إضافة فلاتر حالة الجواز والبطاقة لقاعدة البيانات مباشرة
    if passport_status == 'missing':
        filter_query['$or'] = filter_query.get('$or', [])
        if not isinstance(filter_query['$or'], list):
            filter_query['$or'] = []
        filter_query['$and'] = filter_query.get('$and', [])
        filter_query['$and'].append({'$or': [{'pass_no': {'$exists': False}}, {'pass_no': None}, {'pass_no': ''}]})
    elif passport_status == 'available':
        filter_query['pass_no'] = {'$exists': True, '$ne': None, '$ne': ''}
    
    if card_status == 'missing':
        filter_query['$and'] = filter_query.get('$and', [])
        filter_query['$and'].append({'$or': [{'card_no': {'$exists': False}}, {'card_no': None}, {'card_no': ''}]})
    elif card_status == 'expired':
        filter_query['card_expiry_date'] = {'$lt': datetime.now()}
    
    # حساب pagination
    skip = (page - 1) * per_page
    
    employees = list(mongo.db.employees.find(filter_query).skip(skip).limit(per_page))
    total = mongo.db.employees.count_documents(filter_query)
    
    # إضافة معلومات الشركة والوظيفة
    results = []
    for emp in employees:
        # جلب معلومات الشركة
        company_info = mongo.db.companies.find_one({'company_code': emp.get('company_code')})
        # جلب معلومات الوظيفة
        job_info = mongo.db.jobs.find_one({'job_code': emp.get('job_code')})
        
        emp_dict = serialize_doc(emp)
        emp_dict.update(get_employee_status(emp))
        
        if company_info:
            emp_dict['company_eng'] = company_info.get('company_name_eng', '')
            emp_dict['company_ara'] = company_info.get('company_name_ara', '')
        
        if job_info:
            emp_dict['job_eng'] = job_info.get('job_eng', '')
            emp_dict['job_ara'] = job_info.get('job_ara', '')
            
        results.append(emp_dict)
    
    pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'employees': results,
        'total': total,
        'pages': pages,
        'current_page': page,
        'has_next': page < pages,
        'has_prev': page > 1
    })

# API لإضافة موظف جديد
@app.route('/api/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['staff_no', 'staff_name', 'staff_name_ara', 'job_code', 'nationality_code', 'company_code']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'حقل {field} مطلوب'}), 400
        
        # التحقق من عدم وجود موظف بنفس الرقم
        existing = mongo.db.employees.find_one({'staff_no': data['staff_no']})
        if existing:
            return jsonify({'error': 'رقم الموظف موجود مسبقاً'}), 400
        
        # تحويل تاريخ انتهاء البطاقة
        if data.get('card_expiry_date'):
            try:
                data['card_expiry_date'] = datetime.strptime(data['card_expiry_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'تنسيق التاريخ غير صحيح'}), 400
        
        # إضافة تاريخ الإنشاء
        data['create_date_time'] = datetime.now()
        
        # إدراج الموظف في MongoDB
        result = mongo.db.employees.insert_one(data)
        
        # جلب الموظف المضاف مع التفاصيل الكاملة
        employee = mongo.db.employees.find_one({'_id': result.inserted_id})
        emp_dict = serialize_doc(employee)
        emp_dict.update(get_employee_status(employee))
        
        return jsonify(emp_dict), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API لتحديث بيانات موظف
@app.route('/api/employees/<staff_no>', methods=['PUT'])
def update_employee(staff_no):
    try:
        # تحويل staff_no إلى integer للبحث
        staff_no_int = int(staff_no)
        data = request.get_json()
        
        # تحويل تاريخ انتهاء البطاقة إذا كان موجوداً
        if 'card_expiry_date' in data and data['card_expiry_date']:
            try:
                data['card_expiry_date'] = datetime.strptime(data['card_expiry_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'تنسيق التاريخ غير صحيح'}), 400
        elif 'card_expiry_date' in data and not data['card_expiry_date']:
            data['card_expiry_date'] = None
        
        # تحديث الموظف
        result = mongo.db.employees.update_one(
            {'staff_no': staff_no_int},
            {'$set': data}
        )
        
        if result.matched_count == 0:
            return jsonify({'error': 'الموظف غير موجود'}), 404
        
        # جلب الموظف المحدث
        employee = mongo.db.employees.find_one({'staff_no': staff_no_int})
        emp_dict = serialize_doc(employee)
        emp_dict.update(get_employee_status(employee))
        
        return jsonify(emp_dict)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API لحذف موظف
@app.route('/api/employees/<staff_no>', methods=['DELETE'])
def delete_employee(staff_no):
    try:
        # تحويل staff_no إلى integer للبحث
        staff_no_int = int(staff_no)
        result = mongo.db.employees.delete_one({'staff_no': staff_no_int})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'الموظف غير موجود'}), 404
        
        return jsonify({'message': 'تم حذف الموظف بنجاح'})
        
    except ValueError:
        return jsonify({'error': 'رقم الموظف غير صحيح'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API للحصول على بيانات موظف محدد
@app.route('/api/employees/<staff_no>')
def get_employee(staff_no):
    try:
        # تحويل staff_no إلى integer للبحث
        staff_no_int = int(staff_no)
        employee = mongo.db.employees.find_one({'staff_no': staff_no_int})
        
        if not employee:
            return jsonify({'error': 'الموظف غير موجود'}), 404
        
        emp_dict = serialize_doc(employee)
        emp_dict.update(get_employee_status(employee))
        return jsonify(emp_dict)
        
    except ValueError:
        return jsonify({'error': 'رقم الموظف غير صحيح'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API للإحصائيات
@app.route('/api/statistics')
def get_statistics():
    total_employees = mongo.db.employees.count_documents({})
    
    # إحصائيات الجنسيات
    nationality_pipeline = [
        {'$group': {'_id': '$nationality_code', 'count': {'$sum': 1}}}
    ]
    nationality_stats = {item['_id']: item['count'] for item in mongo.db.employees.aggregate(nationality_pipeline)}
    
    # إحصائيات الشركات
    company_pipeline = [
        {'$lookup': {
            'from': 'companies',
            'localField': 'company_code',
            'foreignField': 'company_code',
            'as': 'company_info'
        }},
        {'$group': {
            '_id': '$company_code',
            'count': {'$sum': 1},
            'company_name': {'$first': {'$arrayElemAt': ['$company_info.company_name_ara', 0]}}
        }}
    ]
    company_stats = {item['company_name'] or item['_id']: item['count'] 
                    for item in mongo.db.employees.aggregate(company_pipeline)}
    
    # إحصائيات الوظائف
    job_pipeline = [
        {'$lookup': {
            'from': 'jobs',
            'localField': 'job_code',
            'foreignField': 'job_code',
            'as': 'job_info'
        }},
        {'$group': {
            '_id': '$job_code',
            'count': {'$sum': 1},
            'job_name': {'$first': {'$arrayElemAt': ['$job_info.job_ara', 0]}}
        }}
    ]
    job_stats = {item['job_name'] or str(item['_id']): item['count'] 
                for item in mongo.db.employees.aggregate(job_pipeline)}
    
    # إحصائيات حالة الجوازات والبطاقات
    employees = list(mongo.db.employees.find())
    passport_missing = sum(1 for emp in employees if not emp.get('pass_no'))
    cards_missing = sum(1 for emp in employees if not emp.get('card_no'))
    
    cards_expired = 0
    for emp in employees:
        if emp.get('card_expiry_date'):
            expiry_date = emp['card_expiry_date']
            if isinstance(expiry_date, str):
                expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
            if expiry_date < datetime.now():
                cards_expired += 1
    
    return jsonify({
        'total_employees': total_employees,
        'nationality_stats': nationality_stats,
        'company_stats': company_stats,
        'job_stats': job_stats,
        'passport_missing': passport_missing,
        'cards_missing': cards_missing,
        'cards_expired': cards_expired
    })

# API للحصول على قوائم الفلاتر
@app.route('/api/filters')
def get_filters():
    nationalities = mongo.db.employees.distinct('nationality_code')
    companies = list(mongo.db.companies.find({}, {'company_code': 1, 'company_name_ara': 1, '_id': 0}))
    
    return jsonify({
        'nationalities': nationalities,
        'companies': [{'code': c['company_code'], 'name': c['company_name_ara']} for c in companies]
    })

@app.route('/api/test')
def test_connection():
    """اختبار الاتصال"""
    return jsonify({'status': 'OK', 'message': 'Server is running with MongoDB'})

# API للعرض المختصر للموظفين
@app.route('/api/employees-summary')
def employees_summary():
    """عرض مختصر لجميع الموظفين مع المعلومات الأساسية فقط"""
    query = request.args.get('query', '').strip()
    nationality = request.args.get('nationality', '')
    company = request.args.get('company', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))  # عدد أكبر للعرض المختصر
    
    # بناء الاستعلام
    filter_query = {}
    
    if query:
        filter_query['$or'] = [
            {'staff_name': {'$regex': query, '$options': 'i'}},
            {'staff_name_ara': {'$regex': query, '$options': 'i'}},
            {'staff_no': {'$regex': query, '$options': 'i'}}
        ]
    
    if nationality:
        filter_query['nationality_code'] = nationality
    
    if company:
        filter_query['company_code'] = company
    
    # حساب pagination
    skip = (page - 1) * per_page
    
    # جلب البيانات الأساسية فقط
    employees = list(mongo.db.employees.find(
        filter_query,
        {
            'staff_no': 1,
            'staff_name': 1,
            'staff_name_ara': 1,
            'nationality_code': 1,
            'company_code': 1,
            'pass_no': 1,
            'card_no': 1,
            'card_expiry_date': 1
        }
    ).skip(skip).limit(per_page))
    
    total = mongo.db.employees.count_documents(filter_query)
    
    # إعداد النتائج المختصرة
    results = []
    for emp in employees:
        # حالة الجواز
        passport_status = '✅' if emp.get('pass_no') else '❌'
        
        # حالة البطاقة
        if not emp.get('card_no'):
            card_status = '❌'
        elif not emp.get('card_expiry_date'):
            card_status = '⚠️'
        else:
            expiry_date = emp['card_expiry_date']
            if isinstance(expiry_date, str):
                expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
            
            if expiry_date < datetime.now():
                card_status = '🔴'
            elif expiry_date < datetime.now() + timedelta(days=90):
                card_status = '🟡'
            else:
                card_status = '🟢'
        
        results.append({
            'staff_no': emp.get('staff_no'),
            'name': emp.get('staff_name_ara') or emp.get('staff_name', ''),
            'nationality': emp.get('nationality_code', ''),
            'company': emp.get('company_code', ''),
            'passport': passport_status,
            'card': card_status
        })
    
    pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'employees': results,
        'total': total,
        'pages': pages,
        'current_page': page,
        'has_next': page < pages,
        'has_prev': page > 1
    })

# API تصدير النتائج المفلترة
@app.route('/api/export-filtered-results', methods=['POST'])
def export_filtered_results():
    """تصدير النتائج المفلترة كملف Excel"""
    try:
        data = request.get_json()
        employees = data.get('employees', [])
        filters = data.get('filters', {})
        total = data.get('total', 0)
        
        if not employees:
            return jsonify({'error': 'لا توجد بيانات للتصدير'}), 400
        
        # إعداد البيانات للتصدير
        report_data = []
        for emp in employees:
            # جلب معلومات الشركة والوظيفة
            company_info = mongo.db.companies.find_one({'company_code': emp.get('company_code')})
            job_info = mongo.db.jobs.find_one({'job_code': emp.get('job_code')})
            
            report_data.append({
                'رقم الموظف': emp.get('staff_no', ''),
                'الاسم بالعربية': emp.get('staff_name_ara', ''),
                'الاسم بالإنجليزية': emp.get('staff_name', ''),
                'الوظيفة': job_info.get('job_ara', '') if job_info else '',
                'الشركة': company_info.get('company_name_ara', '') if company_info else '',
                'الجنسية': emp.get('nationality_code', ''),
                'رقم الجواز': emp.get('pass_no', 'غير متوفر'),
                'حالة الجواز': emp.get('passport_text', ''),
                'رقم البطاقة': emp.get('card_no', 'غير متوفرة'),
                'حالة البطاقة': emp.get('card_text', ''),
                'تاريخ انتهاء البطاقة': emp.get('card_expiry_date', 'غير محدد'),
                'تاريخ الإنشاء': emp.get('create_date_time', '')
            })
        
        # إنشاء DataFrame
        df = pd.DataFrame(report_data)
        
        # إنشاء ملف Excel في الذاكرة
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # كتابة البيانات
                df.to_excel(writer, sheet_name='بيانات الموظفين', index=False)
                
                # إضافة معلومات الفلتر
                filter_info = []
                if filters.get('query'):
                    filter_info.append(f"البحث: {filters['query']}")
                if filters.get('nationality'):
                    filter_info.append(f"الجنسية: {filters['nationality']}")
                if filters.get('company'):
                    filter_info.append(f"الشركة: {filters['company']}")
                if filters.get('passport_status'):
                    filter_info.append(f"حالة الجواز: {filters['passport_status']}")
                if filters.get('card_status'):
                    filter_info.append(f"حالة البطاقة: {filters['card_status']}")
                
                # إضافة ورقة معلومات التقرير
                summary_data = [
                    ['إجمالي النتائج', total],
                    ['تاريخ التقرير', datetime.now().strftime('%Y-%m-%d %H:%M')],
                    ['الفلاتر المطبقة', ' | '.join(filter_info) if filter_info else 'لا توجد فلاتر']
                ]
                
                summary_df = pd.DataFrame(summary_data, columns=['البيان', 'القيمة'])
                summary_df.to_excel(writer, sheet_name='معلومات التقرير', index=False)
                
        except Exception as e:
            return jsonify({'error': f'خطأ في إنشاء ملف Excel: {str(e)}'}), 500
            
        output.seek(0)
        
        # إرسال الملف
        filename = f"تقرير_موظفين_مفلتر_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def load_initial_data():
    """تحميل البيانات الأولية في MongoDB"""
    
    # التحقق من وجود البيانات
    if mongo.db.companies.count_documents({}) > 0:
        print("البيانات محملة مسبقاً!")
        return
    
    # بيانات الشركات
    companies_data = [
        {"company_code": "BRG", "company_name_eng": "Middle East Bridge Trading", "company_name_ara": "میدل ایست بریدج للتجارة العامة (ش.ذ.م.م)"},
        {"company_code": "HON", "company_name_eng": "Honda Resources", "company_name_ara": "موارد هوندا"},
        {"company_code": "LIV", "company_name_eng": "Liverage Trading", "company_name_ara": "ليفردج للتجارة"},
        {"company_code": "MNT", "company_name_eng": "Mınt Art Galery", "company_name_ara": "مينت آرت جالاري"},
        {"company_code": "SQF", "company_name_eng": "SQFT General Store", "company_name_ara": "اس كيو اف تي للمخازن العامة"},
        {"company_code": "TAM", "company_name_eng": "Tamayoz", "company_name_ara": "تميز"},
        {"company_code": "UNI", "company_name_eng": "UNI FOOD GENERAL TRADING LLC", "company_name_ara": "يونيفود للتجارة"}
    ]
    
    mongo.db.companies.insert_many(companies_data)
    
    # بيانات الوظائف
    jobs_data = [
        {"job_code": 1, "job_eng": "Accountant", "job_ara": "محاسب"},
        {"job_code": 2, "job_eng": "Archive Clerk", "job_ara": "كاتب الأرشیف"},
        {"job_code": 3, "job_eng": "Commercial Sales Representative", "job_ara": "ممثل مبيعات تجاري"},
        {"job_code": 4, "job_eng": "Computer Engineer", "job_ara": "مھندس كومبیوتر"},
        {"job_code": 5, "job_eng": "Filing Clerk", "job_ara": "كاتب ملفات"},
        {"job_code": 6, "job_eng": "Marketing Manager", "job_ara": "مدير التسويق"},
        {"job_code": 7, "job_eng": "Messenger", "job_ara": "مراسل"},
        {"job_code": 8, "job_eng": "Operations Manager", "job_ara": "مدير عمليات"},
        {"job_code": 9, "job_eng": "Sales Manager", "job_ara": "مدیر المبیعات"},
        {"job_code": 10, "job_eng": "Shop Assistant", "job_ara": "عامل مساعد بمتجر"},
        {"job_code": 11, "job_eng": "Stall and Market Salesperson", "job_ara": "مندوب مبيعات الأكشاك والسوق"},
        {"job_code": 12, "job_eng": "Stevedore", "job_ara": "محمل سفن"},
        {"job_code": 13, "job_eng": "Legal Consultant", "job_ara": "استشاري قانوني"},
        {"job_code": 14, "job_eng": "Finance Director", "job_ara": "مدیر المالیة"},
        {"job_code": 15, "job_eng": "Administration Manager", "job_ara": "مدير ادارة"},
        {"job_code": 16, "job_eng": "Loading and unloading worker", "job_ara": "عامل الشحن والتفريغ"},
        {"job_code": 17, "job_eng": "Marketing Specialist", "job_ara": "أخصائي تسويق"},
        {"job_code": 18, "job_eng": "Storekeeper", "job_ara": "أمين مخزن"},
        {"job_code": 19, "job_eng": "General Manager", "job_ara": "مدير عام"}
    ]
    
    mongo.db.jobs.insert_many(jobs_data)
    print("تم تحميل بيانات الشركات والوظائف بنجاح في MongoDB!")

if __name__ == '__main__':
    # تحميل البيانات الأولية
    load_initial_data()
    
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
