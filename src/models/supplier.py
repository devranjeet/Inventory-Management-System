"""
Supplier Management Module
"""

class SupplierManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_supplier(self, supplier_name, contact_person=None, phone=None, 
                    email=None, address=None):
        """Add a new supplier"""
        try:
            self.db.cursor.execute('''
                INSERT INTO suppliers (supplier_name, contact_person, phone, email, address)
                VALUES (?, ?, ?, ?, ?)
            ''', (supplier_name, contact_person, phone, email, address))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error adding supplier: {e}")
            return None
    
    def update_supplier(self, supplier_id, **kwargs):
        """Update supplier information"""
        try:
            allowed_fields = ['supplier_name', 'contact_person', 'phone', 'email', 
                            'address', 'outstanding_payment']
            
            updates = []
            params = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    updates.append(f"{field} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(supplier_id)
            query = f"UPDATE suppliers SET {', '.join(updates)} WHERE supplier_id = ?"
            
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating supplier: {e}")
            return False
    
    def delete_supplier(self, supplier_id):
        """Delete a supplier"""
        try:
            # Check if supplier has products
            self.db.cursor.execute('SELECT COUNT(*) FROM products WHERE supplier_id = ?', 
                                 (supplier_id,))
            if self.db.cursor.fetchone()[0] > 0:
                return False
            
            self.db.cursor.execute('DELETE FROM suppliers WHERE supplier_id = ?', (supplier_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting supplier: {e}")
            return False
    
    def get_all_suppliers(self):
        """Get all suppliers"""
        try:
            self.db.cursor.execute('''
                SELECT s.*, COUNT(p.product_id) as product_count
                FROM suppliers s
                LEFT JOIN products p ON s.supplier_id = p.supplier_id
                GROUP BY s.supplier_id
                ORDER BY s.supplier_name
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching suppliers: {e}")
            return []
    
    def get_supplier_by_id(self, supplier_id):
        """Get supplier by ID"""
        try:
            self.db.cursor.execute('''
                SELECT * FROM suppliers WHERE supplier_id = ?
            ''', (supplier_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching supplier: {e}")
            return None
    
    def get_supplier_purchases(self, supplier_id):
        """Get purchase history for a supplier"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, u.username as created_by_name
                FROM purchases p
                LEFT JOIN users u ON p.created_by = u.user_id
                WHERE p.supplier_id = ?
                ORDER BY p.purchase_date DESC
            ''', (supplier_id,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching supplier purchases: {e}")
            return []
    
    def update_outstanding_payment(self, supplier_id, amount_change):
        """Update outstanding payment for supplier"""
        try:
            self.db.cursor.execute('''
                UPDATE suppliers 
                SET outstanding_payment = outstanding_payment + ?
                WHERE supplier_id = ?
            ''', (amount_change, supplier_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating outstanding payment: {e}")
            return False
