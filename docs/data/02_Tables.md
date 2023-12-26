## Tables

### Understanding Tables:

- **Structured Data Storage:** Tables are the heart of any database, providing a structured way to organize and store data.
- **Think Spreadsheet:** Think of a table as a spreadsheet like Excel or Google Sheets with rows and columns:
  - Each **row** represents a unique record or entity (e.g., a customer, product, or order).
  - Each **column** represents a specific piece of information about that record (e.g., customer name, product price, order date).

### Creating Tables in Nextpy:

1. **Define a Python Class:**
   - Use a Python class to define the structure of your table.
   - Inherit from the `xt.Model` base class provided by Nextpy.
   - Set the `table=True` argument within the class declaration to signal that it should be mapped to a database table.
2. **Specify Columns:**
   - Declare class attributes to represent the columns of your table.
   - Nextpy automatically maps common Python data types to corresponding SQL column types.

### Example:

#### Python

```python
from nextpy import xt

class Product(xt.Model, table=True):
    id: int  # Primary key (automatically generated)
    name: str
    price: float
    description: str  # Optional field
```

### Key Points:

- **Primary Key:** Every table requires a primary key column to uniquely identify each record. By default, Nextpy creates an `id` column as the primary key.
- **Optional Fields:** You can include optional fields that may not always have values for every record.
