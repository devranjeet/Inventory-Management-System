"""
Category Management Module
"""

class CategoryManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_category(self, category_name, description=None):
        """Add a new category"""
        try:
            self.db.cursor.execute('''
                INSERT INTO categories (category_name, description)
                VALUES (?, ?)
            ''', (category_name, description))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error adding category: {e}")
            return None
    
    def update_category(self, category_id, category_name=None, description=None):
        """Update category information"""
        try:
            updates = []
            params = []
            
            if category_name:
                updates.append("category_name = ?")
                params.append(category_name)
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            
            if not updates:
                return False
            
            params.append(category_id)
            query = f"UPDATE categories SET {', '.join(updates)} WHERE category_id = ?"
            
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
    
    def delete_category(self, category_id):
        """Delete a category"""
        try:
            # Check if category has products
            self.db.cursor.execute('SELECT COUNT(*) FROM products WHERE category_id = ?', 
                                 (category_id,))
            if self.db.cursor.fetchone()[0] > 0:
                return False
            
            self.db.cursor.execute('DELETE FROM categories WHERE category_id = ?', (category_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
    
    def get_all_categories(self):
        """Get all categories"""
        try:
            self.db.cursor.execute('''
                SELECT c.*, COUNT(p.product_id) as product_count
                FROM categories c
                LEFT JOIN products p ON c.category_id = p.category_id
                GROUP BY c.category_id
                ORDER BY c.category_name
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
    
    def get_category_by_id(self, category_id):
        """Get category by ID"""
        try:
            self.db.cursor.execute('''
                SELECT * FROM categories WHERE category_id = ?
            ''', (category_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching category: {e}")
            return None
    
    def get_products_by_category(self, category_id):
        """Get all products in a category"""
        try:
            self.db.cursor.execute('''
                SELECT p.*, s.supplier_name
                FROM products p
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE p.category_id = ?
                ORDER BY p.product_name
            ''', (category_id,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching products by category: {e}")
            return []
