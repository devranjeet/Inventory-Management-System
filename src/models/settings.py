"""
Settings Management Module
"""

class SettingsManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_setting(self, key):
        """Get a setting value"""
        try:
            self.db.cursor.execute('''
                SELECT setting_value FROM settings WHERE setting_key = ?
            ''', (key,))
            result = self.db.cursor.fetchone()
            return result['setting_value'] if result else None
        except Exception as e:
            print(f"Error fetching setting: {e}")
            return None
    
    def set_setting(self, key, value):
        """Set a setting value"""
        try:
            self.db.cursor.execute('''
                INSERT OR REPLACE INTO settings (setting_key, setting_value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error setting value: {e}")
            return False
    
    def get_all_settings(self):
        """Get all settings"""
        try:
            self.db.cursor.execute('SELECT * FROM settings ORDER BY setting_key')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching settings: {e}")
            return []
    
    def get_currency(self):
        """Get currency setting"""
        return self.get_setting('currency') or 'INR'
    
    def get_tax_rate(self):
        """Get tax rate setting"""
        try:
            return float(self.get_setting('tax_rate') or 0)
        except:
            return 0.0
    
    def get_theme(self):
        """Get theme setting"""
        return self.get_setting('theme') or 'default'
    
    def get_low_stock_threshold(self):
        """Get low stock threshold"""
        try:
            return int(self.get_setting('low_stock_threshold') or 10)
        except:
            return 10
