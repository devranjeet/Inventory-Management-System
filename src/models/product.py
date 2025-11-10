"""
Product Management Module
Handles all product-related operations
"""
from datetime import datetime
import random
import string


class ProductManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def generate_sku(self):
        """Generate unique SKU for product"""
        while True:
            sku = 'SKU-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            self.db.cursor.execute('SELECT product_id FROM products WHERE sku = ?', (sku,))
            if not self.db.cursor.fetchone():
                return sku
    
    def add_product(self, product_name, category_id, supplier_id, unit_price, selling_price, 
                   stock_quantity=0, min_stock_level=10, barcode=None, description=None):
        """Add a new product"""
        try:
            sku = self.generate_sku()
            self.db.cursor.execute('''
                INSERT INTO products (sku, product_name, category_id, supplier_id, 
                                    unit_price, selling_price, stock_quantity, 
                                    min_stock_level, barcode, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (sku, product_name, category_id, supplier_id, unit_price, selling_price,
                 stock_quantity, min_stock_level, barcode, description))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error adding product: {e}")
            return None
    
    def update_product(self, product_id, **kwargs):
        """Update product information"""
        try:
            allowed_fields = ['product_name', 'category_id', 'supplier_id', 'unit_price', 
                            'selling_price', 'stock_quantity', 'min_stock_level', 
                            'barcode', 'description']
            
            updates = []
            params = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    updates.append(f"{field} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            updates.append("updated_at = ?")
            params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            params.append(product_id)
            
            query = f"UPDATE products SET {', '.join(updates)} WHERE product_id = ?"
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def delete_product(self, product_id):
        """Delete a product"""
        try:
            self.db.cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, c.category_name, s.supplier_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE p.product_id = ?
            ''', (product_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching product: {e}")
            return None
    
    def search_products(self, search_term):
        """Search products by name, SKU, or barcode"""
        try:
            search_pattern = f'%{search_term}%'
            self.db.cursor.execute('''
                SELECT p.*, c.category_name, s.supplier_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE p.product_name LIKE ? OR p.sku LIKE ? OR p.barcode LIKE ?
                ORDER BY p.product_name
            ''', (search_pattern, search_pattern, search_pattern))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_all_products(self):
        """Get all products"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, c.category_name, s.supplier_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                ORDER BY p.product_name
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
    
    def get_low_stock_products(self):
        """Get products with stock below minimum level"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, c.category_name, s.supplier_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE p.stock_quantity <= p.min_stock_level
                ORDER BY p.stock_quantity ASC
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching low stock products: {e}")
            return []
    
    def get_out_of_stock_products(self):
        """Get products that are out of stock"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, c.category_name, s.supplier_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE p.stock_quantity = 0
                ORDER BY p.product_name
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching out of stock products: {e}")
            return []
    
    def update_stock(self, product_id, quantity_change, transaction_type, reference_id=None, 
                    notes=None, created_by=None):
        """Update product stock and record history"""
        try:
            # Get current stock
            self.db.cursor.execute('SELECT stock_quantity FROM products WHERE product_id = ?', 
                                 (product_id,))
            result = self.db.cursor.fetchone()
            if not result:
                return False
            
            previous_stock = result['stock_quantity']
            new_stock = previous_stock + quantity_change
            
            if new_stock < 0:
                return False
            
            # Update stock
            self.db.cursor.execute('''
                UPDATE products SET stock_quantity = ?, updated_at = ?
                WHERE product_id = ?
            ''', (new_stock, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), product_id))
            
            # Record history
            self.db.cursor.execute('''
                INSERT INTO stock_history (product_id, transaction_type, quantity_change,
                                         previous_stock, new_stock, reference_id, notes, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product_id, transaction_type, quantity_change, previous_stock, new_stock,
                 reference_id, notes, created_by))
            
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            self.db.conn.rollback()
            return False
    
    def get_stock_history(self, product_id):
        """Get stock history for a product"""
        try:
            self.db.cursor.execute('''
                SELECT sh.*, u.username
                FROM stock_history sh
                LEFT JOIN users u ON sh.created_by = u.user_id
                WHERE sh.product_id = ?
                ORDER BY sh.created_at DESC
            ''', (product_id,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching stock history: {e}")
            return []
