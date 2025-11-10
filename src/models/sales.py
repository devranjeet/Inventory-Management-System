"""
Sales Management Module
"""
from datetime import datetime


class SalesManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def generate_invoice_number(self):
        """Generate unique sales invoice number"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f'INV-{timestamp}'
    
    def add_sale(self, sale_date, items, customer_id=None, tax_rate=0, 
                discount_amount=0, payment_method=None, created_by=None):
        """
        Add a new sale
        items: list of dicts with keys: product_id, quantity, unit_price
        """
        try:
            # Calculate totals
            subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
            tax_amount = (subtotal * tax_rate) / 100
            total_amount = subtotal + tax_amount - discount_amount
            
            # Generate invoice number
            invoice_number = self.generate_invoice_number()
            
            # Insert sale
            self.db.cursor.execute('''
                INSERT INTO sales (invoice_number, customer_id, sale_date, subtotal,
                                 tax_amount, discount_amount, total_amount, 
                                 payment_method, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_number, customer_id, sale_date, subtotal, tax_amount,
                 discount_amount, total_amount, payment_method, created_by))
            
            sale_id = self.db.cursor.lastrowid
            
            # Insert sale items and update stock
            for item in items:
                item_total = item['quantity'] * item['unit_price']
                
                # Check stock availability
                self.db.cursor.execute('''
                    SELECT stock_quantity FROM products WHERE product_id = ?
                ''', (item['product_id'],))
                
                product = self.db.cursor.fetchone()
                if not product or product['stock_quantity'] < item['quantity']:
                    raise Exception(f"Insufficient stock for product {item['product_id']}")
                
                self.db.cursor.execute('''
                    INSERT INTO sale_items (sale_id, product_id, quantity, 
                                          unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (sale_id, item['product_id'], item['quantity'], 
                     item['unit_price'], item_total))
                
                # Update product stock
                self.db.cursor.execute('''
                    UPDATE products SET stock_quantity = stock_quantity - ?
                    WHERE product_id = ?
                ''', (item['quantity'], item['product_id']))
                
                # Record stock history
                self.db.cursor.execute('''
                    SELECT stock_quantity FROM products WHERE product_id = ?
                ''', (item['product_id'],))
                new_stock = self.db.cursor.fetchone()['stock_quantity']
                
                self.db.cursor.execute('''
                    INSERT INTO stock_history (product_id, transaction_type, quantity_change,
                                             previous_stock, new_stock, reference_id, created_by)
                    VALUES (?, 'Sale', ?, ?, ?, ?, ?)
                ''', (item['product_id'], -item['quantity'], 
                     new_stock + item['quantity'], new_stock, sale_id, created_by))
            
            # Update customer loyalty points if customer exists
            if customer_id:
                points = int(total_amount / 100)  # 1 point per 100 currency
                self.db.cursor.execute('''
                    UPDATE customers SET loyalty_points = loyalty_points + ?
                    WHERE customer_id = ?
                ''', (points, customer_id))
            
            self.db.conn.commit()
            return sale_id
        except Exception as e:
            print(f"Error adding sale: {e}")
            self.db.conn.rollback()
            return None
    
    def get_sale_by_id(self, sale_id):
        """Get sale details"""
        try:
            self.db.cursor.execute('''
                SELECT s.*, c.customer_name, u.username as created_by_name
                FROM sales s
                LEFT JOIN customers c ON s.customer_id = c.customer_id
                LEFT JOIN users u ON s.created_by = u.user_id
                WHERE s.sale_id = ?
            ''', (sale_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching sale: {e}")
            return None
    
    def get_sale_items(self, sale_id):
        """Get items in a sale"""
        try:
            self.db.cursor.execute('''
                SELECT si.*, p.product_name, p.sku
                FROM sale_items si
                JOIN products p ON si.product_id = p.product_id
                WHERE si.sale_id = ?
            ''', (sale_id,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching sale items: {e}")
            return []
    
    def get_all_sales(self):
        """Get all sales"""
        try:
            self.db.cursor.execute('''
                SELECT s.*, c.customer_name, u.username as created_by_name
                FROM sales s
                LEFT JOIN customers c ON s.customer_id = c.customer_id
                LEFT JOIN users u ON s.created_by = u.user_id
                ORDER BY s.sale_date DESC
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching sales: {e}")
            return []
    
    def get_sales_by_date_range(self, start_date, end_date):
        """Get sales within a date range"""
        try:
            self.db.cursor.execute('''
                SELECT s.*, c.customer_name, u.username as created_by_name
                FROM sales s
                LEFT JOIN customers c ON s.customer_id = c.customer_id
                LEFT JOIN users u ON s.created_by = u.user_id
                WHERE s.sale_date BETWEEN ? AND ?
                ORDER BY s.sale_date DESC
            ''', (start_date, end_date))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching sales by date range: {e}")
            return []
