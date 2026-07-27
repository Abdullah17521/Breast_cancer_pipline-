from datetime import datetime
import numpy as np
import pandas as pd
import sqlalchemy as db

overall_start = datetime.now()

engine = db.create_engine("mysql+pymysql://root:root@localhost:3306/ecommerce")

query = "SELECT * FROM breast_cancer"

chunks_generator = pd.read_sql(query, con=engine, chunksize=100)

print("Starting ETL Process in Chunks of 100...\n")

batch_no = 1
is_first_chunk = True

for df_chunk in chunks_generator:

    df_chunk.columns = (
        df_chunk.columns.str.strip().str.lower().str.replace(" ", "_")
    )

    df_chunk["tumor_size"] = pd.to_numeric(
        df_chunk["tumor_size"], errors="coerce"
    ).fillna(0)
    df_chunk["age"] = pd.to_numeric(df_chunk["age"], errors="coerce").fillna(0)

    text_cols = df_chunk.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df_chunk[col] = df_chunk[col].astype(str).str.strip().str.upper()

    df_chunk = df_chunk.replace(["NAN", "NONE", "NULL", ""], np.nan)
    conditions = [df_chunk["age"] > 60, df_chunk["age"] >= 40]
    choices = ["SENIOR", "MIDDLE"]
    df_chunk["age_group"] = np.select(conditions, choices, default="YOUNG")
    df_chunk["is_high_risk"] = (
        (df_chunk["tumor_size"] > 20) | (df_chunk["age"] > 60)
    ).astype(int)
    df_chunk = df_chunk.drop_duplicates()
    mode = "replace" if is_first_chunk else "append"
    df_chunk.to_sql(
        "transformed_breast_cancer",
        con=engine,
        if_exists=mode,
        index=False,
    )

    is_first_chunk = False
    print(
        f"Batch {batch_no}: 100 rows Transformed & Saved to DB successfully!"
    )
    batch_no += 1

overall_end = datetime.now()
print(
    "\nETL Pipeline Execution Completed! Total Time:",
    overall_end - overall_start,
)

print("\n--- Sample Transformed Data (First 5 Rows) ---")
df_verified = pd.read_sql(
    "SELECT age, age_group, tumor_size, is_high_risk, status FROM transformed_breast_cancer LIMIT 5",
    con=engine,
)
print(df_verified)
