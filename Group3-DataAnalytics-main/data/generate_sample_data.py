"""
Generate realistic retail transaction dataset for Consumer360
Creates CSV files for customers, products, and transactions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 200
NUM_TRANSACTIONS = 50000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

print("🚀 Generating Consumer360 Sample Dataset...")

# ===== GENERATE CUSTOMERS =====
print("📊 Generating customers...")

first_names = ['Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason', 'Isabella', 'William',
               'Mia', 'James', 'Charlotte', 'Benjamin', 'Amelia', 'Lucas', 'Harper', 'Henry', 'Evelyn', 'Alexander',
               'Abigail', 'Michael', 'Emily', 'Daniel', 'Elizabeth', 'Matthew', 'Sofia', 'Jackson', 'Avery', 'David',
               'Ella', 'Joseph', 'Scarlett', 'Samuel', 'Grace', 'Sebastian', 'Chloe', 'John', 'Victoria', 'Andrew']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
              'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson']

customers = []
for i in range(NUM_CUSTOMERS):
    customer_id = f"C{str(i+1).zfill(5)}"
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,999)}@email.com"
    phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    
    # Random acquisition date in the past 2 years
    days_ago = random.randint(0, 730)
    acquisition_date = END_DATE - timedelta(days=days_ago)
    
    gender = random.choice(['Male', 'Female', 'Other'])
    age = random.randint(18, 75)
    dob = datetime.now() - timedelta(days=age*365)
    
    customers.append({
        'customer_code': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'date_of_birth': dob.strftime('%Y-%m-%d'),
        'gender': gender,
        'acquisition_date': acquisition_date.strftime('%Y-%m-%d'),
        'customer_status': 'Active'
    })

df_customers = pd.DataFrame(customers)
print(f"✅ Generated {len(df_customers)} customers")

# ===== GENERATE PRODUCTS =====
print("📦 Generating products...")

categories = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera', 'Smartwatch', 'Speaker', 'Monitor'],
    'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 'Sneakers', 'Sweater', 'Shorts'],
    'Home': ['Blender', 'Coffee Maker', 'Vacuum', 'Toaster', 'Microwave', 'Air Purifier', 'Lamp', 'Bedding'],
    'Sports': ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Bicycle', 'Tennis Racket', 'Basketball', 'Resistance Bands'],
    'Food': ['Organic Coffee', 'Protein Powder', 'Granola', 'Olive Oil', 'Honey', 'Tea', 'Nuts', 'Chocolate']
}

brands = {
    'Electronics': ['Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'HP', 'Bose', 'Canon'],
    'Clothing': ['Nike', 'Adidas', 'Zara', 'H&M', 'Levi\'s', 'Gap', 'Uniqlo', 'Puma'],
    'Home': ['KitchenAid', 'Dyson', 'Philips', 'Cuisinart', 'Breville', 'Ninja', 'Instant Pot'],
    'Sports': ['Nike', 'Adidas', 'Under Armour', 'Reebok', 'Puma', 'New Balance', 'Lululemon'],
    'Food': ['Organic Valley', 'Whole Foods', 'Nature\'s Path', 'Bob\'s Red Mill', 'Clif Bar']
}

products = []
product_counter = 1
for category, items in categories.items():
    for item in items:
        for variant in range(random.randint(2, 5)):
            product_id = f"P{str(product_counter).zfill(5)}"
            brand = random.choice(brands.get(category, ['Generic']))
            
            # Price based on category
            if category == 'Electronics':
                price = round(random.uniform(50, 2000), 2)
            elif category == 'Clothing':
                price = round(random.uniform(15, 200), 2)
            elif category == 'Home':
                price = round(random.uniform(30, 500), 2)
            elif category == 'Sports':
                price = round(random.uniform(20, 300), 2)
            else:  # Food
                price = round(random.uniform(5, 50), 2)
            
            cost_price = round(price * random.uniform(0.4, 0.7), 2)
            
            products.append({
                'product_code': product_id,
                'product_name': f"{brand} {item} {variant+1}",
                'category': category,
                'subcategory': item,
                'brand': brand,
                'unit_price': price,
                'cost_price': cost_price,
                'supplier': f"Supplier_{random.randint(1,20)}",
                'is_active': True
            })
            product_counter += 1
            
            if product_counter > NUM_PRODUCTS:
                break
        if product_counter > NUM_PRODUCTS:
            break
    if product_counter > NUM_PRODUCTS:
        break

df_products = pd.DataFrame(products)
print(f"✅ Generated {len(df_products)} products")

# ===== GENERATE TRANSACTIONS =====
print("💳 Generating transactions...")

# Create customer purchase patterns (some buy more than others)
customer_weights = np.random.pareto(2, NUM_CUSTOMERS) + 1
customer_weights = customer_weights / customer_weights.sum()

transactions = []
transaction_counter = 1

for _ in range(NUM_TRANSACTIONS):
    # Select customer (weighted - some customers buy more)
    customer_idx = np.random.choice(NUM_CUSTOMERS, p=customer_weights)
    customer_code = df_customers.iloc[customer_idx]['customer_code']
    customer_acq_date = pd.to_datetime(df_customers.iloc[customer_idx]['acquisition_date'])
    
    # Transaction date must be after customer acquisition
    days_range = (END_DATE - customer_acq_date).days
    if days_range <= 0:
        continue
    
    transaction_date = customer_acq_date + timedelta(days=random.randint(0, days_range))
    
    # Select product
    product_idx = random.randint(0, len(df_products) - 1)
    product_code = df_products.iloc[product_idx]['product_code']
    unit_price = df_products.iloc[product_idx]['unit_price']
    
    # Quantity (most buy 1-2 items, rarely more)
    quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.3, 0.1, 0.07, 0.03])
    
    # Discount (20% chance of discount)
    discount_pct = random.choice([0, 0, 0, 0, 5, 10, 15, 20]) / 100
    discount_amount = round(unit_price * quantity * discount_pct, 2)
    
    # Tax (8%)
    subtotal = unit_price * quantity - discount_amount
    tax_amount = round(subtotal * 0.08, 2)
    total_amount = round(subtotal + tax_amount, 2)
    
    payment_method = random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash', 'Apple Pay'])
    
    # Store location
    store_code = f"STORE{random.randint(1, 10):03d}"
    
    transactions.append({
        'transaction_id': f"TXN{str(transaction_counter).zfill(8)}",
        'customer_code': customer_code,
        'product_code': product_code,
        'transaction_date': transaction_date.strftime('%Y-%m-%d'),
        'transaction_timestamp': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
        'quantity': quantity,
        'unit_price': unit_price,
        'discount_amount': discount_amount,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'payment_method': payment_method,
        'store_code': store_code
    })
    transaction_counter += 1

df_transactions = pd.DataFrame(transactions)
df_transactions = df_transactions.sort_values('transaction_timestamp')
print(f"✅ Generated {len(df_transactions)} transactions")

# ===== SAVE TO CSV =====
print("\n💾 Saving datasets to CSV...")

df_customers.to_csv('customers.csv', index=False)
print(f"✅ Saved customers.csv ({len(df_customers)} rows)")

df_products.to_csv('products.csv', index=False)
print(f"✅ Saved products.csv ({len(df_products)} rows)")

df_transactions.to_csv('transactions.csv', index=False)
print(f"✅ Saved transactions.csv ({len(df_transactions)} rows)")

# ===== GENERATE SUMMARY STATISTICS =====
print("\n📈 Dataset Summary:")
print(f"   Total Customers: {len(df_customers):,}")
print(f"   Total Products: {len(df_products):,}")
print(f"   Total Transactions: {len(df_transactions):,}")
print(f"   Date Range: {df_transactions['transaction_date'].min()} to {df_transactions['transaction_date'].max()}")
print(f"   Total Revenue: ${df_transactions['total_amount'].sum():,.2f}")
print(f"   Average Order Value: ${df_transactions['total_amount'].mean():.2f}")
print(f"   Unique Customers with Purchases: {df_transactions['customer_code'].nunique():,}")

print("\n✨ Dataset generation complete!")
print("📁 Files created: customers.csv, products.csv, transactions.csv")
