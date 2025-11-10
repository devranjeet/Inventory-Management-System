"""
Expense Management Module
"""

class ExpenseManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_expense(self, expense_type, amount, expense_date, description=None, created_by=None):
        """Add a new expense"""
        try:
            self.db.cursor.execute('''
                INSERT INTO expenses (expense_type, amount, expense_date, description, created_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (expense_type, amount, expense_date, description, created_by))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error adding expense: {e}")
            return None
    
    def update_expense(self, expense_id, **kwargs):
        """Update expense information"""
        try:
            allowed_fields = ['expense_type', 'amount', 'expense_date', 'description']
            
            updates = []
            params = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    updates.append(f"{field} = ?")
                    params.append(value)
            
            if not updates:
                return False
            
            params.append(expense_id)
            query = f"UPDATE expenses SET {', '.join(updates)} WHERE expense_id = ?"
            
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating expense: {e}")
            return False
    
    def delete_expense(self, expense_id):
        """Delete an expense"""
        try:
            self.db.cursor.execute('DELETE FROM expenses WHERE expense_id = ?', (expense_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False
    
    def get_all_expenses(self):
        """Get all expenses"""
        try:
            self.db.cursor.execute('''
                SELECT e.*, u.username as created_by_name
                FROM expenses e
                LEFT JOIN users u ON e.created_by = u.user_id
                ORDER BY e.expense_date DESC
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching expenses: {e}")
            return []
    
    def get_expenses_by_date_range(self, start_date, end_date):
        """Get expenses within a date range"""
        try:
            self.db.cursor.execute('''
                SELECT e.*, u.username as created_by_name
                FROM expenses e
                LEFT JOIN users u ON e.created_by = u.user_id
                WHERE e.expense_date BETWEEN ? AND ?
                ORDER BY e.expense_date DESC
            ''', (start_date, end_date))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching expenses by date range: {e}")
            return []
    
    def get_expenses_by_type(self, expense_type):
        """Get expenses by type"""
        try:
            self.db.cursor.execute('''
                SELECT e.*, u.username as created_by_name
                FROM expenses e
                LEFT JOIN users u ON e.created_by = u.user_id
                WHERE e.expense_type = ?
                ORDER BY e.expense_date DESC
            ''', (expense_type,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching expenses by type: {e}")
            return []
    
    def get_expense_summary(self, start_date, end_date):
        """Get expense summary by type"""
        try:
            self.db.cursor.execute('''
                SELECT 
                    expense_type,
                    COUNT(*) as count,
                    SUM(amount) as total_amount
                FROM expenses
                WHERE expense_date BETWEEN ? AND ?
                GROUP BY expense_type
                ORDER BY total_amount DESC
            ''', (start_date, end_date))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error generating expense summary: {e}")
            return []
