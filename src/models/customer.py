"""
Customer Management Module
"""

class CustomerManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_customer(self, customer_name, phone=None, email=None, address=None):
        """Add a new customer"""
        try:
            self.db.cursor.execute('''
                INSERT INTO customers (customer_name, phone, email, address)
                VALUES (?, ?, ?, ?)
            ''', (customer_name, phone, email, address))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error adding customer: {e}")
            return None
    
    def update_customer(self, customer_id, **kwargs):
        """Update customer information"""
        try:
            allowed_fields = ['customer_name', 'phone', 'email', 'address', 'loyalty_points']
            
            updates = []
            params = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    updates.append(f"{field} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(customer_id)
            query = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = ?"
            
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False
    
    def delete_customer(self, customer_id):
        """Delete a customer"""
        try:
            self.db.cursor.execute('DELETE FROM customers WHERE customer_id = ?', (customer_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False
    
    def get_all_customers(self):
        """Get all customers"""
        try:
            self.db.cursor.execute('''
                SELECT c.*, COUNT(s.sale_id) as purchase_count
                FROM customers c
                LEFT JOIN sales s ON c.customer_id = s.customer_id
                GROUP BY c.customer_id
                ORDER BY c.customer_name
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return []
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        try:
            self.db.cursor.execute('''
                SELECT * FROM customers WHERE customer_id = ?
            ''', (customer_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching customer: {e}")
            return None
    
    def get_customer_purchases(self, customer_id):
        """Get purchase history for a customer"""
        try:
            self.db.cursor.execute('''
                SELECT s.*, u.username as created_by_name
                FROM sales s
                LEFT JOIN users u ON s.created_by = u.user_id
                WHERE s.customer_id = ?
                ORDER BY s.sale_date DESC
            ''', (customer_id,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching customer purchases: {e}")
            return []
    
    def search_customers(self, search_term):
        """Search customers by name, phone, or email"""
        try:
            search_pattern = f'%{search_term}%'
            self.db.cursor.execute('''
                SELECT c.*, COUNT(s.sale_id) as purchase_count
                FROM customers c
                LEFT JOIN sales s ON c.customer_id = s.customer_id
                WHERE c.customer_name LIKE ? OR c.phone LIKE ? OR c.email LIKE ?
                GROUP BY c.customer_id
                ORDER BY c.customer_name
            ''', (search_pattern, search_pattern, search_pattern))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error searching customers: {e}")
            return []
