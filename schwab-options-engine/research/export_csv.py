import sqlite3
import pandas as pd
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
for table in ["option_snapshots", "contract_features", "ticker_scores", "alerts"]:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    out = f"{table}.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out} ({len(df)} rows)")
