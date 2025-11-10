# Contributing to Inventory Management System

Thank you for your interest in contributing! This guide will help you extend and improve the system.

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a new branch for your feature
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Code Structure and Architecture

### MVC Pattern

The application follows the Model-View-Controller (MVC) pattern:

```
Models (models/) ──────> Database (SQLite)
    ↑                         ↑
    │                         │
Controllers (controllers/) ──┘
    ↑
    │
Views (views/) ──────> User Interface (Tkinter)
```

### Adding New Features

#### 1. Adding a New Model

Create a new file in `models/` that extends `BaseModel`:

```python
# models/new_feature_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, Any

class NewFeatureModel(BaseModel):
    """Model for new feature operations"""
    
    def get_all(self) -> list:
        """Get all items"""
        query = "SELECT * FROM new_table ORDER BY id"
        results = self.db.execute_query(query)
        return self.to_dict_list(results)
    
    def create(self, name: str, description: str) -> tuple:
        """Create new item"""
        query = "INSERT INTO new_table (name, description) VALUES (?, ?)"
        success, item_id = self.db.execute_update(query, (name, description))
        return success, item_id
```

#### 2. Adding a New Controller

Create a new file in `controllers/`:

```python
# controllers/new_feature_controller.py
from models.new_feature_model import NewFeatureModel

class NewFeatureController:
    """Controller for new feature operations"""
    
    def __init__(self):
        self.model = NewFeatureModel()
    
    def get_all_items(self) -> list:
        """Get all items"""
        return self.model.get_all()
    
    def create_item(self, name: str, description: str) -> tuple:
        """Create item with validation"""
        if not name or not name.strip():
            return False, "Name is required"
        
        return self.model.create(name, description)
```

#### 3. Adding a New View

Create a new file in `views/`:

```python
# views/new_feature_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.new_feature_controller import NewFeatureController

class NewFeatureView:
    """View for new feature"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.controller = NewFeatureController()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create view widgets"""
        # Add your UI components here
        pass
    
    def load_data(self):
        """Load data"""
        items = self.controller.get_all_items()
        # Populate your UI with data
    
    def refresh(self):
        """Refresh view"""
        self.load_data()
```

#### 4. Register in Main Window

Add navigation in `views/main_window.py`:

```python
# In create_widgets() method, add to nav_buttons list:
("New Feature", self.show_new_feature),

# Add method to show the view:
def show_new_feature(self):
    """Show new feature view"""
    self.clear_content()
    from views.new_feature_view import NewFeatureView
    self.current_view = NewFeatureView(self.content_frame, self.auth_controller)
```

## Database Changes

### Adding a New Table

1. Update `database/schema.sql`:

```sql
-- New table
CREATE TABLE IF NOT EXISTS new_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index if needed
CREATE INDEX IF NOT EXISTS idx_new_table_name ON new_table(name);
```

2. Delete existing database (loses data) or write migration:

```bash
rm database/inventory.db
python main.py  # Recreates database with new schema
```

### Migration Strategy (for production)

For production systems with existing data:

```python
# migrations/001_add_new_table.py
def migrate_up(db):
    """Apply migration"""
    db.execute_update("""
        CREATE TABLE IF NOT EXISTS new_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def migrate_down(db):
    """Rollback migration"""
    db.execute_update("DROP TABLE IF EXISTS new_table")
```

## Coding Standards

### Python Style Guide (PEP 8)

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all classes and methods

```python
def example_method(self, param1: str, param2: int) -> bool:
    """
    Brief description of what the method does
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    # Implementation
    pass
```

### Type Hints

Use type hints for better code documentation:

```python
from typing import Optional, List, Dict, Any, Tuple

def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
    """Get item by ID"""
    pass
```

### Error Handling

Always handle errors gracefully:

```python
try:
    result = some_operation()
except Exception as e:
    print(f"Error in operation: {e}")
    return False, f"Operation failed: {str(e)}"
```

## Testing

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Feature works as expected
- [ ] No errors in console
- [ ] Database operations complete successfully
- [ ] UI is responsive and user-friendly
- [ ] Edge cases are handled
- [ ] Existing features still work

### Testing Database Operations

```python
# Test in Python console
from models.your_model import YourModel

model = YourModel()

# Test create
success, item_id = model.create("Test", "Description")
print(f"Created: {success}, ID: {item_id}")

# Test read
item = model.get_by_id(item_id)
print(f"Retrieved: {item}")

# Test update
success = model.update(item_id, "Updated", "New description")
print(f"Updated: {success}")

# Test delete
success = model.delete(item_id)
print(f"Deleted: {success}")
```

## UI Guidelines

### Consistent Layout

Use the same layout pattern as existing views:

```python
# Title
title_label = ttk.Label(self.frame, text="View Title", font=('Arial', 18, 'bold'))
title_label.pack(pady=(0, 10))

# Toolbar
toolbar = ttk.Frame(self.frame)
toolbar.pack(fill=tk.X, pady=(0, 10))

# Buttons
ttk.Button(toolbar, text="Action", command=self.action).pack(side=tk.LEFT, padx=(0, 5))

# Content area (usually a Treeview)
tree_frame = ttk.Frame(self.frame)
tree_frame.pack(fill=tk.BOTH, expand=True)
```

### Dialog Windows

Use consistent dialog patterns:

```python
class MyDialog:
    def __init__(self, parent, callback=None):
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Dialog Title")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()  # Modal dialog
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add your form fields here
        
        # Buttons at the bottom
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
```

## Common Patterns

### Validation Pattern

```python
from utils.helpers import validate_positive_number, validate_email

def validate_form(self):
    """Validate form inputs"""
    name = self.name_var.get().strip()
    
    if not name:
        messagebox.showerror("Error", "Name is required")
        return False
    
    valid, price = validate_positive_number(self.price_var.get(), "Price")
    if not valid:
        messagebox.showerror("Error", price)
        return False
    
    return True
```

### Treeview Pattern

```python
# Create treeview
columns = ('ID', 'Name', 'Value')
self.tree = ttk.Treeview(frame, columns=columns, show='headings')

# Configure columns
self.tree.heading('ID', text='ID')
self.tree.column('ID', width=80, anchor=tk.CENTER)

# Populate data
for item in items:
    self.tree.insert('', tk.END, values=(
        item['id'],
        item['name'],
        item['value']
    ))
```

## Pull Request Guidelines

### Before Submitting

1. Test your changes thoroughly
2. Update documentation if needed
3. Ensure code follows style guidelines
4. Add comments for complex logic
5. Check that existing features still work

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation

## Testing Done
- [ ] Manual testing
- [ ] Database operations verified
- [ ] UI tested
- [ ] Edge cases tested

## Screenshots (if UI changes)
[Add screenshots here]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## Feature Ideas

Looking for ideas? Here are some features that would be valuable:

### High Priority
- [ ] Password hashing for security
- [ ] Export reports to PDF/CSV
- [ ] Email notifications for low stock
- [ ] Product search with filters
- [ ] Barcode scanning support

### Medium Priority
- [ ] Multi-user session management
- [ ] Advanced analytics and charts
- [ ] Backup/restore functionality
- [ ] Product images
- [ ] Purchase orders workflow

### Low Priority
- [ ] REST API for mobile apps
- [ ] Multi-location support
- [ ] Customer management
- [ ] Invoice generation
- [ ] Dark mode theme

## Questions?

- Check existing code for examples
- Read the main [README.md](README.md)
- Open an issue for discussion
- Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the project

Thank you for contributing to make this project better! 🎉
