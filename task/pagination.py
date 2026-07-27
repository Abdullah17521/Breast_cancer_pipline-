from datetime import datetime
import pandas as pd
import sqlalchemy as db

overall_start = datetime.now()
print("Process Started At:", overall_start.strftime("%Y-%m-%d %H:%M:%S"))

engine = db.create_engine("mysql+pymysql://root:root@localhost:3306/ecommerce")

query = "SELECT COUNT(*) as count FROM breast_cancer"

print("\n--- Counting Total Records in 'breast_cancer' Table ---\n")
total_records = pd.read_sql(query, con=engine)
print(f"Total records in 'breast_cancer' table: {total_records.iloc[0]['count']}")

chunks_generator = pd.read_sql(query, con=engine, chunksize=100)

print("\n--- Processing and Writing Data in Chunks of 100 ---\n")

batch_no = 1
is_first_chunk = True

for df_chunk in chunks_generator:
    chunk_start = datetime.now()

    print(f"--- Processing Batch {batch_no} ---")
    print(f"Rows in this chunk: {len(df_chunk)}")

    mode = "replace" if is_first_chunk else "append"

    df_chunk.to_sql("processed_data", con=engine, if_exists=mode, index=False)

    is_first_chunk = False

    chunk_end = datetime.now()
    print(
        f"Batch {batch_no} written successfully in {chunk_end - chunk_start} seconds."
    )
    print("-" * 50)

    batch_no += 1

overall_end = datetime.now()
print("\nProcess Ended At:", overall_end.strftime("%Y-%m-%d %H:%M:%S"))
print("Total Time Taken:", overall_end - overall_start)
print(
    "\nData processing completed! All records stored in 'processed_data' table."
)

print("\nVerifying written data (First 100 rows from 'processed_data'):\n")
verified_df = pd.read_sql(
    "SELECT * FROM processed_data LIMIT 100", con=engine
)
print(verified_df)