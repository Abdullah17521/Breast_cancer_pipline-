import pandas as pd
import sqlalchemy as db

# 1. Database Connections
source_engine = db.create_engine(
    "mysql+pymysql://root:root@localhost:3306/ecommerce"
)
target_engine = db.create_engine(
    "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
)

# 2. Fetch Data Before Transformation (MySQL Source)
df_before = pd.read_sql("SELECT * FROM breast_cancer", con=source_engine)

# 3. Fetch Data After Transformation (PostgreSQL Target)
df_after = pd.read_sql(
    "SELECT * FROM transformed_breast_cancer", con=target_engine
)

# 4. Display Results
print("=" * 60)
print("              ETL DATA COMPARISON REPORT              ")
print("=" * 60)

print("\nBEFORE TRANSFORMATION (Source DB: MySQL)")
print(f"Total Row Count : {len(df_before)}")
print(f"Total Columns   : {df_before.shape[1]}")
print("\nSample Data (First 3 Rows):")
print(df_before.head(3))

print("\n" + "-" * 60)

print("\n AFTER TRANSFORMATION (Target DB: PostgreSQL)")
print(f"Total Row Count : {len(df_after)}")
print(f"Total Columns   : {df_after.shape[1]}")
print("\nSample Data (First 3 Rows):")
print(df_after.head(3))

print("=" * 60)