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
A complete, production-ready Inventory Management System built with Python, Tkinter (GUI), and SQLite3 database. Features modular MVC architecture, secure authentication, CRUD operations, stock monitoring, and comprehensive reporting.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### Core Functionality
- 🔐 **Secure User Authentication** - Login system with role-based access (admin/user)
- 📦 **Product Management** - Complete CRUD operations for products with category and supplier linking
- 🏷️ **Category Management** - Organize products into categories
- 🏢 **Supplier Management** - Manage supplier information and contacts
- 💰 **Sales Tracking** - Record sales transactions with automatic stock updates
- 📥 **Purchase Management** - Track inventory purchases with stock replenishment
- 📊 **Dashboard** - Real-time overview with statistics and low stock alerts
- 📈 **Reports** - Comprehensive reporting for sales, purchases, stock, and product performance

### Technical Features
- **MVC Architecture** - Clean separation of Models, Views, and Controllers
- **SQLite Database** - Lightweight, file-based database (no server required)
- **Modular Design** - Easy to extend and maintain
- **Search & Filter** - Quick product search and filtering capabilities
- **Stock Alerts** - Automatic alerts for low stock items
- **Data Validation** - Input validation for all forms
- **User-Friendly UI** - Clean, intuitive Tkinter-based interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually included with Python)
- SQLite3 (included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/devranjeet/Inventory-Management-System.git
   cd Inventory-Management-System
   ```

2. **No additional dependencies needed!**
   This application uses only Python standard library modules.

3. **Run the application**
   ```bash
   python main.py
   ```

### First Login
- **Username:** `admin`
- **Password:** `admin123`

The database will be automatically created on first run with sample data.

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
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies (none required!)
├── README.md                    # This file
│
├── database/                    # Database layer
│   ├── schema.sql              # Database schema and initial data
│   ├── database_manager.py     # Database connection manager
│   └── inventory.db            # SQLite database (auto-created)
│
├── models/                      # Data models (MVC - Model)
│   ├── base_model.py           # Base model class
│   ├── user_model.py           # User data operations
│   ├── product_model.py        # Product data operations
│   ├── category_model.py       # Category data operations
│   ├── supplier_model.py       # Supplier data operations
│   ├── sale_model.py           # Sales data operations
│   └── purchase_model.py       # Purchase data operations
│
├── controllers/                 # Business logic (MVC - Controller)
│   ├── auth_controller.py      # Authentication logic
│   ├── product_controller.py   # Product business logic
│   ├── sales_controller.py     # Sales business logic
│   └── purchase_controller.py  # Purchase business logic
│
├── views/                       # User interface (MVC - View)
│   ├── login_view.py           # Login window
│   ├── main_window.py          # Main application window
│   ├── dashboard_view.py       # Dashboard with statistics
│   ├── products_view.py        # Product management UI
│   ├── categories_view.py      # Category management UI
│   ├── suppliers_view.py       # Supplier management UI
│   ├── sales_view.py           # Sales management UI
│   ├── purchases_view.py       # Purchase management UI
│   └── reports_view.py         # Reports generation UI
│
└── utils/                       # Utility functions
    └── helpers.py              # Helper functions and validators
```

## 🎯 Usage Guide

### Dashboard
- View real-time statistics for sales, purchases, and stock value
- Monitor low stock alerts
- Quick access to all modules

### Products
- **Add Product:** Click "Add Product" button, fill in details
- **Edit Product:** Double-click a product or select and click "Edit"
- **Delete Product:** Select a product and click "Delete"
- **Search:** Use the search box to filter products by name

### Categories & Suppliers
- Manage product categories and supplier information
- Edit and delete with validation (prevents deletion if linked to products)

### Sales
- **New Sale:** Click "New Sale", select product, enter quantity and customer info
- Stock automatically decrements after each sale
- View complete sales history

### Purchases
- **New Purchase:** Click "New Purchase", select product and supplier
- Stock automatically increments after each purchase
- Track purchase costs and suppliers

### Reports
- **Sales Reports:** View sales for 7, 30, or 90 days
- **Purchase Reports:** Track purchasing patterns
- **Stock Reports:** Low stock items and total stock value
- **Top Products:** Identify best-selling products

## 🗃️ Database Schema

### Tables
- **users** - User accounts and authentication
- **categories** - Product categories
- **suppliers** - Supplier information
- **products** - Product inventory with stock levels
- **sales** - Sales transactions
- **purchases** - Purchase transactions

### Key Features
- Foreign key relationships for data integrity
- Indexes for optimal query performance
- Automatic timestamps for all transactions
- Default admin user and sample data

## 🔧 Configuration

### Database Location
Default: `database/inventory.db`

To change the database location, edit `database/database_manager.py`:
```python
db_manager = DatabaseManager(db_path="your/custom/path/inventory.db")
```

### User Roles
- **admin** - Full access to all features
- **user** - Standard access (can be customized in code)

## 🌟 Future Enhancements

The modular architecture makes it easy to add new features:

- [ ] Barcode scanning integration
- [ ] Export reports to PDF/Excel
- [ ] Multi-user concurrent access
- [ ] Email notifications for low stock
- [ ] Advanced analytics and charts
- [ ] Mobile app integration via REST API
- [ ] Multi-location inventory support
- [ ] Product photos and attachments
- [ ] Purchase order management
- [ ] Customer management module

## 🛠️ Development

### Adding New Features

1. **Add a Model** - Create new model in `models/` extending `BaseModel`
2. **Add a Controller** - Create controller in `controllers/` for business logic
3. **Add a View** - Create view in `views/` for the UI
4. **Register in Main Window** - Add navigation in `views/main_window.py`

### Database Changes

1. Modify `database/schema.sql` for schema changes
2. Delete `database/inventory.db` to recreate (loses data)
3. Or write migration scripts for production systems

## 🐛 Troubleshooting

### "No module named 'tkinter'"
- **Windows/Mac:** Tkinter is usually included with Python
- **Linux:** Install with `sudo apt-get install python3-tk`

### Database is locked
- Close all other instances of the application
- Only one instance can write to the database at a time

### Application doesn't start
- Ensure Python 3.8 or higher is installed
- Check that all files are present in the correct structure
- Run from the project root directory

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
## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Authors

- **Ranjeet** - Initial work

## 🙏 Acknowledgments

- Built with Python's standard library - no external dependencies!
- SQLite for reliable, serverless database
- Tkinter for cross-platform GUI

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Python**
