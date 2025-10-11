import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# إعدادات قاعدة البيانات
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/employees_db')