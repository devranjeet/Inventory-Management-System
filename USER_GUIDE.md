# User Guide - Inventory Management System

## Table of Contents
1. [Getting Started](#getting-started)
2. [User Roles](#user-roles)
3. [Feature Guide](#feature-guide)
4. [Common Tasks](#common-tasks)
5. [Tips & Best Practices](#tips--best-practices)

## Getting Started

### First Time Setup

1. **Login**
   - Default username: `admin`
   - Default password: `admin123`
   - ⚠️ **Important:** Change default password after first login

2. **Initial Configuration**
   - Go to Settings
   - Configure company information
   - Set currency and tax rate
   - Adjust low stock threshold

3. **Add Basic Data**
   - Add categories for your products
   - Add supplier information
   - Create staff user accounts (Admin only)

## User Roles

### Administrator
Full system access including:
- User management
- System settings
- All features and reports
- Data backup and restore

### Staff
Limited access:
- Product management
- Sales processing
- Purchase entry
- Customer management
- Basic reports

## Feature Guide

### 1. Dashboard
The dashboard provides a quick overview of your business:
- Total products, customers, suppliers
- Today's and monthly sales
- Low stock alerts
- Out of stock notifications
- Outstanding payments

**Refresh:** Click the "Refresh Dashboard" button to update statistics

### 2. Product Management

#### Adding a Product
1. Click "Products" in the sidebar
2. Click "➕ Add Product"
3. Fill in required fields:
   - Product Name *
   - Category *
   - Supplier *
   - Unit Price * (purchase cost)
   - Selling Price *
   - Initial Stock Quantity
   - Minimum Stock Level (for alerts)
4. Optional: Add barcode and description
5. Click "Save Product"

**Note:** SKU is auto-generated

#### Searching Products
- Use the search bar to find products by:
  - Product name
  - SKU code
  - Barcode

#### Editing/Deleting Products
1. Select a product from the list
2. Click "✏️ Edit Product" or "🗑️ Delete Product"

#### Export Products
- Click "📤 Export" to save product list to Excel

### 3. Category Management

#### Adding a Category
1. Click "Categories" in the sidebar
2. Click "Add Category"
3. Enter category name and description
4. Save

**Note:** Categories with products cannot be deleted

### 4. Supplier Management

#### Adding a Supplier
1. Click "Suppliers" in the sidebar
2. Enter supplier details:
   - Name
   - Contact person
   - Phone and email
   - Address
3. Save

#### Tracking Outstanding Payments
- The system automatically tracks pending payments to suppliers
- View outstanding amounts in the supplier list

### 5. Purchase Management

#### Recording a Purchase
1. Click "Purchases" in the sidebar
2. Click "Add Purchase"
3. Select supplier
4. Add items to purchase:
   - Select product
   - Enter quantity
   - Enter unit price
5. Enter payment details:
   - Paid amount (can be partial)
   - Notes
6. Save

**Automatic Actions:**
- Invoice number is generated
- Stock is automatically updated
- Outstanding payment is calculated
- Stock history is recorded

### 6. Sales Management

#### Making a Sale
1. Click "Sales" in the sidebar
2. Click "New Sale"
3. Optional: Select customer
4. Add items to sale:
   - Select product
   - Enter quantity
   - Price is auto-filled
5. Apply tax and discount
6. Select payment method
7. Save

**Automatic Actions:**
- Invoice number is generated
- Stock is automatically deducted
- Customer loyalty points are awarded
- Stock history is recorded

**Stock Check:**
The system prevents overselling - you'll get an error if trying to sell more than available stock.

### 7. Customer Management

#### Adding a Customer
1. Click "Customers" in the sidebar
2. Click "Add Customer"
3. Enter customer details
4. Save

#### Loyalty Points
- Customers earn 1 point per ₹100 spent
- View loyalty points in customer details

### 8. Reports & Analytics

Available reports:
- **Sales Report:** Daily/monthly sales analysis
- **Purchase Report:** Supplier-wise purchases
- **Profit/Loss Report:** Financial analysis
- **Top Selling Products:** Best performers
- **Category Sales:** Category-wise breakdown
- **Expense Report:** Business expense tracking

#### Generating Reports
1. Click "Reports" in the sidebar
2. Select report type
3. Choose date range
4. Click "Generate Report"
5. Export to Excel if needed

### 9. Expense Management

#### Recording an Expense
1. Click "Expenses" in the sidebar
2. Click "Add Expense"
3. Enter:
   - Expense type (Rent, Utilities, Salaries, etc.)
   - Amount
   - Date
   - Description
4. Save

### 10. System Settings

#### Configuring Settings (Admin Only)
1. Click "Settings" in the sidebar
2. Modify:
   - Company information
   - Currency symbol
   - Tax rate (%)
   - Low stock threshold
3. Save changes

### 11. Data Backup

#### Creating a Backup (Admin Only)
1. Go to Settings
2. Click "Backup Database"
3. Backup is saved with timestamp in `backup/` folder

#### Restoring from Backup
1. Go to Settings
2. Click "Restore Database"
3. Select backup file
4. Confirm restoration

⚠️ **Warning:** Restoration will overwrite current data

## Common Tasks

### Daily Operations

1. **Start of Day**
   - Login to system
   - Check dashboard alerts
   - Review low stock items

2. **Process Sales**
   - Record each sale as it happens
   - Print invoices if needed
   - Track inventory automatically

3. **End of Day**
   - Review daily sales report
   - Check stock levels
   - Note any reorder requirements

### Weekly Tasks

1. Review top-selling products
2. Check outstanding supplier payments
3. Add new products as needed
4. Update product prices if necessary

### Monthly Tasks

1. Generate monthly sales report
2. Analyze profit/loss
3. Review and record all expenses
4. Create database backup
5. Review customer loyalty programs

## Tips & Best Practices

### Inventory Management

1. **Set Appropriate Min Stock Levels**
   - Consider lead time from suppliers
   - Account for sales velocity
   - Leave buffer for unexpected demand

2. **Regular Stock Audits**
   - Compare physical stock with system
   - Adjust discrepancies promptly
   - Use stock adjustment feature

3. **Product Organization**
   - Use clear, consistent naming
   - Categorize products logically
   - Add detailed descriptions

### Financial Management

1. **Record All Transactions**
   - Enter sales immediately
   - Record purchases promptly
   - Don't forget expenses

2. **Monitor Profit Margins**
   - Review profit/loss reports regularly
   - Adjust pricing if needed
   - Identify low-margin products

3. **Track Payments**
   - Monitor outstanding supplier payments
   - Follow up on pending payments
   - Maintain good supplier relationships

### Data Security

1. **Regular Backups**
   - Create backups daily or weekly
   - Store backups in safe location
   - Test restore process occasionally

2. **User Management**
   - Use strong passwords
   - Create staff accounts as needed
   - Remove inactive users

3. **Access Control**
   - Give appropriate permissions
   - Admin access only for trusted users
   - Monitor system usage

### System Performance

1. **Database Maintenance**
   - Keep database size reasonable
   - Archive old data if needed
   - Backup before major changes

2. **Data Quality**
   - Avoid duplicate products
   - Keep supplier info updated
   - Verify product details regularly

## Troubleshooting

### Common Issues

**Issue:** Cannot login
- **Solution:** Check username and password, contact admin

**Issue:** Low stock alert not showing
- **Solution:** Check min stock level in product settings

**Issue:** Sale fails with "insufficient stock"
- **Solution:** Check current stock, update if needed

**Issue:** Export not working
- **Solution:** Ensure pandas and openpyxl are installed

**Issue:** Barcode generation fails
- **Solution:** Check python-barcode installation

## Support

For additional help:
1. Check the main README.md
2. Review demo.py for examples
3. Open an issue on GitHub

## Keyboard Shortcuts

- `Enter` on login form → Submit login
- Search boxes update results on typing
- Use Tab to navigate between form fields

## Data Export Formats

- **Excel (.xlsx):** Full formatting, recommended for reports
- **CSV (.csv):** Plain text, universal compatibility

## Security Notes

- Database file (`inventory.db`) contains all data
- Keep database file secure
- Regular backups are essential
- Change default passwords immediately
- Use strong passwords for all users

---

**Last Updated:** November 2024
**Version:** 1.0.0
