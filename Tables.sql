/* Create the database */
CREATE DATABASE  IF NOT EXISTS amazon_sales;

/* Select the amazon_sales database */
USE amazon_sales;

CREATE TABLE categories (
categoryid int,
maincategory varchar(255) NOT NULL,
finalsubcategory varchar(255) NOT NULL,
PRIMARY KEY (categoryid)
);

/* Create the tables */
CREATE TABLE products (
id INT PRIMARY KEY,
productid varchar(10) NOT NULL,
productname text NOT NULL,
categoryid int,
maincategory varchar(255),
finalsubcategory varchar(255),
actualprice decimal(10,2),
discountedprice decimal(10,2),
discount int,
imglink varchar(255),
productlink varchar(255),
FOREIGN KEY (categoryid) REFERENCES categories (categoryid)
);

CREATE TABLE users (
userid varchar(255),
PRIMARY KEY (userid)
);

CREATE TABLE reviews (
reviewid varchar(255),
product_id_fk INT NOT NULL,
userid varchar(255),
rating decimal(10,1),
ratingcount int,
PRIMARY KEY (reviewid, product_id_fk),
FOREIGN KEY (product_id_fk) REFERENCES products (id),
FOREIGN KEY (userid) REFERENCES users (userid)
);