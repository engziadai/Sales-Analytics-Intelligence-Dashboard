import pandas as pd
import re

# Load the raw dataset
# Note: Using the filename from your snippet
df = pd.read_excel('Dashboard_Dataset_Before.xlsx')

# 1. Standardize Dates (Keep a copy to check fixes)
raw_dates = df['Date'].copy()
df['Date'] = pd.to_datetime(df['Date'], dayfirst=False, errors='coerce', format='mixed')
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
date_fixes = (raw_dates != df['Date']).sum()

# 2. Handle Missing Values
status_fixes = df['Status'].isnull().sum()
df['Status'] = df['Status'].fillna('Pending')

price_fixes = df['Price'].isnull().sum()
df['Price'] = df['Price'].fillna(df['Price'].median())

# 3. Clean Customer_Name and count fixes
def clean_name(name):
    if isinstance(name, str):
        # Remove special characters/numbers using RE
        cleaned = re.sub(r'[^a-zA-Z\s]', '', name).strip().title()
        return cleaned
    return name

raw_names = df['Customer_Name'].copy()
df['Customer_Name'] = df['Customer_Name'].apply(clean_name)
name_fixes = (raw_names != df['Customer_Name']).sum()

# 4. Recalculate Total_Amount for reliability
df['Total_Amount'] = df['Price'] * df['Quantity']

# 5. Clean Product_Category
raw_cats = df['Product_Category'].copy()
df['Product_Category'] = df['Product_Category'].str.strip().str.title()
cat_fixes = (raw_cats != df['Product_Category']).sum()

# 6. Remove unnecessary columns (Notes AND Transaction_ID)
# We drop the first column 'Transaction_ID' as requested
cols_to_drop = ['Transaction_ID', 'Notes']
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

# 7. Save to CSV
# Using the standard name we'll use in the dashboard
output_file = 'Dashboard_Dataset_After.csv'
df.to_csv(output_file, index=False)

# --- CLEANING REPORT ---
print("-" * 30)
print("CLEANING SUMMARY REPORT")
print("-" * 30)
print(f"Total Rows Processed: {len(df)}")
print(f"Date format fixes:    {date_fixes}")
print(f"Customer Name fixes:  {name_fixes}")
print(f"Category name fixes:  {cat_fixes}")
print(f"Missing Status filled: {status_fixes}")
print(f"Missing Price filled:  {price_fixes}")
print("-" * 30)
print(f"File '{output_file}' is ready!")