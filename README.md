# Amazon Sales Dataset Analysis

Loads and analyzes "Amazon sales dataset" from Kaggle using MySQL and Python. It is created MySQL database, with Python is extracted the CSV data, cleaned and nomralized and runs 6 analytical SQL queries.

## Relations Diagram

-	‘categories’ -> ‘products’ (1:N): ‘categoryid’
-	‘products’ -> ‘reviews’ (1:N): ‘id’
-	‘users’ -> ‘reviews’ (1:N): ‘userid’

## Files

- 'Tables.sql': Creates DB/tables with relationships
- 'DataLoad.py': Loads amazon.csv, extracts, cleans data and inserts into the MySQL DB
- 'Queries.sql': 6 analytical queries

## Setup & Execution

1. Prerequisites:
- MySQL Workbrench
- Python 3.x
- pip install pandas pymysql sqlalchemy os

2. Download Dataset:
   1. Download amazon.csv from Kaggle (https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)
   2. Place amazon.csv in same folder as DataLoad.py

3. Run:
   1. MySQL Workbrench: Execute 'Tables.sql'
   2. Edit DataLoad.py line 6:
   engine = create_engine("mysql+pymysql://root:INTRODUCE_PASSWORD@localhost/amazon_sales")

   Replace INTRODUCE_PASSWORD with your root password
   3. Execute DataLoad.py
   4. MySQL Workbrench: Execute 'Queries.sql'

## Author

Liliana Lain Huditian - Data Analyst.
