# Setup and Installation Guide

This guide will walk you through setting up and running the Inventory Management System.

## Prerequisites

### Required Software
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Tkinter** - Usually included with Python
- **SQLite3** - Included with Python (no installation needed)

### Checking Your Python Installation

Open a terminal/command prompt and run:
```bash
python --version
# or
python3 --version
```

You should see Python 3.8 or higher.

### Checking Tkinter Installation

```bash
python -m tkinter
# or
python3 -m tkinter
```

A small window should appear. If it doesn't, you need to install Tkinter.

#### Installing Tkinter (if needed)

**Ubuntu/Debian Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL Linux:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
Tkinter is included with Python from python.org. If using Homebrew:
```bash
brew install python-tk
```

**Windows:**
Tkinter is included with Python from python.org.

## Installation Steps

### Step 1: Download the Project

**Option A: Using Git**
```bash
git clone https://github.com/devranjeet/Inventory-Management-System.git
cd Inventory-Management-System
```

**Option B: Download ZIP**
1. Download the ZIP file from GitHub
2. Extract it to a folder of your choice
3. Open terminal/command prompt in that folder

### Step 2: Verify Installation

Check that all required files are present:
```bash
# On Windows
dir

# On Linux/Mac
ls -la
```

You should see:
- `main.py`
- `database/` folder
- `models/` folder
- `controllers/` folder
- `views/` folder
- `utils/` folder
- `README.md`
- `requirements.txt`

### Step 3: Run the Application

```bash
python main.py
# or
python3 main.py
```

The application should start, showing the login window.

## First Run

### Default Login Credentials
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Important:** Change the default password after first login in a production environment.

### What Happens on First Run

1. The application creates a `database/inventory.db` file
2. Database schema is initialized with tables for users, products, categories, etc.
3. Default admin user is created
4. Sample categories and suppliers are added

## Troubleshooting

### "No module named 'tkinter'" Error

**Windows/Mac:**
- Reinstall Python from [python.org](https://python.org) (make sure to check "tcl/tk" during installation)

**Linux:**
- Install tkinter package (see "Installing Tkinter" above)

### "Database is locked" Error

- Close all other instances of the application
- Only one instance can write to the database at a time
- If the error persists, delete `database/inventory.db` and restart (you'll lose all data)

### Application Window Doesn't Appear

1. Check if Python is running in the background (Task Manager/Activity Monitor)
2. Try running with `-v` flag for verbose output:
   ```bash
   python -v main.py
   ```
3. Check for error messages in the terminal

### "Permission denied" Error

**Linux/Mac:**
```bash
chmod +x main.py
python3 main.py
```

### Port Already in Use (if using Flask version)

This Tkinter version doesn't use network ports, so this shouldn't be an issue.

## Running in a Virtual Environment (Optional)

Using a virtual environment is a good practice:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Run the application
python main.py

# When done, deactivate:
deactivate
```

## Database Management

### Database Location
The SQLite database is stored at: `database/inventory.db`

### Backing Up Your Data
Simply copy the `inventory.db` file to a safe location:
```bash
cp database/inventory.db database/inventory_backup.db
```

### Resetting the Database
To start fresh (⚠️ **This will delete all your data**):
```bash
# On Windows:
del database\inventory.db

# On Linux/Mac:
rm database/inventory.db
```

Then restart the application - a new database will be created with default data.

### Viewing Database Contents
You can use any SQLite browser like:
- [DB Browser for SQLite](https://sqlitebrowser.org/) (Free, GUI)
- Command line: `sqlite3 database/inventory.db`

## Configuration

### Changing Database Location

Edit `database/database_manager.py`:
```python
def __init__(self, db_path: str = "your/custom/path/inventory.db"):
```

### Adding New Users

You can add users through the application (admin functionality) or directly in the database:
```sql
INSERT INTO users (username, password, full_name, role) 
VALUES ('newuser', 'password123', 'New User', 'user');
```

⚠️ **Note:** In production, implement proper password hashing!

## Performance Tips

1. **Regular backups** - Backup your database file regularly
2. **Don't run multiple instances** - Only run one instance of the app at a time
3. **Close properly** - Always close the application properly to avoid database locks
4. **Monitor database size** - SQLite can handle large databases, but performance may degrade with millions of records

## Security Recommendations

For production use:

1. **Change default credentials** immediately
2. **Implement password hashing** (current version uses plain text)
3. **Add password complexity requirements**
4. **Implement session timeouts**
5. **Add audit logging** for all transactions
6. **Regular backups** with encryption
7. **File permissions** - Restrict access to database file

## Getting Help

If you encounter issues:

1. Check this SETUP guide
2. Read the main [README.md](README.md)
3. Check [GitHub Issues](https://github.com/devranjeet/Inventory-Management-System/issues)
4. Open a new issue with:
   - Your OS and Python version
   - Complete error message
   - Steps to reproduce the issue

## Next Steps

Once the application is running:

1. Log in with default credentials
2. Explore the dashboard
3. Add some products, categories, and suppliers
4. Try recording sales and purchases
5. Generate reports

See the main [README.md](README.md) for detailed usage instructions.

## Uninstallation

To completely remove the application:

1. Delete the entire project folder
2. If using a virtual environment, delete the `venv` folder

That's it! No system files are modified outside the project folder.
