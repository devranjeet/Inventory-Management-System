"""
Suppliers View - Manage suppliers
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.supplier_model import SupplierModel
from utils.helpers import validate_email, validate_phone


class SuppliersView:
    """View for managing suppliers"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.model = SupplierModel()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_suppliers()
    
    def create_widgets(self):
        """Create suppliers view widgets"""
        # Title
        title_label = ttk.Label(self.frame, text="Suppliers", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Supplier", command=self.add_supplier).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Edit Supplier", command=self.edit_supplier).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Delete Supplier", command=self.delete_supplier).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Refresh", command=self.load_suppliers).pack(side=tk.LEFT)
        
        # Suppliers treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Contact', 'Email', 'Phone')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Supplier Name')
        self.tree.heading('Contact', text='Contact Person')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Phone', text='Phone')
        
        self.tree.column('ID', width=60, anchor=tk.CENTER)
        self.tree.column('Name', width=200)
        self.tree.column('Contact', width=150)
        self.tree.column('Email', width=200)
        self.tree.column('Phone', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_supplier())
    
    def load_suppliers(self):
        """Load all suppliers"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        suppliers = self.model.get_all_suppliers()
        for supplier in suppliers:
            self.tree.insert('', tk.END, values=(
                supplier.get('supplier_id', ''),
                supplier.get('supplier_name', ''),
                supplier.get('contact_person', ''),
                supplier.get('email', ''),
                supplier.get('phone', '')
            ))
    
    def add_supplier(self):
        """Open dialog to add new supplier"""
        SupplierDialog(self.frame, self.model, callback=self.load_suppliers)
    
    def edit_supplier(self):
        """Open dialog to edit selected supplier"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a supplier to edit")
            return
        
        item = self.tree.item(selection[0])
        supplier_id = item['values'][0]
        supplier = self.model.get_supplier_by_id(supplier_id)
        
        if supplier:
            SupplierDialog(self.frame, self.model, supplier=supplier, callback=self.load_suppliers)
    
    def delete_supplier(self):
        """Delete selected supplier"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a supplier to delete")
            return
        
        item = self.tree.item(selection[0])
        supplier_id = item['values'][0]
        supplier_name = item['values'][1]
        
        # Check if supplier has products
        count = self.model.get_products_count(supplier_id)
        if count > 0:
            messagebox.showerror("Error", f"Cannot delete supplier. It has {count} products.")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{supplier_name}'?"):
            success = self.model.delete_supplier(supplier_id)
            if success:
                messagebox.showinfo("Success", "Supplier deleted successfully")
                self.load_suppliers()
            else:
                messagebox.showerror("Error", "Failed to delete supplier")
    
    def refresh(self):
        """Refresh suppliers list"""
        self.load_suppliers()


class SupplierDialog:
    """Dialog for adding/editing suppliers"""
    
    def __init__(self, parent, model, supplier=None, callback=None):
        self.model = model
        self.supplier = supplier
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Supplier" if supplier else "Add Supplier")
        self.dialog.geometry("500x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        if supplier:
            self.populate_fields()
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Supplier name
        ttk.Label(main_frame, text="Supplier Name:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, pady=5)
        
        # Contact person
        ttk.Label(main_frame, text="Contact Person:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.contact_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.contact_var, width=40).grid(row=1, column=1, pady=5)
        
        # Email
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.email_var, width=40).grid(row=2, column=1, pady=5)
        
        # Phone
        ttk.Label(main_frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.phone_var, width=40).grid(row=3, column=1, pady=5)
        
        # Address
        ttk.Label(main_frame, text="Address:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.address_text = tk.Text(main_frame, width=30, height=4)
        self.address_text.grid(row=4, column=1, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def populate_fields(self):
        """Populate fields with supplier data"""
        self.name_var.set(self.supplier.get('supplier_name', ''))
        self.contact_var.set(self.supplier.get('contact_person', ''))
        self.email_var.set(self.supplier.get('email', ''))
        self.phone_var.set(self.supplier.get('phone', ''))
        self.address_text.insert('1.0', self.supplier.get('address', ''))
    
    def save(self):
        """Save supplier"""
        name = self.name_var.get().strip()
        contact = self.contact_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_text.get('1.0', tk.END).strip()
        
        if not name:
            messagebox.showerror("Error", "Supplier name is required")
            return
        
        if email and not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        if phone and not validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone format")
            return
        
        if self.supplier:
            success = self.model.update_supplier(
                self.supplier['supplier_id'], name, contact, email, phone, address
            )
        else:
            success, _ = self.model.create_supplier(name, contact, email, phone, address)
        
        if success:
            messagebox.showinfo("Success", "Supplier saved successfully")
            self.dialog.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Error", "Failed to save supplier")
