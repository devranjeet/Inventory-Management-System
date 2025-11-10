"""
Reports and Analytics Module
"""
from datetime import datetime, timedelta


class ReportManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_sales_report(self, start_date, end_date):
        """Generate sales report for a date range"""
        try:
            self.db.cursor.execute('''
                SELECT 
                    DATE(sale_date) as date,
                    COUNT(sale_id) as total_sales,
                    SUM(subtotal) as subtotal,
                    SUM(tax_amount) as tax,
                    SUM(discount_amount) as discount,
                    SUM(total_amount) as total
                FROM sales
                WHERE sale_date BETWEEN ? AND ?
                GROUP BY DATE(sale_date)
                ORDER BY date
            ''', (start_date, end_date))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error generating sales report: {e}")
            return []
    
    def get_purchase_report(self, start_date, end_date):
        """Generate purchase report for a date range"""
        try:
            self.db.cursor.execute('''
                SELECT 
                    DATE(purchase_date) as date,
                    COUNT(purchase_id) as total_purchases,
                    SUM(total_amount) as total_amount,
                    SUM(paid_amount) as paid_amount,
                    SUM(total_amount - paid_amount) as outstanding
                FROM purchases
                WHERE purchase_date BETWEEN ? AND ?
                GROUP BY DATE(purchase_date)
                ORDER BY date
            ''', (start_date, end_date))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error generating purchase report: {e}")
            return []
    
    def get_profit_loss_report(self, start_date, end_date):
        """Generate profit/loss report"""
        try:
            # Get sales revenue
            self.db.cursor.execute('''
                SELECT SUM(total_amount) as total_sales
                FROM sales
                WHERE sale_date BETWEEN ? AND ?
            ''', (start_date, end_date))
            sales_data = self.db.cursor.fetchone()
            total_sales = sales_data['total_sales'] if sales_data['total_sales'] else 0
            
            # Get cost of goods sold
            self.db.cursor.execute('''
                SELECT SUM(si.quantity * p.unit_price) as cogs
                FROM sale_items si
                JOIN products p ON si.product_id = p.product_id
                JOIN sales s ON si.sale_id = s.sale_id
                WHERE s.sale_date BETWEEN ? AND ?
            ''', (start_date, end_date))
            cogs_data = self.db.cursor.fetchone()
            cogs = cogs_data['cogs'] if cogs_data['cogs'] else 0
            
            # Get expenses
            self.db.cursor.execute('''
                SELECT SUM(amount) as total_expenses
                FROM expenses
                WHERE expense_date BETWEEN ? AND ?
            ''', (start_date, end_date))
            expense_data = self.db.cursor.fetchone()
            expenses = expense_data['total_expenses'] if expense_data['total_expenses'] else 0
            
            # Calculate profit
            gross_profit = total_sales - cogs
            net_profit = gross_profit - expenses
            
            return {
                'total_sales': total_sales,
                'cogs': cogs,
                'gross_profit': gross_profit,
                'expenses': expenses,
                'net_profit': net_profit,
                'gross_margin': (gross_profit / total_sales * 100) if total_sales > 0 else 0,
                'net_margin': (net_profit / total_sales * 100) if total_sales > 0 else 0
            }
        except Exception as e:
            print(f"Error generating profit/loss report: {e}")
            return None
    
    def get_top_selling_products(self, start_date, end_date, limit=10):
        """Get top selling products"""
        try:
            self.db.cursor.execute('''
                SELECT 
                    p.product_id,
                    p.product_name,
                    p.sku,
                    SUM(si.quantity) as total_quantity,
                    SUM(si.total_price) as total_revenue,
                    COUNT(DISTINCT si.sale_id) as sale_count
                FROM sale_items si
                JOIN products p ON si.product_id = p.product_id
                JOIN sales s ON si.sale_id = s.sale_id
                WHERE s.sale_date BETWEEN ? AND ?
                GROUP BY p.product_id
                ORDER BY total_quantity DESC
                LIMIT ?
            ''', (start_date, end_date, limit))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching top selling products: {e}")
            return []
    
    def get_category_sales_report(self, start_date, end_date):
        """Get sales report by category"""
        try:
            self.db.cursor.execute('''
                SELECT 
                    c.category_name,
                    COUNT(DISTINCT si.sale_id) as sale_count,
                    SUM(si.quantity) as total_quantity,
                    SUM(si.total_price) as total_revenue
                FROM sale_items si
                JOIN products p ON si.product_id = p.product_id
                JOIN categories c ON p.category_id = c.category_id
                JOIN sales s ON si.sale_id = s.sale_id
                WHERE s.sale_date BETWEEN ? AND ?
                GROUP BY c.category_id
                ORDER BY total_revenue DESC
            ''', (start_date, end_date))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error generating category sales report: {e}")
            return []
    
    def get_supplier_purchase_report(self, start_date, end_date):
        """Get purchase report by supplier"""
        try:
            self.db.cursor.execute('''
                SELECT 
                    s.supplier_name,
                    COUNT(p.purchase_id) as purchase_count,
                    SUM(p.total_amount) as total_amount,
                    SUM(p.paid_amount) as paid_amount,
                    SUM(p.total_amount - p.paid_amount) as outstanding
                FROM purchases p
                JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE p.purchase_date BETWEEN ? AND ?
                GROUP BY s.supplier_id
                ORDER BY total_amount DESC
            ''', (start_date, end_date))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error generating supplier purchase report: {e}")
            return []
    
    def get_dashboard_stats(self):
        """Get key metrics for dashboard"""
        try:
            stats = {}
            
            # Total products
            self.db.cursor.execute('SELECT COUNT(*) as count FROM products')
            stats['total_products'] = self.db.cursor.fetchone()['count']
            
            # Low stock products
            self.db.cursor.execute('''
                SELECT COUNT(*) as count FROM products 
                WHERE stock_quantity <= min_stock_level
            ''')
            stats['low_stock_count'] = self.db.cursor.fetchone()['count']
            
            # Out of stock products
            self.db.cursor.execute('SELECT COUNT(*) as count FROM products WHERE stock_quantity = 0')
            stats['out_of_stock_count'] = self.db.cursor.fetchone()['count']
            
            # Today's sales
            today = datetime.now().strftime('%Y-%m-%d')
            self.db.cursor.execute('''
                SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total
                FROM sales WHERE DATE(sale_date) = ?
            ''', (today,))
            today_sales = self.db.cursor.fetchone()
            stats['today_sales_count'] = today_sales['count']
            stats['today_sales_total'] = today_sales['total']
            
            # This month's sales
            first_day = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            self.db.cursor.execute('''
                SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total
                FROM sales WHERE sale_date >= ?
            ''', (first_day,))
            month_sales = self.db.cursor.fetchone()
            stats['month_sales_count'] = month_sales['count']
            stats['month_sales_total'] = month_sales['total']
            
            # Total customers
            self.db.cursor.execute('SELECT COUNT(*) as count FROM customers')
            stats['total_customers'] = self.db.cursor.fetchone()['count']
            
            # Total suppliers
            self.db.cursor.execute('SELECT COUNT(*) as count FROM suppliers')
            stats['total_suppliers'] = self.db.cursor.fetchone()['count']
            
            # Outstanding payments
            self.db.cursor.execute('SELECT COALESCE(SUM(outstanding_payment), 0) as total FROM suppliers')
            stats['outstanding_payments'] = self.db.cursor.fetchone()['total']
            
            # Total stock value
            self.db.cursor.execute('''
                SELECT COALESCE(SUM(stock_quantity * unit_price), 0) as total
                FROM products
            ''')
            stats['total_stock_value'] = self.db.cursor.fetchone()['total']
            
            return stats
        except Exception as e:
            print(f"Error fetching dashboard stats: {e}")
            return {}
