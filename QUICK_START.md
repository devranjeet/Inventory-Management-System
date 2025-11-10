# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/devranjeet/Inventory-Management-System.git
cd Inventory-Management-System

# Install dependencies (if not already installed)
pip install bcrypt pandas openpyxl python-barcode
```

### Step 2: Run Demo (1 minute)

```bash
python3 demo.py
```

This will:
- Create a demo database
- Add sample categories, suppliers, products
- Record sample purchases and sales
- Generate reports
- Create a backup

### Step 3: Run Tests (1 minute)

```bash
python3 tests/test_system.py
```

Expected output: `Ran 8 tests in 0.707s - OK ✅`

### Step 4: Start Application (1 minute)

```bash
python3 main.py
```

**Login with:**
- Username: `admin`
- Password: `admin123`

---

## 📱 Main Features Access

After logging in:

| Feature | Click | What You Can Do |
|---------|-------|-----------------|
| **Dashboard** | 🏠 Dashboard | View key metrics, alerts |
| **Products** | 📦 Products | Add, edit, search products |
| **Categories** | 🗂️ Categories | Manage product categories |
| **Suppliers** | 🏷️ Suppliers | Manage supplier info |
| **Purchases** | 📥 Purchases | Record new purchases |
| **Sales** | 📤 Sales | Process sales & billing |
| **Customers** | 👥 Customers | Manage customer info |
| **Reports** | 📊 Reports | Generate analytics |
| **Expenses** | 💰 Expenses | Track business expenses |
| **Settings** | ⚙️ Settings | Configure system |

---

## ✏️ Common Tasks

### Adding a Product

1. Click **📦 Products**
2. Click **➕ Add Product**
3. Fill in:
   - Product Name
   - Select Category
   - Select Supplier
   - Unit Price (what you pay)
   - Selling Price (what you charge)
   - Initial Stock
4. Click **Save**

**Note:** SKU is auto-generated!

### Recording a Sale

1. Click **📤 Sales**
2. Click **New Sale**
3. Add items to cart
4. Apply tax/discount
5. Select payment method
6. Click **Save**

**Auto Actions:**
- Invoice generated
- Stock deducted
- Customer points added

### Checking Low Stock

1. Go to **🏠 Dashboard**
2. View "Low Stock Items" count
3. Or click **📦 Products**
4. Check products with red indicators

### Generating Reports

1. Click **📊 Reports**
2. Select report type:
   - Sales Report
   - Purchase Report
   - Profit/Loss
   - Top Products
3. Choose date range
4. Click **Generate**
5. Export to Excel if needed

### Creating Backup

1. Click **⚙️ Settings** (Admin only)
2. Click **Backup Database**
3. Backup saved in `backup/` folder

---

## 🎯 Key Points

### Auto-Generated Items
- ✅ Product SKU codes
- ✅ Purchase invoice numbers (PUR-...)
- ✅ Sales invoice numbers (INV-...)

### Automatic Actions
- ✅ Stock increases on purchase
- ✅ Stock decreases on sale
- ✅ Outstanding payment tracking
- ✅ Loyalty points calculation

### Real-Time Alerts
- ⚠️ Low stock warnings
- ❌ Out of stock alerts
- ⏰ Payment reminders

---

## 📋 Default Data

### Default Admin User
- **Username:** admin
- **Password:** admin123
- **Role:** Administrator

### Sample Data (after demo.py)
- 4 Categories
- 3 Suppliers
- 5 Products
- 3 Customers
- Sample transactions

---

## 🔧 Troubleshooting

**Issue:** Login fails  
**Fix:** Use admin/admin123, check console for errors

**Issue:** Database not created  
**Fix:** Check write permissions in current directory

**Issue:** Import errors  
**Fix:** Run `pip install -r requirements.txt`

---

## 📚 Learn More

- **Full Guide:** See [USER_GUIDE.md](USER_GUIDE.md)
- **API Docs:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **README:** See [README.md](README.md)

---

## 💡 Pro Tips

1. **Change default password** immediately
2. **Create regular backups** of database
3. **Set appropriate min stock levels** for alerts
4. **Use search feature** for quick product lookup
5. **Export reports** for external analysis

---

**Ready to explore? Launch the app:**
```bash
python3 main.py
```

🎉 Happy inventory managing!
