# -*- coding: utf-8 -*-
"""
database.py — إدارة قاعدة بيانات SQLite لسوبرماركت زعرب
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zarab.db')

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """إنشاء الجداول إذا لم تكن موجودة"""
    conn = get_conn()
    c = conn.cursor()

    # جدول الزبائن
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            phone       TEXT,
            status      TEXT    DEFAULT 'عادي',
            created_at  TEXT    DEFAULT (datetime('now','localtime'))
        )
    ''')

    # جدول المعاملات (دفع / دين / مشترى)
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            type        TEXT    NOT NULL,  -- 'purchase' | 'payment' | 'debt'
            description TEXT,
            amount      REAL    NOT NULL,
            is_paid     INTEGER DEFAULT 0, -- 0=دين, 1=مدفوع
            date        TEXT    DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')

    conn.commit()
    conn.close()

# ─── عمليات الزبائن ───────────────────────────────────────
def add_customer(name, phone='', status='عادي'):
    conn = get_conn()
    conn.execute(
        'INSERT INTO customers (name, phone, status) VALUES (?,?,?)',
        (name, phone, status)
    )
    conn.commit()
    conn.close()

def get_all_customers():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM customers ORDER BY name').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def search_customers(query):
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? ORDER BY name',
        (f'%{query}%', f'%{query}%')
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_customer(customer_id):
    conn = get_conn()
    conn.execute('DELETE FROM transactions WHERE customer_id=?', (customer_id,))
    conn.execute('DELETE FROM customers WHERE id=?', (customer_id,))
    conn.commit()
    conn.close()

def update_customer(customer_id, name, phone, status):
    conn = get_conn()
    conn.execute(
        'UPDATE customers SET name=?, phone=?, status=? WHERE id=?',
        (name, phone, status, customer_id)
    )
    conn.commit()
    conn.close()

# ─── عمليات المعاملات ─────────────────────────────────────
def add_transaction(customer_id, type_, description, amount, is_paid=1):
    conn = get_conn()
    conn.execute(
        'INSERT INTO transactions (customer_id, type, description, amount, is_paid) VALUES (?,?,?,?,?)',
        (customer_id, type_, description, amount, is_paid)
    )
    conn.commit()
    conn.close()

def get_transactions(customer_id):
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM transactions WHERE customer_id=? ORDER BY date DESC',
        (customer_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_customer_summary(customer_id):
    """
    حساب الملخص المالي بنظام المقاصة:
    - مجموع المشتريات: إحصائية لكل ما تم شراؤه.
    - الدين: مجموع (المعاملات من نوع 'debt' + أي معاملات غير مدفوعة).
    - المدفوع: مجموع المعاملات من نوع 'payment'.
    النتيجة: (المدفوع - الدين) يحدد هل للزبون رصيد أم عليه دين.
    """
    conn = get_conn()
    
    # 1. مجموع المشتريات (كل ما أخذه الزبون: كاش + دين)
    total_purchases = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE customer_id=? AND (type='purchase' OR type='debt')",
        (customer_id,)
    ).fetchone()[0]
    
    # 2. إجمالي الديون المسجلة (نوع دين أو أي معامله is_paid=0)
    total_debt = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE customer_id=? AND (type='debt' OR is_paid=0)",
        (customer_id,)
    ).fetchone()[0]
    
    # 3. إجمالي الدفعات المسجلة (نوع payment)
    total_payments = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM transactions WHERE customer_id=? AND type='payment'",
        (customer_id,)
    ).fetchone()[0]
    
    conn.close()
    
    # الحساب الصافي
    balance = total_payments - total_debt
    
    if balance >= 0:
        # رصيد إيجابي: الزبون دفع أكثر مما عليه
        return {
            'paid': float(balance),
            'debt': 0.0,
            'total_purchases': float(total_purchases)
        }
    else:
        # رصيد سلبي: الزبون عليه دين
        return {
            'paid': 0.0,
            'debt': float(abs(balance)),
            'total_purchases': float(total_purchases)
        }

# ─── بيانات تجريبية ───────────────────────────────────────
def seed_sample_data():
    """إضافة بيانات تجريبية إذا كانت القاعدة فارغة"""
    conn = get_conn()
    count = conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
    conn.close()
    if count > 0:
        return  # البيانات موجودة مسبقاً

    samples = [
        ('محمد العلي',  '0599-111-222', 'دائم'),
        ('سارة خالد',   '0598-333-444', 'جديد'),
        ('أحمد يوسف',   '0597-555-666', 'VIP'),
        ('نور الدين',   '0596-777-888', 'عادي'),
        ('ليلى حسن',    '0595-999-000', 'دائم'),
        ('خالد سمير',   '0594-123-456', 'عادي'),
        ('منى إبراهيم', '0593-654-321', 'دائم'),
        ('يوسف طارق',   '0592-789-012', 'جديد'),
    ]
    for name, phone, status in samples:
        add_customer(name, phone, status)

    # معاملات تجريبية للزبون الأول
    conn = get_conn()
    first_id = conn.execute('SELECT id FROM customers LIMIT 1').fetchone()[0]
    conn.close()
    add_transaction(first_id, 'purchase', 'تفاح + موز',  45.0,  is_paid=1)
    add_transaction(first_id, 'purchase', 'حليب + خبز',  22.0,  is_paid=1)
    add_transaction(first_id, 'payment',  'دفعة نقدية',  150.0, is_paid=1)
    add_transaction(first_id, 'purchase', 'زيت زيتون',   90.0,  is_paid=0)

if __name__ == '__main__':
    init_db()
    seed_sample_data()
    print('DB initialized at:', DB_PATH)
    print('Customers:', get_all_customers())
