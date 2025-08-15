# 🚀 دليل النشر على Render

## خطوات النشر:

### 1. الإعداد المسبق ✅
- [x] رفع الكود إلى GitHub
- [x] إعداد ملفات النشر (render.yaml, Procfile, gunicorn.conf.py)
- [x] قاعدة بيانات MongoDB Atlas جاهزة

### 2. إنشاء الخدمة على Render

1. **اذهب إلى [Render.com](https://render.com)**
2. **اضغط "New +" > "Web Service"**
3. **اختر "Connect a repository"**
4. **اختر المستودع: `Yamanxl9/employee-management-system`**

### 3. إعدادات الخدمة

```
Name: employee-management-system
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --config gunicorn.conf.py
```

### 4. متغيرات البيئة المطلوبة

أضف هذه المتغيرات في قسم "Environment Variables":

```
MONGODB_URI=mongodb+srv://yamantakala5:Yaman123@cluster0.sgxaxpf.mongodb.net/employees_db
SECRET_KEY=employee-management-secret-key-2025
FLASK_ENV=production
PORT=10000
```

### 5. إعدادات إضافية

- **Region**: Oregon (US West) أو أقرب منطقة
- **Plan**: Free tier (مناسب للاختبار)
- **Auto-Deploy**: نعم (تنشيط التحديث التلقائي)

### 6. بعد النشر

ستحصل على رابط مثل:
```
https://employee-management-system-xxx.onrender.com
```

### 7. اختبار التطبيق

تأكد من عمل:
- [ ] الصفحة الرئيسية
- [ ] البحث بالعربي والإنجليزي
- [ ] الفلاتر والإحصائيات
- [ ] تصدير البيانات

### 8. استكشاف الأخطاء

إذا فشل النشر، تحقق من:
1. **Logs**: في لوحة Render تحت "Logs"
2. **Environment Variables**: تأكد من صحة MONGODB_URI
3. **Build Logs**: تحقق من تثبيت المكتبات

---

## معلومات قاعدة البيانات

- **Platform**: MongoDB Atlas
- **Database**: employees_db
- **Collections**: employees (71), companies (13), jobs (22)
- **Connection**: Configured and tested ✅

## الميزات المتاحة

✅ **البحث الذكي**: عربي/إنجليزي  
✅ **الفلاتر المتقدمة**: جنسية، شركة، وظيفة  
✅ **الإحصائيات**: لوحة تحكم شاملة  
✅ **التصدير**: Excel مع تنسيق عربي  
✅ **تسجيل الأنشطة**: Audit logs  
✅ **إدارة الحالات**: جوازات وبطاقات  

---

## الدعم الفني

للمساعدة في النشر أو حل المشاكل، تحقق من:
- [Render Documentation](https://render.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- GitHub Repository Issues
