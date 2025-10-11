from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# إعداد قاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "employees.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# نماذج قاعدة البيانات
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    company_code = db.Column(db.String(10), unique=True, nullable=False)
    company_name_eng = db.Column(db.String(100), nullable=False)
    company_name_ara = db.Column(db.String(100), nullable=False)

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_code = db.Column(db.String(10), unique=True, nullable=False)
    job_eng = db.Column(db.String(100), nullable=False)
    job_ara = db.Column(db.String(100), nullable=False)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    staff_no = db.Column(db.String(20), unique=True, nullable=False)
    staff_name = db.Column(db.String(100), nullable=False)
    staff_name_ara = db.Column(db.String(100), nullable=False)
    job_code = db.Column(db.String(10), nullable=False)
    pass_no = db.Column(db.String(50))
    nationality_code = db.Column(db.String(50))
    company_code = db.Column(db.String(10), nullable=False)
    card_no = db.Column(db.String(50))
    card_expiry_date = db.Column(db.Date)
    create_date_time = db.Column(db.DateTime, default=datetime.utcnow)

# إنشاء الجداول
def init_db():
    with app.app_context():
        db.create_all()
        
        # تحميل البيانات الأولية
        if Company.query.count() == 0:
            load_initial_data()

def load_initial_data():
    # تحميل الشركات
    companies_data = [
        {"company_code": "001", "company_name_eng": "Al-Aqeeli Trading", "company_name_ara": "العقيلي للتجارة"},
        {"company_code": "002", "company_name_eng": "Al-Aqeeli Construction", "company_name_ara": "العقيلي للإنشاءات"},
        {"company_code": "003", "company_name_eng": "Al-Aqeeli Services", "company_name_ara": "العقيلي للخدمات"},
        {"company_code": "004", "company_name_eng": "Al-Aqeeli Industries", "company_name_ara": "العقيلي للصناعات"},
        {"company_code": "005", "company_name_eng": "Al-Aqeeli Real Estate", "company_name_ara": "العقيلي للعقارات"},
        {"company_code": "006", "company_name_eng": "Al-Aqeeli Technology", "company_name_ara": "العقيلي للتكنولوجيا"},
        {"company_code": "007", "company_name_eng": "Al-Aqeeli Logistics", "company_name_ara": "العقيلي للنقل"}
    ]
    
    for comp_data in companies_data:
        company = Company(**comp_data)
        db.session.add(company)
    
    # تحميل الوظائف
    jobs_data = [
        {"job_code": "MGR", "job_eng": "Manager", "job_ara": "مدير"},
        {"job_code": "ACC", "job_eng": "Accountant", "job_ara": "محاسب"},
        {"job_code": "ENG", "job_eng": "Engineer", "job_ara": "مهندس"},
        {"job_code": "SEC", "job_eng": "Secretary", "job_ara": "سكرتير"},
        {"job_code": "DR", "job_eng": "Driver", "job_ara": "سائق"},
        {"job_code": "GRD", "job_eng": "Guard", "job_ara": "حارس"},
        {"job_code": "CLN", "job_eng": "Cleaner", "job_ara": "عامل نظافة"},
        {"job_code": "TCH", "job_eng": "Technician", "job_ara": "فني"},
        {"job_code": "SAL", "job_eng": "Sales Representative", "job_ara": "مندوب مبيعات"},
        {"job_code": "HR", "job_eng": "HR Specialist", "job_ara": "أخصائي موارد بشرية"},
        {"job_code": "IT", "job_eng": "IT Specialist", "job_ara": "أخصائي تقنية معلومات"},
        {"job_code": "FIN", "job_eng": "Financial Analyst", "job_ara": "محلل مالي"},
        {"job_code": "MKT", "job_eng": "Marketing Specialist", "job_ara": "أخصائي تسويق"},
        {"job_code": "OPR", "job_eng": "Operations Officer", "job_ara": "ضابط عمليات"},
        {"job_code": "QC", "job_eng": "Quality Controller", "job_ara": "مراقب جودة"},
        {"job_code": "PRJ", "job_eng": "Project Coordinator", "job_ara": "منسق مشاريع"},
        {"job_code": "LOG", "job_eng": "Logistics Officer", "job_ara": "ضابط لوجستي"},
        {"job_code": "PUR", "job_eng": "Purchasing Officer", "job_ara": "ضابط مشتريات"},
        {"job_code": "REL", "job_eng": "Public Relations", "job_ara": "علاقات عامة"},
        {"job_code": "TRN", "job_eng": "Trainer", "job_ara": "مدرب"},
        {"job_code": "SOFF", "job_eng": "Sales Officer", "job_ara": "ضابط مبيعات"},
        {"job_code": "AST", "job_eng": "Assistant", "job_ara": "مساعد"}
    ]
    
    for job_data in jobs_data:
        job = Job(**job_data)
        db.session.add(job)
    
    db.session.commit()
    print("تم تحميل البيانات الأولية بنجاح!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/filters')
def get_filters():
    companies = Company.query.all()
    jobs = Job.query.all()
    
    return jsonify({
        'companies': [{'company_code': c.company_code, 'company_name_ara': c.company_name_ara, 'company_name_eng': c.company_name_eng} for c in companies],
        'jobs': [{'job_code': j.job_code, 'job_ara': j.job_ara, 'job_eng': j.job_eng} for j in jobs]
    })

@app.route('/api/employees')
def get_employees():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    search = request.args.get('search', '')
    company_code = request.args.get('company_code', '')
    job_code = request.args.get('job_code', '')
    passport_status = request.args.get('passport_status', '')
    card_status = request.args.get('card_status', '')
    
    query = Employee.query
    
    # تطبيق الفلاتر
    if search:
        query = query.filter(
            (Employee.staff_name.contains(search)) |
            (Employee.staff_name_ara.contains(search)) |
            (Employee.staff_no.contains(search))
        )
    
    if company_code:
        query = query.filter(Employee.company_code == company_code)
    
    if job_code:
        query = query.filter(Employee.job_code == job_code)
    
    if passport_status:
        if passport_status == 'available':
            query = query.filter(Employee.pass_no.isnot(None), Employee.pass_no != '')
        elif passport_status == 'missing':
            query = query.filter((Employee.pass_no.is_(None)) | (Employee.pass_no == ''))
    
    if card_status:
        today = date.today()
        if card_status == 'valid':
            query = query.filter(Employee.card_expiry_date > today)
        elif card_status == 'expired':
            query = query.filter(Employee.card_expiry_date <= today)
        elif card_status == 'missing':
            query = query.filter((Employee.card_no.is_(None)) | (Employee.card_no == ''))
    
    # ترقيم الصفحات
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    employees = pagination.items
    
    # إضافة معلومات الشركة والوظيفة
    result = []
    for emp in employees:
        company = Company.query.filter_by(company_code=emp.company_code).first()
        job = Job.query.filter_by(job_code=emp.job_code).first()
        
        emp_data = {
            'staff_no': emp.staff_no,
            'staff_name': emp.staff_name,
            'staff_name_ara': emp.staff_name_ara,
            'job_code': emp.job_code,
            'job_ara': job.job_ara if job else '',
            'job_eng': job.job_eng if job else '',
            'pass_no': emp.pass_no or '',
            'nationality_code': emp.nationality_code or '',
            'company_code': emp.company_code,
            'company_name_ara': company.company_name_ara if company else '',
            'company_name_eng': company.company_name_eng if company else '',
            'card_no': emp.card_no or '',
            'card_expiry_date': emp.card_expiry_date.strftime('%Y-%m-%d') if emp.card_expiry_date else '',
            'create_date_time': emp.create_date_time.strftime('%Y-%m-%d %H:%M:%S') if emp.create_date_time else ''
        }
        result.append(emp_data)
    
    return jsonify({
        'employees': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.json
    
    # التحقق من عدم وجود موظف بنفس الرقم
    existing = Employee.query.filter_by(staff_no=data['staff_no']).first()
    if existing:
        return jsonify({'success': False, 'message': 'رقم الموظف موجود مسبقاً'}), 400
    
    # تحويل تاريخ انتهاء البطاقة
    card_expiry = None
    if data.get('card_expiry_date'):
        try:
            card_expiry = datetime.strptime(data['card_expiry_date'], '%Y-%m-%d').date()
        except:
            pass
    
    employee = Employee(
        staff_no=data['staff_no'],
        staff_name=data['staff_name'],
        staff_name_ara=data['staff_name_ara'],
        job_code=data['job_code'],
        pass_no=data.get('pass_no', ''),
        nationality_code=data.get('nationality_code', ''),
        company_code=data['company_code'],
        card_no=data.get('card_no', ''),
        card_expiry_date=card_expiry
    )
    
    try:
        db.session.add(employee)
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم إضافة الموظف بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في إضافة الموظف: {str(e)}'}), 500

@app.route('/api/employees/<staff_no>', methods=['PUT'])
def update_employee(staff_no):
    employee = Employee.query.filter_by(staff_no=staff_no).first()
    if not employee:
        return jsonify({'success': False, 'message': 'الموظف غير موجود'}), 404
    
    data = request.json
    
    # تحديث البيانات
    employee.staff_name = data.get('staff_name', employee.staff_name)
    employee.staff_name_ara = data.get('staff_name_ara', employee.staff_name_ara)
    employee.job_code = data.get('job_code', employee.job_code)
    employee.pass_no = data.get('pass_no', employee.pass_no)
    employee.nationality_code = data.get('nationality_code', employee.nationality_code)
    employee.company_code = data.get('company_code', employee.company_code)
    employee.card_no = data.get('card_no', employee.card_no)
    
    # تحديث تاريخ انتهاء البطاقة
    if data.get('card_expiry_date'):
        try:
            employee.card_expiry_date = datetime.strptime(data['card_expiry_date'], '%Y-%m-%d').date()
        except:
            pass
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم تحديث بيانات الموظف بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في تحديث الموظف: {str(e)}'}), 500

@app.route('/api/employees/<staff_no>', methods=['DELETE'])
def delete_employee(staff_no):
    employee = Employee.query.filter_by(staff_no=staff_no).first()
    if not employee:
        return jsonify({'success': False, 'message': 'الموظف غير موجود'}), 404
    
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم حذف الموظف بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ في حذف الموظف: {str(e)}'}), 500

@app.route('/api/statistics')
def get_statistics():
    total_employees = Employee.query.count()
    
    # إحصائيات الجوازات
    employees_with_passport = Employee.query.filter(
        Employee.pass_no.isnot(None), 
        Employee.pass_no != ''
    ).count()
    employees_without_passport = total_employees - employees_with_passport
    
    # إحصائيات البطاقات
    today = date.today()
    employees_with_valid_card = Employee.query.filter(Employee.card_expiry_date > today).count()
    employees_with_expired_card = Employee.query.filter(Employee.card_expiry_date <= today).count()
    employees_without_card = Employee.query.filter(
        (Employee.card_no.is_(None)) | (Employee.card_no == '')
    ).count()
    
    return jsonify({
        'total_employees': total_employees,
        'passport_stats': {
            'available': employees_with_passport,
            'missing': employees_without_passport
        },
        'card_stats': {
            'valid': employees_with_valid_card,
            'expired': employees_with_expired_card,
            'missing': employees_without_card
        }
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
