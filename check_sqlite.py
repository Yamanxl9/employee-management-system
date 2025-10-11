import sqlite3

try:
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = cursor.fetchall()
    print('الجداول الموجودة:', tables)
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'عدد السجلات في {table[0]}: {count}')
    
    # عرض عينة من بيانات الموظفين
    cursor.execute('SELECT * FROM employees LIMIT 3')
    employees = cursor.fetchall()
    print('عينة من الموظفين:', employees)
    
    conn.close()
except Exception as e:
    print(f'خطأ: {e}')
