"""
Products View
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.product import ProductManager
from models.category import CategoryManager
from models.supplier import SupplierManager
from utils.barcode_gen import BarcodeGenerator
from utils.data_utils import DataExporter, DataImporter


class ProductsView:
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.product_manager = ProductManager(db)
        self.category_manager = CategoryManager(db)
        self.supplier_manager = SupplierManager(db)
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        """Create products view widgets"""
        # Title
        title_label = ttk.Label(self.parent, text="Product Management", 
                               font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=10)
        
        # Top controls
        controls_frame = ttk.Frame(self.parent)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        # Search
        ttk.Label(controls_frame, text="Search:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(controls_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        ttk.Button(controls_frame, text="Search", 
                  command=self.search_products).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Clear", 
                  command=self.load_products).pack(side='left', padx=5)
        
        # Action buttons
        btn_frame = ttk.Frame(self.parent)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="➕ Add Product", 
                  command=self.add_product_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="✏️ Edit Product", 
                  command=self.edit_product_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete Product", 
                  command=self.delete_product).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Refresh", 
                  command=self.load_products).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📤 Export", 
                  command=self.export_products).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📥 Import", 
                  command=self.import_products).pack(side='left', padx=5)
        
        # Products table
        table_frame = ttk.Frame(self.parent)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical')
        hsb = ttk.Scrollbar(table_frame, orient='horizontal')
        
        # Treeview
        columns = ('SKU', 'Name', 'Category', 'Supplier', 'Unit Price', 'Selling Price', 'Stock', 'Min Stock')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def load_products(self):
        """Load all products"""
        self.tree.delete(*self.tree.get_children())
        self.search_entry.delete(0, tk.END)
        
        products = self.product_manager.get_all_products()
        
        for product in products:
            self.tree.insert('', 'end', values=(
                product['sku'],
                product['product_name'],
                product['category_name'] or 'N/A',
                product['supplier_name'] or 'N/A',
                f"₹{product['unit_price']:.2f}",
                f"₹{product['selling_price']:.2f}",
                product['stock_quantity'],
                product['min_stock_level']
            ), tags=(product['product_id'],))
    
    def search_products(self):
        """Search products"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.load_products()
            return
        
        self.tree.delete(*self.tree.get_children())
        
        products = self.product_manager.search_products(search_term)
        
        for product in products:
            self.tree.insert('', 'end', values=(
                product['sku'],
                product['product_name'],
                product['category_name'] or 'N/A',
                product['supplier_name'] or 'N/A',
                f"₹{product['unit_price']:.2f}",
                f"₹{product['selling_price']:.2f}",
                product['stock_quantity'],
                product['min_stock_level']
            ), tags=(product['product_id'],))
    
    def add_product_dialog(self):
        """Show add product dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Product")
        dialog.geometry("500x600")
        
        # Form fields
        ttk.Label(dialog, text="Product Name:*").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Category:*").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(dialog, textvariable=category_var, width=28)
        categories = self.category_manager.get_all_categories()
        category_combo['values'] = [cat['category_name'] for cat in categories]
        category_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Supplier:*").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        supplier_var = tk.StringVar()
        supplier_combo = ttk.Combobox(dialog, textvariable=supplier_var, width=28)
        suppliers = self.supplier_manager.get_all_suppliers()
        supplier_combo['values'] = [sup['supplier_name'] for sup in suppliers]
        supplier_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Unit Price:*").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        unit_price_entry = ttk.Entry(dialog, width=30)
        unit_price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Selling Price:*").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        selling_price_entry = ttk.Entry(dialog, width=30)
        selling_price_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Stock Quantity:").grid(row=5, column=0, sticky='e', padx=5, pady=5)
        stock_entry = ttk.Entry(dialog, width=30)
        stock_entry.insert(0, "0")
        stock_entry.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Min Stock Level:").grid(row=6, column=0, sticky='e', padx=5, pady=5)
        min_stock_entry = ttk.Entry(dialog, width=30)
        min_stock_entry.insert(0, "10")
        min_stock_entry.grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Barcode:").grid(row=7, column=0, sticky='e', padx=5, pady=5)
        barcode_entry = ttk.Entry(dialog, width=30)
        barcode_entry.grid(row=7, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=8, column=0, sticky='ne', padx=5, pady=5)
        desc_text = tk.Text(dialog, width=30, height=5)
        desc_text.grid(row=8, column=1, padx=5, pady=5)
        
        def save_product():
            try:
                name = name_entry.get().strip()
                category_name = category_var.get()
                supplier_name = supplier_var.get()
                unit_price = float(unit_price_entry.get())
                selling_price = float(selling_price_entry.get())
                stock = int(stock_entry.get())
                min_stock = int(min_stock_entry.get())
                barcode = barcode_entry.get().strip() or None
                description = desc_text.get(1.0, tk.END).strip() or None
                
                if not name or not category_name or not supplier_name:
                    messagebox.showerror("Error", "Please fill all required fields")
                    return
                
                # Get category and supplier IDs
                category_id = next((c['category_id'] for c in categories 
                                  if c['category_name'] == category_name), None)
                supplier_id = next((s['supplier_id'] for s in suppliers 
                                  if s['supplier_name'] == supplier_name), None)
                
                if not category_id or not supplier_id:
                    messagebox.showerror("Error", "Invalid category or supplier")
                    return
                
                # Add product
                product_id = self.product_manager.add_product(
                    name, category_id, supplier_id, unit_price, selling_price,
                    stock, min_stock, barcode, description
                )
                
                if product_id:
                    messagebox.showinfo("Success", "Product added successfully")
                    dialog.destroy()
                    self.load_products()
                else:
                    messagebox.showerror("Error", "Failed to add product")
            except ValueError:
                messagebox.showerror("Error", "Invalid numeric values")
        
        # Save button
        ttk.Button(dialog, text="Save Product", command=save_product).grid(
            row=9, column=0, columnspan=2, pady=20)
    
    def edit_product_dialog(self):
        """Show edit product dialog"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
        
        product_id = int(self.tree.item(selected[0])['tags'][0])
        product = self.product_manager.get_product_by_id(product_id)
        
        if not product:
            messagebox.showerror("Error", "Product not found")
            return
        
        # Similar to add_product_dialog but pre-filled with existing values
        messagebox.showinfo("Info", "Edit functionality - Similar to Add with pre-filled values")
    
    def delete_product(self):
        """Delete selected product"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            return
        
        product_id = int(self.tree.item(selected[0])['tags'][0])
        
        if self.product_manager.delete_product(product_id):
            messagebox.showinfo("Success", "Product deleted successfully")
            self.load_products()
        else:
            messagebox.showerror("Error", "Failed to delete product")
    
    def export_products(self):
        """Export products to CSV/Excel"""
        products = self.product_manager.get_all_products()
        
        if not products:
            messagebox.showwarning("Warning", "No products to export")
            return
        
        columns = ['sku', 'product_name', 'category_name', 'supplier_name', 
                  'unit_price', 'selling_price', 'stock_quantity', 'min_stock_level']
        
        filepath = DataExporter.export_to_excel(products, columns, 'products')
        
        if filepath:
            messagebox.showinfo("Success", f"Products exported to {filepath}")
        else:
            messagebox.showerror("Error", "Failed to export products")
    
    def import_products(self):
        """Import products from CSV/Excel"""
        messagebox.showinfo("Info", "Import functionality - Select CSV/Excel file to import products")
