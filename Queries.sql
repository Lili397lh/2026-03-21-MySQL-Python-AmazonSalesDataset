/* Create and select the database */
CREATE DATABASE  IF NOT EXISTS amazon_sales;
USE amazon_sales;

/*Products with maximum discount by main category*/
WITH max_disc AS (
SELECT 
c.maincategory, max(p.discount) AS maxdiscount
FROM 
products p
JOIN categories c 
	ON p.categoryid=c.categoryid
GROUP BY
c.maincategory
)

SELECT DISTINCT
c.maincategory, c.finalsubcategory, p.productid, p.discount
FROM products p
JOIN categories c 
	ON p.categoryid=c.categoryid
JOIN max_disc m
	ON p.maincategory=m.maincategory
	AND p.discount=m.maxdiscount;

/*Top 10 of products in rating for each main category*/
SELECT t.maincategory, t.productid, t.AVGrating
FROM (
	SELECT
	c.maincategory, 
    p.productid, 
    AVG(r.rating) AS AVGrating, 
    ROW_NUMBER() OVER (
		PARTITION BY c.maincategory
        ORDER BY AVG(r.rating) DESC
	) AS rn
	FROM reviews r
	JOIN products p
		ON r.product_id_fk=p.id
	JOIN categories c 
		ON p.categoryid=c.categoryid
	GROUP BY c.maincategory, p.productid
) t
WHERE t.rn <=10
ORDER BY t.maincategory, t.AVGrating DESC;

/*Top 3 of main categories with more reviews*/
SELECT
c.maincategory, SUM(r.ratingcount) AS sumratingcount
FROM reviews r
JOIN products p
	ON r.product_id_fk=p.id
JOIN categories c
	ON p.categoryid=c.categoryid
GROUP BY c.maincategory
ORDER BY sumratingcount DESC
LIMIT 3;

/*Top 5 of users with more reviews by category*/
SELECT t.maincategory, t.userid, t.COUNTreviewid
FROM (
	SELECT
	c.maincategory, 
    u.userid, 
    COUNT(r.reviewid) AS COUNTreviewid, 
    ROW_NUMBER() OVER (
		PARTITION BY c.maincategory
        ORDER BY AVG(r.reviewid) DESC
	) AS rn
	FROM reviews r
	JOIN products p
		ON r.product_id_fk=p.id
	JOIN categories c 
		ON p.categoryid=c.categoryid
	JOIN users u
		ON r.userid=u.userid
	GROUP BY c.maincategory, u.userid
) t
WHERE t.rn <=5
ORDER BY t.maincategory, t.COUNTreviewid DESC;

/*Products with rating > 4.5 by subcategory*/
SELECT DISTINCT
p.productid, r.rating, c.finalsubcategory
FROM products p
JOIN reviews r
	ON r.product_id_fk=p.id
JOIN categories c
	ON p.categoryid=c.categoryid
WHERE r.rating >= 4.5
ORDER BY c.finalsubcategory,r.rating DESC;

/*Total reviews, mean rating and mean discount by main category*/
SELECT
c.maincategory, COUNT(r.reviewid), AVG(r.rating), AVG(p.discount)
FROM products p
JOIN reviews r
	ON r.product_id_fk=p.id
JOIN categories c
	ON p.categoryid=c.categoryid
GROUP BY c.maincategory
ORDER BY c.maincategory;