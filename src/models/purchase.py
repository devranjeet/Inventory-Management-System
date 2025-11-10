"""
Purchase Management Module
"""
from datetime import datetime


class PurchaseManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def generate_invoice_number(self):
        """Generate unique purchase invoice number"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f'PUR-{timestamp}'
    
    def add_purchase(self, supplier_id, purchase_date, items, paid_amount=0, notes=None, created_by=None):
        """
        Add a new purchase
        items: list of dicts with keys: product_id, quantity, unit_price
        """
        try:
            # Calculate total
            total_amount = sum(item['quantity'] * item['unit_price'] for item in items)
            
            # Determine payment status
            if paid_amount >= total_amount:
                payment_status = 'Paid'
            elif paid_amount > 0:
                payment_status = 'Partial'
            else:
                payment_status = 'Pending'
            
            # Generate invoice number
            invoice_number = self.generate_invoice_number()
            
            # Insert purchase
            self.db.cursor.execute('''
                INSERT INTO purchases (invoice_number, supplier_id, purchase_date, 
                                     total_amount, paid_amount, payment_status, notes, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_number, supplier_id, purchase_date, total_amount, 
                 paid_amount, payment_status, notes, created_by))
            
            purchase_id = self.db.cursor.lastrowid
            
            # Insert purchase items and update stock
            for item in items:
                item_total = item['quantity'] * item['unit_price']
                
                self.db.cursor.execute('''
                    INSERT INTO purchase_items (purchase_id, product_id, quantity, 
                                              unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (purchase_id, item['product_id'], item['quantity'], 
                     item['unit_price'], item_total))
                
                # Update product stock
                self.db.cursor.execute('''
                    UPDATE products SET stock_quantity = stock_quantity + ?
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
                    VALUES (?, 'Purchase', ?, ?, ?, ?, ?)
                ''', (item['product_id'], item['quantity'], 
                     new_stock - item['quantity'], new_stock, purchase_id, created_by))
            
            # Update supplier outstanding payment
            outstanding = total_amount - paid_amount
            if outstanding > 0:
                self.db.cursor.execute('''
                    UPDATE suppliers 
                    SET outstanding_payment = outstanding_payment + ?
                    WHERE supplier_id = ?
                ''', (outstanding, supplier_id))
            
            self.db.conn.commit()
            return purchase_id
        except Exception as e:
            print(f"Error adding purchase: {e}")
            self.db.conn.rollback()
            return None
    
    def get_purchase_by_id(self, purchase_id):
        """Get purchase details"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, s.supplier_name, u.username as created_by_name
                FROM purchases p
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                LEFT JOIN users u ON p.created_by = u.user_id
                WHERE p.purchase_id = ?
            ''', (purchase_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching purchase: {e}")
            return None
    
    def get_purchase_items(self, purchase_id):
        """Get items in a purchase"""
        try:
            self.db.cursor.execute('''
                SELECT pi.*, p.product_name, p.sku
                FROM purchase_items pi
                JOIN products p ON pi.product_id = p.product_id
                WHERE pi.purchase_id = ?
            ''', (purchase_id,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching purchase items: {e}")
            return []
    
    def get_all_purchases(self):
        """Get all purchases"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, s.supplier_name, u.username as created_by_name
                FROM purchases p
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                LEFT JOIN users u ON p.created_by = u.user_id
                ORDER BY p.purchase_date DESC
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching purchases: {e}")
            return []
    
    def update_payment(self, purchase_id, additional_payment):
        """Update payment for a purchase"""
        try:
            # Get current purchase details
            self.db.cursor.execute('''
                SELECT total_amount, paid_amount, supplier_id 
                FROM purchases WHERE purchase_id = ?
            ''', (purchase_id,))
            purchase = self.db.cursor.fetchone()
            
            if not purchase:
                return False
            
            new_paid_amount = purchase['paid_amount'] + additional_payment
            
            # Determine new payment status
            if new_paid_amount >= purchase['total_amount']:
                payment_status = 'Paid'
            elif new_paid_amount > 0:
                payment_status = 'Partial'
            else:
                payment_status = 'Pending'
            
            # Update purchase
            self.db.cursor.execute('''
                UPDATE purchases 
                SET paid_amount = ?, payment_status = ?
                WHERE purchase_id = ?
            ''', (new_paid_amount, payment_status, purchase_id))
            
            # Update supplier outstanding payment
            self.db.cursor.execute('''
                UPDATE suppliers 
                SET outstanding_payment = outstanding_payment - ?
                WHERE supplier_id = ?
            ''', (additional_payment, purchase['supplier_id']))
            
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating payment: {e}")
            self.db.conn.rollback()
            return False
