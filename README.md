# Inventory Management System

A comprehensive Inventory Management System built with Python, Tkinter (GUI), and SQLite3 database. This system provides complete inventory tracking, sales management, purchase management, and business analytics.

## 🌟 Features

### 1. **User Management**
- ✅ Login/Logout System with secure authentication
- ✅ Role-based Access Control (Admin & Staff)
- ✅ Password Encryption using bcrypt
- ✅ User account management

### 2. **Product Management**
- ✅ Add, Update, Delete Products
- ✅ Product Search (by name, SKU, or barcode)
- ✅ Auto-generated SKU codes
- ✅ Stock tracking with real-time updates
- ✅ Product categorization
- ✅ Supplier association

### 3. **Category Management**
- ✅ Add, Edit, Delete Categories
- ✅ Category-wise product filtering
- ✅ Product count per category

### 4. **Supplier Management**
- ✅ Supplier information management
- ✅ Purchase history tracking
- ✅ Outstanding payment tracking
- ✅ Contact management

### 5. **Purchase Management**
- ✅ Purchase entry with invoice generation
- ✅ Automatic stock updates on purchase
- ✅ Multiple items per purchase
- ✅ Payment tracking (Paid, Partial, Pending)
- ✅ Purchase history

### 6. **Sales Management**
- ✅ Sales entry and billing
- ✅ Invoice generation with unique invoice numbers
- ✅ Automatic stock deduction
- ✅ Tax and discount calculations
- ✅ Customer association
- ✅ Multiple payment methods

### 7. **Stock Tracking**
- ✅ Real-time stock view
- ✅ Low stock alerts
- ✅ Out-of-stock notifications
- ✅ Stock history tracking
- ✅ Stock value calculation

### 8. **Reports & Analytics**
- ✅ Daily/Monthly sales reports
- ✅ Purchase reports
- ✅ Profit/Loss analysis
- ✅ Top selling products
- ✅ Category-wise sales reports
- ✅ Supplier purchase reports
- ✅ Dashboard with key metrics

### 9. **Barcode/SKU System**
- ✅ Auto-generated product SKU codes
- ✅ Barcode generation support
- ✅ Barcode-based product search

### 10. **Expense & Accounting**
- ✅ Business expense tracking
- ✅ Expense categorization
- ✅ Date-wise expense reports
- ✅ Basic ledger functionality

### 11. **Data Backup & Restore**
- ✅ SQLite database backup system
- ✅ Restore from backup functionality
- ✅ Timestamped backups

### 12. **System Settings**
- ✅ Currency settings
- ✅ Tax rate configuration
- ✅ Discount settings
- ✅ Low stock threshold
- ✅ Company information

### 13. **Customer Management**
- ✅ Customer information storage
- ✅ Purchase history tracking
- ✅ Loyalty points system
- ✅ Customer search

### 14. **Export/Import Features**
- ✅ Export data to Excel/CSV
- ✅ Product import from CSV
- ✅ Report generation

### 15. **Dashboard Overview**
- ✅ Key metrics display
- ✅ Real-time alerts
- ✅ Stock status overview
- ✅ Sales statistics

## 📋 Requirements

- Python 3.8 or higher
- tkinter (usually comes with Python)
- SQLite3 (built-in with Python)
- bcrypt
- pandas
- openpyxl
- python-barcode
- Pillow

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/devranjeet/Inventory-Management-System.git
cd Inventory-Management-System
```

2. Install system dependencies (if needed):
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On macOS
brew install python-tk

# On Windows
# tkinter comes pre-installed with Python
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the application:
```bash
python3 main.py
```

### Default Login Credentials

- **Username:** admin
- **Password:** admin123

**⚠️ Important:** Change the default password after first login!

## 📁 Project Structure

```
Inventory-Management-System/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── models/            # Data models
│   │   ├── database.py    # Database management
│   │   ├── user.py        # User management
│   │   ├── product.py     # Product management
│   │   ├── category.py    # Category management
│   │   ├── supplier.py    # Supplier management
│   │   ├── purchase.py    # Purchase management
│   │   ├── sales.py       # Sales management
│   │   ├── customer.py    # Customer management
│   │   ├── expense.py     # Expense management
│   │   ├── reports.py     # Reports and analytics
│   │   └── settings.py    # System settings
│   ├── views/             # GUI views
│   │   ├── login_view.py
│   │   ├── main_view.py
│   │   ├── dashboard_view.py
│   │   ├── products_view.py
│   │   ├── categories_view.py
│   │   ├── suppliers_view.py
│   │   ├── purchases_view.py
│   │   ├── sales_view.py
│   │   ├── customers_view.py
│   │   ├── reports_view.py
│   │   ├── expenses_view.py
│   │   ├── settings_view.py
│   │   └── users_view.py
│   └── utils/             # Utility modules
│       ├── barcode_gen.py # Barcode generation
│       └── data_utils.py  # Data export/import
├── reports/               # Generated reports
├── backup/                # Database backups
└── inventory.db           # SQLite database (auto-created)
```

## 🔒 Security Features

- **Password Hashing:** All passwords are hashed using bcrypt
- **Role-Based Access:** Admin and Staff roles with different permissions
- **Data Validation:** Input validation on all forms
- **SQL Injection Prevention:** Parameterized queries throughout

## 📊 Database Schema

The system uses SQLite3 with the following main tables:
- users
- categories
- suppliers
- products
- purchases & purchase_items
- sales & sale_items
- customers
- expenses
- settings
- stock_history

## 🎯 Key Functionalities

### For Administrators:
- Full system access
- User management
- System settings configuration
- Data backup and restore
- Complete reports access

### For Staff:
- Product management
- Sales processing
- Purchase entry
- Customer management
- Basic reports

## 🛠️ Development

### Running Tests
```bash
python3 -m pytest tests/
```

### Code Structure
The application follows MVC (Model-View-Controller) pattern:
- **Models:** Handle data and business logic
- **Views:** Tkinter GUI components
- **Controllers:** Implicitly handled within views

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🎉 Acknowledgments

- Built with Python and Tkinter
- Uses SQLite for lightweight database management
- Inspired by modern inventory management systems

## 📈 Future Enhancements

- Web-based interface using Flask
- Multi-store support
- Advanced analytics and forecasting
- Mobile app integration
- Cloud backup support
- Email notifications
- Automated reordering
- Barcode scanner integration

---

**Made with ❤️ for efficient inventory management**
