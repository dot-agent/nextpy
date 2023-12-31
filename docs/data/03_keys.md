## Keys: Identifying Your Data

Now that you've built your first table in Nextpy, let's dive deeper into the crucial concept of **keys**, the essential tools for identifying and organizing your data within tables.

### Understanding Keys

Imagine your table as a filing cabinet containing folders for each record. Just like labels on those folders, keys help you quickly retrieve the specific information you need.

Nextpy offers two key types:

- **Primary Key:** This unique identifier ensures every record is unique. By default, Nextpy automatically generates an `id` column as the primary key.
- **Custom Keys:** You can choose another column as the primary key by setting the `primary_key=True` flag on that specific attribute in your model class. This is especially useful when the `id` doesn't represent the most logical identifier for your records.

**Why do we need keys?**

- **Unique Identification:** Keys prevent duplicate records and ensure efficient data retrieval.
- **Faster Queries:** Using the primary key as a reference point, Nextpy can quickly locate the exact data you need within your table.
- **Data Relationships:** Keys play a crucial role in establishing relationships between tables. Foreign keys reference primary keys to link and connect related data across your database.

### Customizing Keys

Let's say you're building a database for an online store. While the default `id` might work for products, it might not be the most intuitive key for customers. Here's how you can set a custom primary key using a "sku" (stock keeping unit) field:

```python
class Product(xt.Model, table=True):
    sku: str (primary_key=True)
    name: str
    price: float
    description: str
```

Remember, a custom key must be unique for each record.

### Advanced Key Options

For complex scenarios, Nextpy offers even more key flexibility:

- **Composite Keys:** Combine multiple columns to uniquely identify a record when a single field isn't sufficient.
- **Auto-incrementing Keys:** Define specific columns to automatically generate unique values upon record creation.

### Key Takeaways

- Keys are crucial for uniquely identifying and organizing data within your tables.
- Nextpy provides both automatic and customizable key options to suit your needs.
- Understanding and utilizing keys effectively unlocks efficient data retrieval and robust database relationships.
