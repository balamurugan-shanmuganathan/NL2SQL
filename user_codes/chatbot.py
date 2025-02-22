import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
import duckdb
import kagglehub
import re
import pandas as pd
import os

# Load LLM
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
model_name=Gemini(id="gemini-2.0-flash-exp", temperature=0)

def load_dataset():
    path=kagglehub.dataset_download("andrexibiza/grocery-sales-dataset")
    categories = pd.read_csv(path + "/categories.csv")
    cities = pd.read_csv(path + "/cities.csv")
    countries = pd.read_csv(path + "/countries.csv")
    customers = pd.read_csv(path + "/customers.csv")
    employees =  pd.read_csv(path + "/employees.csv")
    products = pd.read_csv(path + "/products.csv")
    sales = pd.read_csv(path + "/sales.csv", nrows=50000)

    con = duckdb.connect("sales.db")
    # Store DataFrames as tables in DuckDB
    con.execute("CREATE TABLE IF NOT EXISTS categories AS SELECT * FROM categories")
    con.execute("CREATE TABLE IF NOT EXISTS cities AS SELECT * FROM cities")
    con.execute("CREATE TABLE IF NOT EXISTS countries AS SELECT * FROM countries")
    con.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM customers")
    con.execute("CREATE TABLE IF NOT EXISTS employees AS SELECT * FROM employees")
    con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM products")
    con.execute("CREATE TABLE IF NOT EXISTS sales AS SELECT * FROM sales")

    con.execute("UPDATE sales SET TotalPrice =CAST(FLOOR((RANDOM() % 7500) * 4 + 4) AS INTEGER)")
    con.close()
    print("Data is successfully Loaded..")


def run_sql_query(sql):
    con = duckdb.connect("sales.db")
    result = con.execute(sql).df()
    con.close()
    return result

def get_tablenames():
    con = duckdb.connect("sales.db")
    # Get all table names
    tables = con.execute("SHOW TABLES").df()["name"].tolist()
    tables_dict = {}
    # Retrieve column names for each table
    for table in tables:
        columns = con.execute(f"DESCRIBE {table}").df()["column_name"].tolist()
        tables_dict[table] = columns  # Store in dictionary
    con.close()
    return tables_dict

def sql_code_generator(user_query, tables_names):
    agent = Agent(
        name='Sql Agent',
        model=model_name,
        description="You are senior sql developer.",
        instructions=[
            "Convert user query in to SQL questions",
            "Use this table information to generate your code"
            f"Table Details {tables_names}"
        ],
        show_tool_calls=True,
        debug_mode=True

    )

    response=agent.run(user_query)
    response=re.sub(r"```sql\s*|\s*```", "", response.content.strip())

    return response