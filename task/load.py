import pandas as pd
import sqlalchemy as db
from transform import df_chunk

# Driver name corrected to postgresql+psycopg2
target_engine = db.create_engine(
    "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
)

df_chunk.to_sql(
    "transformed_breast_cancer",
    con=target_engine,
    if_exists="append",
    index=False,
)

print("Data loaded into target database successfully!")
test=pd.read_sql("SELECT * FROM transformed_breast_cancer LIMIT 5", con=target_engine)
print(test)
