from config import DB_PATH
import duckdb

def main():
    import pandas as pd
    
    df = pd.read_csv("data/global_fuel_prices_2020_2026.csv")

    df.columns = [c.lower() for c in df.columns]

    if "country" not in df.columns:
        df["country"] = "GLOBAL"

    con = duckdb.connect(str(DB_PATH))

    con.execute("DROP TABLE IF EXISTS raw_fuel")
    con.execute("CREATE TABLE raw_fuel AS SELECT * FROM df")

    print("raw_fuel loaded into DuckDB")


if __name__ == "__main__":
    main()