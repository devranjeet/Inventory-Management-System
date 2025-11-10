"""
Dashboard View
"""
import tkinter as tk
from tkinter import ttk
from models.reports import ReportManager
from datetime import datetime


class DashboardView:
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.report_manager = ReportManager(db)
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create dashboard widgets"""
        # Title
        title_label = ttk.Label(self.parent, text="Dashboard", 
                               font=('Helvetica', 20, 'bold'))
        title_label.pack(pady=10)
        
        # Stats container
        stats_frame = ttk.Frame(self.parent)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create stat cards
        self.stat_cards = {}
        
        # Row 1
        row1 = ttk.Frame(stats_frame)
        row1.pack(fill='x', pady=10)
        
        self.stat_cards['total_products'] = self.create_stat_card(row1, "Total Products", "0", "📦")
        self.stat_cards['low_stock'] = self.create_stat_card(row1, "Low Stock Items", "0", "⚠️")
        self.stat_cards['out_of_stock'] = self.create_stat_card(row1, "Out of Stock", "0", "❌")
        self.stat_cards['total_customers'] = self.create_stat_card(row1, "Total Customers", "0", "👥")
        
        # Row 2
        row2 = ttk.Frame(stats_frame)
        row2.pack(fill='x', pady=10)
        
        self.stat_cards['today_sales'] = self.create_stat_card(row2, "Today's Sales", "₹0", "💰")
        self.stat_cards['month_sales'] = self.create_stat_card(row2, "This Month's Sales", "₹0", "📈")
        self.stat_cards['stock_value'] = self.create_stat_card(row2, "Stock Value", "₹0", "💎")
        self.stat_cards['outstanding'] = self.create_stat_card(row2, "Outstanding Payments", "₹0", "⏰")
        
        # Alerts section
        alerts_frame = ttk.LabelFrame(stats_frame, text="Alerts & Notifications", padding=10)
        alerts_frame.pack(fill='both', expand=True, pady=10)
        
        # Alerts listbox
        self.alerts_text = tk.Text(alerts_frame, height=10, width=80, wrap='word')
        self.alerts_text.pack(fill='both', expand=True)
        self.alerts_text.config(state='disabled')
        
        # Refresh button
        refresh_btn = ttk.Button(self.parent, text="Refresh Dashboard", command=self.load_data)
        refresh_btn.pack(pady=10)
    
    def create_stat_card(self, parent, title, value, icon):
        """Create a stat card widget"""
        card = ttk.Frame(parent, relief='raised', borderwidth=2)
        card.pack(side='left', fill='both', expand=True, padx=5)
        
        # Icon
        icon_label = ttk.Label(card, text=icon, font=('Helvetica', 24))
        icon_label.pack(pady=(10, 0))
        
        # Value
        value_label = ttk.Label(card, text=value, font=('Helvetica', 18, 'bold'))
        value_label.pack()
        
        # Title
        title_label = ttk.Label(card, text=title, font=('Helvetica', 10))
        title_label.pack(pady=(0, 10))
        
        return value_label
    
    def load_data(self):
        """Load dashboard data"""
        # Get stats
        stats = self.report_manager.get_dashboard_stats()
        
        # Update stat cards
        self.stat_cards['total_products'].config(text=str(stats.get('total_products', 0)))
        self.stat_cards['low_stock'].config(text=str(stats.get('low_stock_count', 0)))
        self.stat_cards['out_of_stock'].config(text=str(stats.get('out_of_stock_count', 0)))
        self.stat_cards['total_customers'].config(text=str(stats.get('total_customers', 0)))
        
        # Format currency values
        today_sales = stats.get('today_sales_total', 0)
        month_sales = stats.get('month_sales_total', 0)
        stock_value = stats.get('total_stock_value', 0)
        outstanding = stats.get('outstanding_payments', 0)
        
        self.stat_cards['today_sales'].config(text=f"₹{today_sales:,.2f}")
        self.stat_cards['month_sales'].config(text=f"₹{month_sales:,.2f}")
        self.stat_cards['stock_value'].config(text=f"₹{stock_value:,.2f}")
        self.stat_cards['outstanding'].config(text=f"₹{outstanding:,.2f}")
        
        # Load alerts
        self.load_alerts(stats)
    
    def load_alerts(self, stats):
        """Load and display alerts"""
        self.alerts_text.config(state='normal')
        self.alerts_text.delete(1.0, tk.END)
        
        alerts = []
        
        # Low stock alerts
        if stats.get('low_stock_count', 0) > 0:
            alerts.append(f"⚠️  {stats['low_stock_count']} products have low stock levels")
        
        # Out of stock alerts
        if stats.get('out_of_stock_count', 0) > 0:
            alerts.append(f"❌  {stats['out_of_stock_count']} products are out of stock")
        
        # Outstanding payments alerts
        if stats.get('outstanding_payments', 0) > 0:
            alerts.append(f"⏰  Outstanding supplier payments: ₹{stats['outstanding_payments']:,.2f}")
        
        if not alerts:
            alerts.append("✅  No alerts at this time. Everything looks good!")
        
        for alert in alerts:
            self.alerts_text.insert(tk.END, alert + "\n\n")
        
        self.alerts_text.config(state='disabled')
