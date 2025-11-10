"""
Database Manager for Inventory Management System
Handles all SQLite database operations
"""
import sqlite3
import os
from datetime import datetime
import bcrypt


class DatabaseManager:
    def __init__(self, db_path='inventory.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.create_default_admin()
    
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create all necessary database tables"""
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Admin', 'Staff')),
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Categories table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Suppliers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT NOT NULL,
                contact_person TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                outstanding_payment REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                product_name TEXT NOT NULL,
                category_id INTEGER,
                supplier_id INTEGER,
                unit_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                min_stock_level INTEGER DEFAULT 10,
                barcode TEXT UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(category_id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
            )
        ''')
        
        # Purchases table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                supplier_id INTEGER,
                purchase_date DATE NOT NULL,
                total_amount REAL NOT NULL,
                paid_amount REAL DEFAULT 0,
                payment_status TEXT CHECK(payment_status IN ('Paid', 'Partial', 'Pending')),
                notes TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        ''')
        
        # Purchase Items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_items (
                purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (purchase_id) REFERENCES purchases(purchase_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                loyalty_points INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sales table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                sale_date DATE NOT NULL,
                subtotal REAL NOT NULL,
                tax_amount REAL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                total_amount REAL NOT NULL,
                payment_method TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        ''')
        
        # Sale Items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Expenses table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_type TEXT NOT NULL,
                amount REAL NOT NULL,
                expense_date DATE NOT NULL,
                description TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        ''')
        
        # System Settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Stock History table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                transaction_type TEXT CHECK(transaction_type IN ('Purchase', 'Sale', 'Adjustment')),
                quantity_change INTEGER NOT NULL,
                previous_stock INTEGER NOT NULL,
                new_stock INTEGER NOT NULL,
                reference_id INTEGER,
                notes TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        ''')
        
        self.conn.commit()
        self.initialize_settings()
    
    def initialize_settings(self):
        """Initialize default settings"""
        default_settings = {
            'currency': 'INR',
            'tax_rate': '18',
            'discount_enabled': 'true',
            'theme': 'default',
            'low_stock_threshold': '10',
            'company_name': 'My Inventory System',
            'company_address': '',
            'company_phone': '',
            'company_email': ''
        }
        
        for key, value in default_settings.items():
            self.cursor.execute('''
                INSERT OR IGNORE INTO settings (setting_key, setting_value)
                VALUES (?, ?)
            ''', (key, value))
        
        self.conn.commit()
    
    def create_default_admin(self):
        """Create default admin user if no users exist"""
        self.cursor.execute('SELECT COUNT(*) FROM users')
        if self.cursor.fetchone()[0] == 0:
            password = 'admin123'
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, role, email)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', hashed_password.decode('utf-8'), 'Administrator', 'Admin', 'admin@inventory.com'))
            self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def backup_database(self, backup_path=None):
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f'backup/inventory_backup_{timestamp}.db'
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        import shutil
        shutil.copy2(self.db_path, backup_path)
        return backup_path
    
    def restore_database(self, backup_path):
        """Restore database from backup"""
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        self.close()
        import shutil
        shutil.copy2(backup_path, self.db_path)
        self.connect()
        return True
