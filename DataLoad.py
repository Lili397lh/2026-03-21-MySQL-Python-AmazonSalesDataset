import pandas as pd
import os
from sqlalchemy import create_engine, text

# ----MySQL connection----
engine = create_engine("mysql+pymysql://root:INTRODUCE_PASSWORD@localhost/amazon_sales")

# ----CSV load----
DIR=os.path.dirname(os.path.abspath(__file__))
csv_path=os.path.join(DIR,'amazon.csv')
if not os.path.exists(csv_path):
    print(f"{csv_path} not found. Must be downloaded in Kaggle")
    exit()

df=pd.read_csv(csv_path)
print("Loading CSV...")

# Create 'id'
df['id'] = range(1, len(df) + 1)

# ----Filtering----
df['discounted_price']=df['discounted_price'].str.lstrip('₹').str.replace(',','', regex=False)
df['discounted_price']=pd.to_numeric(df['discounted_price'].astype(float), errors='coerce')/100
df['actual_price']=df['actual_price'].str.lstrip('₹').str.replace(',','', regex=False)
df['actual_price']=pd.to_numeric(df['actual_price'].astype(float), errors='coerce')/100
df['discount_percentage']=df['discount_percentage'].str.rstrip('%').str.replace(',','', regex=False)
df['rating_count']=df['rating_count'].str.replace(',','', regex=False)
df['rating_count']=df['rating_count']
df['rating_count']=pd.to_numeric(df['rating_count'].astype(float), errors='coerce')
df['rating']=df['rating'].str.replace('|','', regex=False)
df['rating']=pd.to_numeric(df['rating'], errors='coerce')

#Reviews and users data extration
dfreview=df.copy()
dfreview['user_id'] = dfreview['user_id'].str.split(',')
dfreview['review_id'] = dfreview['review_id'].str.split(',')

mask = (dfreview['user_id'].str.len() == dfreview['review_id'].str.len())
dfreview = dfreview[mask]

dfreview = dfreview.explode(['user_id', 'review_id'])

# Category processing
dfcategory = df[['category']].copy()
dfcategory['main_category'] = dfcategory['category'].str.split('|').str[0]
dfcategory['final_subcategory'] = dfcategory['category'].str.split('|').str[-1]
dfcategory['full_category'] = dfcategory['main_category'] + ' | ' + dfcategory['final_subcategory']

dfunique_categories = dfcategory[['full_category', 'main_category', 'final_subcategory']].drop_duplicates().reset_index(drop=True)
dfunique_categories.index = dfunique_categories.index + 1
dfunique_categories = dfunique_categories.reset_index().rename(columns={'index': 'category_id'})

df['main_category'] = df['category'].str.split('|').str[0]
df['final_subcategory'] = df['category'].str.split('|').str[-1]
df['full_category'] = df['main_category'] + ' | ' + df['final_subcategory']

df = df.merge(dfunique_categories[['category_id', 'full_category']], on='full_category', how='left')

# ----Final data frames to load----
df_categories = dfunique_categories.rename(
    columns={
        "category_id": "categoryid",
        "main_category": "maincategory",
        "final_subcategory": "finalsubcategory",
    }
)[["categoryid", "maincategory", "finalsubcategory"]]
df_products = df.rename(
    columns={
        "id": "id",
        "product_id": "productid",
        "product_name": "productname",
        "category_id": "categoryid",
        "main_category": "maincategory",
        "final_subcategory": "finalsubcategory",
        "actual_price": "actualprice",
        "discounted_price": "discountedprice",
        "discount_percentage": "discount",
        "img_link": "imglink",
        "product_link": "productlink",
    }
)[
    [
        "id",
        "productid",
        "productname",
        "categoryid",
        "maincategory",
        "finalsubcategory",
        "actualprice",
        "discountedprice",
        "discount",
        "imglink",
        "productlink",
    ]
]
df_users = pd.DataFrame(dfreview["user_id"].unique(), columns=["userid"]).drop_duplicates(subset="userid")
df_reviews = dfreview.rename(
    columns={
        "review_id": "reviewid",
        "id": "product_id_fk",
        "user_id": "userid",
        "rating": "rating",
        "rating_count": "ratingcount",
    }
)[["reviewid", "product_id_fk", "userid", "rating", "ratingcount"]]

# Delete data in tables
with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    conn.execute(text("TRUNCATE TABLE reviews"))
    conn.execute(text("TRUNCATE TABLE products"))
    conn.execute(text("TRUNCATE TABLE users"))
    conn.execute(text("TRUNCATE TABLE categories"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))

# Load data
df_categories.to_sql("categories", con=engine, if_exists="append", index=False)
df_products.to_sql("products", con=engine, if_exists="append", index=False)
df_users.to_sql("users", con=engine, if_exists="append", index=False)
df_reviews.to_sql("reviews", con=engine, if_exists="append", index=False)

'''# Activate FK
with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))'''

print("Data loading complete")