# نسخة مبسطة من التطبيق تستخدم SQLite بدلاً من MongoDB
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-key'

# إنشاء قاعدة البيانات والجداول
def init_db():
    conn = sqlite3.connect('employees_simple.db')
    cursor = conn.cursor()
    
    # جدول الشركات
    cursor.execute('''CREATE TABLE IF NOT EXISTS companies (
        company_code TEXT PRIMARY KEY,
        company_name_eng TEXT,
        company_name_ara TEXT
    )''')
    
    # جدول الوظائف
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
        job_code INTEGER PRIMARY KEY,
        job_eng TEXT,
        job_ara TEXT
    )''')
    
    # جدول الموظفين
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
        staff_no TEXT PRIMARY KEY,
        staff_name TEXT,
        staff_name_ara TEXT,
        job_code INTEGER,
        pass_no TEXT,
        nationality_code TEXT,
        company_code TEXT,
        card_no TEXT,
        card_expiry_date TEXT,
        create_date_time TEXT
    )''')
    
    # إدخال بيانات تجريبية
    companies = [
        ("IN", "IN Company", "شركة IN"),
        ("YONIFOOD", "YONIFOOD Trading", "يونيفود للتجارة"),
        ("SCM", "SCM General Stores", "اس كيو اف تي للمخازن العامة")
    ]
    
    jobs = [
        (1, "Accountant", "محاسب"),
        (2, "Sales Representative", "مندوب مبيعات"),
        (3, "Store Keeper", "أمين مخزن"),
        (4, "Manager", "مدير")
    ]
    
    employees = [
        ("P9057552", "Salah Iqbal Fairfiri", "صلاح إقبال فيرفيري", 1, "P9057552", "IN", "IN", "100230994227238", "2025-12-31", datetime.now().isoformat()),
        ("P4678866", "MUHAMED NIHAL PATTAMARU VALAPPIL", "محمد نهال باتامارو فالابيل", 1, "P4678866", "IN", "YONIFOOD", "100070996846473", "2025-06-30", datetime.now().isoformat()),
        ("N6308013", "MOHAMED FAYIZ ABOOBACKER", "محمد فايز أبو بكر", 2, "N6308013", "IN", "YONIFOOD", "100051074387878", "2024-12-31", datetime.now().isoformat())
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO companies VALUES (?, ?, ?)', companies)
    cursor.executemany('INSERT OR REPLACE INTO jobs VALUES (?, ?, ?)', jobs)
    cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', employees)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('simple_index.html')

@app.route('/api/test')
def api_test():
    return jsonify({'status': 'ok', 'message': 'API working'})

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    return jsonify({'valid': True, 'user': {'username': 'demo'}})

@app.route('/api/statistics')
def get_statistics():
    conn = sqlite3.connect('employees_simple.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM employees')
    total_employees = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM employees WHERE pass_no IS NULL OR pass_no = ""')
    passport_missing = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM employees WHERE card_no IS NULL OR card_no = ""')
    cards_missing = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM employees WHERE card_expiry_date < ?', (datetime.now().strftime('%Y-%m-%d'),))
    cards_expired = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_employees': total_employees,
        'passport_missing': passport_missing,
        'cards_missing': cards_missing,
        'cards_expired': cards_expired
    })

@app.route('/api/filters')
def get_filters():
    conn = sqlite3.connect('employees_simple.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT nationality_code FROM employees WHERE nationality_code IS NOT NULL')
    nationalities = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT company_code, company_name_ara FROM companies')
    companies = [{'code': row[0], 'name': row[1]} for row in cursor.fetchall()]
    
    cursor.execute('SELECT job_code, job_ara FROM jobs ORDER BY job_code')
    jobs = [{'code': row[0], 'name': row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'nationalities': nationalities,
        'companies': companies,
        'jobs': jobs
    })

@app.route('/api/search')
def search_employees():
    query = request.args.get('query', '').strip()
    nationality = request.args.get('nationality', '')
    company = request.args.get('company', '')
    job = request.args.get('job', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    conn = sqlite3.connect('employees_simple.db')
    cursor = conn.cursor()
    
    # بناء الاستعلام
    where_conditions = []
    params = []
    
    if query:
        where_conditions.append('(staff_name LIKE ? OR staff_name_ara LIKE ? OR staff_no LIKE ? OR pass_no LIKE ?)')
        params.extend([f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'])
    
    if nationality:
        where_conditions.append('nationality_code = ?')
        params.append(nationality)
    
    if company:
        where_conditions.append('company_code = ?')
        params.append(company)
    
    if job:
        where_conditions.append('job_code = ?')
        params.append(job)
    
    where_clause = ' AND '.join(where_conditions) if where_conditions else '1=1'
    
    # حساب العدد الإجمالي
    cursor.execute(f'SELECT COUNT(*) FROM employees WHERE {where_clause}', params)
    total = cursor.fetchone()[0]
    
    # جلب البيانات مع pagination
    offset = (page - 1) * per_page
    cursor.execute(f'''
        SELECT e.*, c.company_name_eng, c.company_name_ara, j.job_eng, j.job_ara
        FROM employees e
        LEFT JOIN companies c ON e.company_code = c.company_code
        LEFT JOIN jobs j ON e.job_code = j.job_code
        WHERE {where_clause}
        LIMIT ? OFFSET ?
    ''', params + [per_page, offset])
    
    results = []
    for row in cursor.fetchall():
        emp = {
            'staff_no': row[0],
            'staff_name': row[1],
            'staff_name_ara': row[2],
            'job_code': row[3],
            'pass_no': row[4],
            'nationality_code': row[5],
            'company_code': row[6],
            'card_no': row[7],
            'card_expiry_date': row[8],
            'company_eng': row[10],
            'company_ara': row[11],
            'job_eng': row[12],
            'job_ara': row[13],
            'passport_status': 'available' if row[4] else 'missing',
            'passport_text': 'متوفر' if row[4] else 'غير متوفر',
            'passport_class': 'success' if row[4] else 'danger',
            'card_status': 'valid' if row[7] else 'missing',
            'card_text': 'سارية' if row[7] else 'غير متوفرة',
            'card_class': 'success' if row[7] else 'danger'
        }
        results.append(emp)
    
    conn.close()
    
    pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'employees': results,
        'total': total,
        'pages': pages,
        'current_page': page,
        'has_next': page < pages,
        'has_prev': page > 1
    })

@app.route('/api/employees-summary')
def employees_summary():
    return search_employees()  # نفس API البحث

if __name__ == '__main__':
    init_db()
    print("قاعدة البيانات جاهزة!")
    app.run(debug=True, port=5001)  # منفذ مختلف لتجنب التعارض
