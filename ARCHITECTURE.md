# System Architecture

## Overview

The Inventory Management System follows a **Model-View-Controller (MVC)** architectural pattern with a clean separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          User Interface                          │
│                       (Tkinter - Views Layer)                    │
├─────────────────────────────────────────────────────────────────┤
│  LoginView  │  MainWindow  │  DashboardView  │  ProductsView    │
│  SalesView  │  PurchasesView  │  ReportsView  │  CategoriesView │
│  SuppliersView                                                   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ User Actions
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic                              │
│                    (Controllers Layer)                           │
├─────────────────────────────────────────────────────────────────┤
│  AuthController  │  ProductController  │  SalesController        │
│  PurchaseController                                              │
└──────────────────────┬──────────────────────────────────────────┘
                       │ Validated Operations
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                       Data Access                                │
│                      (Models Layer)                              │
├─────────────────────────────────────────────────────────────────┤
│  UserModel  │  ProductModel  │  CategoryModel  │  SupplierModel  │
│  SaleModel  │  PurchaseModel  │  BaseModel                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │ SQL Queries
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Database Manager                             │
│                  (database_manager.py)                           │
└──────────────────────┬──────────────────────────────────────────┘
                       │ SQLite Operations
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                      SQLite Database                             │
│                      (inventory.db)                              │
├─────────────────────────────────────────────────────────────────┤
│  users  │  products  │  categories  │  suppliers  │  sales       │
│  purchases                                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Interaction Flow

```
User Action → View → Controller → Model → Database
    ↑                                        │
    └────────────────────────────────────────┘
           Response (Display Results)
```

### 2. Example: Creating a Sale

```
1. User clicks "New Sale" in SalesView
2. SalesView displays dialog with form
3. User fills form and clicks "Complete Sale"
4. SalesView calls SalesController.create_sale()
5. SalesController validates inputs
6. SalesController calls SaleModel.create_sale()
7. SaleModel executes INSERT query
8. SaleModel calls ProductModel.update_stock()
9. Database updates both sales and products tables
10. Success message returns to SalesView
11. SalesView refreshes display
```

## Component Details

### Views Layer (UI)

**Purpose:** Present data to users and capture user input

**Components:**
- `LoginView` - Authentication interface
- `MainWindow` - Application shell with navigation
- `DashboardView` - Overview and statistics
- `ProductsView` - Product management interface
- `CategoriesView` - Category management
- `SuppliersView` - Supplier management
- `SalesView` - Sales transaction interface
- `PurchasesView` - Purchase transaction interface
- `ReportsView` - Report generation interface

**Technology:** Python Tkinter (standard library)

### Controllers Layer (Business Logic)

**Purpose:** Handle business rules, validation, and orchestration

**Components:**
- `AuthController` - User authentication and session management
- `ProductController` - Product business logic and validation
- `SalesController` - Sales transaction logic
- `PurchaseController` - Purchase transaction logic

**Responsibilities:**
- Input validation
- Business rule enforcement
- Error handling
- Orchestrating multiple model operations

### Models Layer (Data Access)

**Purpose:** Interact with database and manage data

**Components:**
- `BaseModel` - Common database operations
- `UserModel` - User data operations
- `ProductModel` - Product data operations
- `CategoryModel` - Category data operations
- `SupplierModel` - Supplier data operations
- `SaleModel` - Sales data operations
- `PurchaseModel` - Purchase data operations

**Responsibilities:**
- SQL query execution
- Data transformation (database rows to dictionaries)
- Database transactions

### Database Layer

**Purpose:** Persistent data storage

**Components:**
- `DatabaseManager` - Connection and query management
- `schema.sql` - Database structure definition

**Technology:** SQLite3 (file-based, serverless)

## Design Patterns

### 1. MVC Pattern

**Benefits:**
- Separation of concerns
- Easier testing
- Better maintainability
- Reusable components

### 2. Singleton Pattern

Used in `DatabaseManager` to ensure single database connection.

```python
_db_manager = None

def get_db_manager() -> DatabaseManager:
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
```

### 3. Repository Pattern

Models act as repositories for data access:

```python
class ProductModel(BaseModel):
    def get_all_products(self):
        # Encapsulates query logic
        pass
```

### 4. Template Method Pattern

`BaseModel` provides common functionality for all models:

```python
class BaseModel:
    def to_dict(self, row):
        # Common conversion logic
        pass
```

## Key Design Decisions

### 1. SQLite for Database

**Rationale:**
- No separate server needed
- Zero configuration
- Cross-platform
- Perfect for small to medium installations

**Trade-offs:**
- Single concurrent writer
- Not suitable for high-concurrency scenarios

### 2. Tkinter for UI

**Rationale:**
- Included with Python (no dependencies)
- Cross-platform
- Good for desktop applications
- Simple to use

**Trade-offs:**
- Not as modern as web interfaces
- Limited styling options

### 3. Plain Text Passwords

**Current State:** Passwords stored in plain text

**Production Recommendation:** Implement password hashing with bcrypt or similar:

```python
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### 4. Automatic Stock Updates

Sales and purchases automatically update stock levels through model layer:

```python
def create_sale(self, product_id, quantity, ...):
    # Insert sale
    success, sale_id = self.db.execute_update(...)
    
    if success:
        # Automatically update stock
        product_model.update_stock(product_id, -quantity)
```

## Security Considerations

### Current Implementation

1. **Authentication:** Basic username/password
2. **Session Management:** In-memory (single user)
3. **Password Storage:** Plain text (⚠️ not production-ready)
4. **SQL Injection:** Protected via parameterized queries
5. **File Access:** Database file permissions

### Production Recommendations

1. **Implement password hashing** (bcrypt, argon2)
2. **Add session timeouts**
3. **Implement audit logging**
4. **Add role-based permissions**
5. **Encrypt sensitive data**
6. **Regular security audits**

## Performance Considerations

### Current Optimizations

1. **Database Indexes:** On foreign keys and frequently queried columns
2. **Connection Reuse:** Single connection per operation
3. **Efficient Queries:** JOINs to reduce round trips
4. **Result Limits:** Default limits on list queries

### Scalability Options

For larger deployments:

1. **Database:** Migrate to PostgreSQL or MySQL
2. **Caching:** Add Redis for frequently accessed data
3. **API Layer:** Create REST API for multi-client support
4. **Load Balancing:** Multiple application instances
5. **Read Replicas:** For reporting queries

## Testing Strategy

### Current Tests

- Unit tests for models (database operations)
- Integration tests for controllers
- System tests for complete workflows

### Test Execution

```bash
python test_system.py
```

### Future Testing

- Automated UI tests (tkinter testing)
- Performance tests
- Security tests
- Stress tests

## Extension Points

### Adding New Entities

1. **Database:** Add table to `schema.sql`
2. **Model:** Create new model in `models/`
3. **Controller:** Create controller in `controllers/`
4. **View:** Create view in `views/`
5. **Navigation:** Update `main_window.py`

### Adding New Reports

1. Add method to appropriate model
2. Create report view or extend `ReportsView`
3. Add navigation button

### Adding External Integrations

Create new modules:
- `integrations/email_service.py`
- `integrations/barcode_scanner.py`
- `integrations/payment_gateway.py`

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.8+ |
| UI Framework | Tkinter | Standard Library |
| Database | SQLite | 3.x |
| Additional | None | Zero dependencies! |

## File Structure

```
Inventory-Management-System/
├── main.py                 # Entry point
├── database/
│   ├── schema.sql         # Database schema
│   └── database_manager.py # DB connection manager
├── models/                 # Data access layer
│   ├── base_model.py
│   ├── user_model.py
│   ├── product_model.py
│   ├── category_model.py
│   ├── supplier_model.py
│   ├── sale_model.py
│   └── purchase_model.py
├── controllers/           # Business logic layer
│   ├── auth_controller.py
│   ├── product_controller.py
│   ├── sales_controller.py
│   └── purchase_controller.py
├── views/                 # Presentation layer
│   ├── login_view.py
│   ├── main_window.py
│   ├── dashboard_view.py
│   ├── products_view.py
│   ├── categories_view.py
│   ├── suppliers_view.py
│   ├── sales_view.py
│   ├── purchases_view.py
│   └── reports_view.py
├── utils/                 # Helper functions
│   └── helpers.py
└── docs/                  # Documentation
    ├── README.md
    ├── SETUP.md
    ├── CONTRIBUTING.md
    ├── API.md
    └── ARCHITECTURE.md
```

## Conclusion

This architecture provides:
- ✓ Clean separation of concerns
- ✓ Easy maintenance and testing
- ✓ Extensibility for new features
- ✓ Clear data flow
- ✓ Minimal dependencies
- ✓ Cross-platform compatibility

The modular design allows developers to easily add new features without affecting existing functionality.
