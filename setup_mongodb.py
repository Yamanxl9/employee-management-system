"""
سكريبت لإعداد قاعدة بيانات MongoDB لتتوافق مع نظام إدارة الموظفين
يقوم بإنشاء المجموعات والفهارس المطلوبة وتحميل البيانات التجريبية
"""

from pymongo import MongoClient, ASCENDING, TEXT
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging
from werkzeug.security import generate_password_hash
import random

# تحميل متغيرات البيئة
load_dotenv()

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_database_connection():
    """الحصول على اتصال قاعدة البيانات"""
    try:
        # محاولة الاتصال بـ MongoDB Atlas أولاً
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # اختبار الاتصال
        client.admin.command('ismaster')
        
        # اختيار قاعدة البيانات
        if 'mongodb.net' in mongodb_uri:
            # إذا كان Atlas، استخرج اسم قاعدة البيانات من URI
            db_name = mongodb_uri.split('/')[-1].split('?')[0] or 'employees_db'
        else:
            db_name = 'employees_db'
            
        db = client[db_name]
        logger.info(f"✅ نجح الاتصال بقاعدة البيانات: {db_name}")
        return client, db
        
    except Exception as e:
        logger.error(f"❌ فشل في الاتصال بقاعدة البيانات: {e}")
        return None, None

def create_collections_and_indexes(db):
    """إنشاء المجموعات والفهارس المطلوبة"""
    try:
        # إنشاء collection للشركات
        companies = db.companies
        companies.create_index([("company_code", ASCENDING)], unique=True)
        companies.create_index([("company_name_eng", TEXT), ("company_name_ara", TEXT)])
        logger.info("✅ تم إنشاء مجموعة الشركات والفهارس")
        
        # إنشاء collection للوظائف
        jobs = db.jobs
        jobs.create_index([("job_code", ASCENDING)], unique=True)
        jobs.create_index([("job_eng", TEXT), ("job_ara", TEXT)])
        logger.info("✅ تم إنشاء مجموعة الوظائف والفهارس")
        
        # إنشاء collection للموظفين
        employees = db.employees
        employees.create_index([("staff_no", ASCENDING)], unique=True)
        employees.create_index([("staff_name", TEXT), ("staff_name_ara", TEXT)])
        employees.create_index([("nationality_code", ASCENDING)])
        employees.create_index([("company_code", ASCENDING)])
        employees.create_index([("job_code", ASCENDING)])
        employees.create_index([("pass_no", ASCENDING)])
        employees.create_index([("card_no", ASCENDING)])
        employees.create_index([("card_expiry_date", ASCENDING)])
        employees.create_index([("create_date_time", ASCENDING)])
        logger.info("✅ تم إنشاء مجموعة الموظفين والفهارس")
        
        # إنشاء collection للمستخدمين
        users = db.users
        users.create_index([("username", ASCENDING)], unique=True)
        logger.info("✅ تم إنشاء مجموعة المستخدمين والفهارس")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في إنشاء المجموعات: {e}")
        return False

def insert_sample_companies(db):
    """إدراج بيانات الشركات التجريبية"""
    try:
        companies_data = [
            {
                "company_code": "001",
                "company_name_eng": "Alpha Construction",
                "company_name_ara": "شركة ألفا للإنشاءات"
            },
            {
                "company_code": "002", 
                "company_name_eng": "Beta Trading",
                "company_name_ara": "شركة بيتا للتجارة"
            },
            {
                "company_code": "003",
                "company_name_eng": "Gamma Services",
                "company_name_ara": "شركة جاما للخدمات"
            },
            {
                "company_code": "004",
                "company_name_eng": "Delta Engineering",
                "company_name_ara": "شركة دلتا للهندسة"
            },
            {
                "company_code": "005",
                "company_name_eng": "Epsilon Technology",
                "company_name_ara": "شركة إبسيلون للتكنولوجيا"
            }
        ]
        
        # حذف البيانات الموجودة
        db.companies.delete_many({})
        
        # إدراج البيانات الجديدة
        result = db.companies.insert_many(companies_data)
        logger.info(f"✅ تم إدراج {len(result.inserted_ids)} شركة")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في إدراج بيانات الشركات: {e}")
        return False

def insert_sample_jobs(db):
    """إدراج بيانات الوظائف التجريبية"""
    try:
        jobs_data = [
            {"job_code": "ENG", "job_eng": "Engineer", "job_ara": "مهندس"},
            {"job_code": "MGR", "job_eng": "Manager", "job_ara": "مدير"},
            {"job_code": "TEC", "job_eng": "Technician", "job_ara": "فني"},
            {"job_code": "ACC", "job_eng": "Accountant", "job_ara": "محاسب"},
            {"job_code": "SEC", "job_eng": "Secretary", "job_ara": "سكرتير"},
            {"job_code": "DRV", "job_eng": "Driver", "job_ara": "سائق"},
            {"job_code": "GRD", "job_eng": "Guard", "job_ara": "حارس"},
            {"job_code": "CLN", "job_eng": "Cleaner", "job_ara": "عامل نظافة"},
            {"job_code": "ITT", "job_eng": "IT Specialist", "job_ara": "أخصائي تقنية"},
            {"job_code": "HRT", "job_eng": "HR Specialist", "job_ara": "أخصائي موارد بشرية"}
        ]
        
        # حذف البيانات الموجودة
        db.jobs.delete_many({})
        
        # إدراج البيانات الجديدة
        result = db.jobs.insert_many(jobs_data)
        logger.info(f"✅ تم إدراج {len(result.inserted_ids)} وظيفة")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في إدراج بيانات الوظائف: {e}")
        return False

def insert_sample_employees(db):
    """إدراج بيانات الموظفين التجريبية"""
    try:
        # أسماء تجريبية
        names_data = [
            ("Ahmed Ali", "أحمد علي", "EGY"),
            ("Sarah Mohammed", "سارة محمد", "SAU"),
            ("Omar Hassan", "عمر حسن", "JOR"),
            ("Fatima Abdullah", "فاطمة عبدالله", "UAE"),
            ("Khalid Ibrahim", "خالد إبراهيم", "KWT"),
            ("Mona Youssef", "منى يوسف", "EGY"),
            ("Hassan Ahmad", "حسن أحمد", "LBN"),
            ("Layla Salem", "ليلى سالم", "SAU"),
            ("Mohammed Nasser", "محمد ناصر", "QAT"),
            ("Nour Al-Din", "نور الدين", "BHR"),
            ("Amina Rashid", "آمينة راشد", "UAE"),
            ("Tarek Mahmoud", "طارق محمود", "EGY"),
            ("Rania Farid", "رانيا فريد", "JOR"),
            ("Abdullah Al-Mansouri", "عبدالله المنصوري", "UAE"),
            ("Yasmin Kamal", "ياسمين كمال", "SAU"),
            ("Sami Al-Zahra", "سامي الزهراء", "KWT"),
            ("Hala Mustafa", "هالة مصطفى", "EGY"),
            ("Waleed Al-Rashid", "وليد الراشد", "SAU"),
            ("Dina Abbas", "دينا عباس", "LBN"),
            ("Majid Al-Amiri", "ماجد الأميري", "UAE"),
            ("Reem Sultan", "ريم سلطان", "QAT"),
            ("Faisal Al-Otaibi", "فيصل العتيبي", "SAU"),
            ("Lina Habib", "لينا حبيب", "JOR"),
            ("Youssef Al-Maktoum", "يوسف المكتوم", "UAE"),
            ("Rana Abdel Rahman", "رنا عبد الرحمن", "EGY")
        ]
        
        companies = ["001", "002", "003", "004", "005"]
        jobs = ["ENG", "MGR", "TEC", "ACC", "SEC", "DRV", "GRD", "CLN", "ITT", "HRT"]
        
        employees_data = []
        
        for i, (name_eng, name_ara, nationality) in enumerate(names_data, 1):
            staff_no = 100000 + i
            
            # تحديد ما إذا كان لديه جواز (80% لديهم جواز)
            has_passport = random.random() < 0.8
            passport_no = f"P{random.randint(1000000, 9999999)}" if has_passport else ""
            
            # تحديد ما إذا كان لديه بطاقة (90% لديهم بطاقة)
            has_card = random.random() < 0.9
            card_no = f"C{random.randint(100000, 999999)}" if has_card else ""
            
            # تاريخ انتهاء البطاقة (إذا كان لديه بطاقة)
            card_expiry = None
            if has_card:
                # 70% بطاقات سارية، 20% تنتهي قريباً، 10% منتهية
                rand_val = random.random()
                if rand_val < 0.7:  # سارية
                    card_expiry = (datetime.now() + timedelta(days=random.randint(60, 365))).strftime("%Y-%m-%d")
                elif rand_val < 0.9:  # تنتهي قريباً
                    card_expiry = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
                else:  # منتهية
                    card_expiry = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
            
            employee = {
                "staff_no": staff_no,
                "staff_name": name_eng,
                "staff_name_ara": name_ara,
                "job_code": random.choice(jobs),
                "nationality_code": nationality,
                "company_code": random.choice(companies),
                "pass_no": passport_no,
                "card_no": card_no,
                "card_expiry_date": card_expiry,
                "create_date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            employees_data.append(employee)
        
        # حذف البيانات الموجودة
        db.employees.delete_many({})
        
        # إدراج البيانات الجديدة
        result = db.employees.insert_many(employees_data)
        logger.info(f"✅ تم إدراج {len(result.inserted_ids)} موظف")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في إدراج بيانات الموظفين: {e}")
        return False

def create_admin_user(db):
    """إنشاء المستخدم الإداري"""
    try:
        # حذف المستخدمين الموجودين
        db.users.delete_many({})
        
        # إنشاء المستخدم الإداري
        admin_user = {
            "username": "admin",
            "password": generate_password_hash("admin123"),
            "role": "admin",
            "created_at": datetime.now()
        }
        
        result = db.users.insert_one(admin_user)
        logger.info(f"✅ تم إنشاء المستخدم الإداري: admin/admin123")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في إنشاء المستخدم الإداري: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء إعداد قاعدة البيانات MongoDB...")
    
    # الاتصال بقاعدة البيانات
    client, db = get_database_connection()
    if db is None:
        return False
    
    try:
        # إنشاء المجموعات والفهارس
        if not create_collections_and_indexes(db):
            return False
        
        # إدراج بيانات الشركات
        if not insert_sample_companies(db):
            return False
        
        # إدراج بيانات الوظائف
        if not insert_sample_jobs(db):
            return False
        
        # إدراج بيانات الموظفين
        if not insert_sample_employees(db):
            return False
        
        # إنشاء المستخدم الإداري
        if not create_admin_user(db):
            return False
        
        logger.info("🎉 تم إعداد قاعدة البيانات بنجاح!")
        logger.info("📊 إحصائيات قاعدة البيانات:")
        logger.info(f"   - الشركات: {db.companies.count_documents({})}")
        logger.info(f"   - الوظائف: {db.jobs.count_documents({})}")
        logger.info(f"   - الموظفين: {db.employees.count_documents({})}")
        logger.info(f"   - المستخدمين: {db.users.count_documents({})}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ عام في إعداد قاعدة البيانات: {e}")
        return False
        
    finally:
        client.close()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ تم إعداد قاعدة البيانات بنجاح!")
        print("🔑 بيانات المستخدم الإداري:")
        print("   اسم المستخدم: admin")
        print("   كلمة المرور: admin123")
    else:
        print("\n❌ فشل في إعداد قاعدة البيانات!")
