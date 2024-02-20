# #!/usr/bin/env python
# #
# # Small script to show PostgreSQL and Pyscopg together
# #

# # import psycopg2

# # try:
# #     conn = psycopg2.connect("dbname='myduka_db' user='postgres' host='localhost' password='Tony41943318' 'portid=5432'")
# # except:
# #     print("I am unable to connect to the database")

# # cur= conn.cursor()
# # cur.execute('''INSERT INTO public.products(
# # 	id, name, buying_price, selling_price, stock_quantity)
# # 	VALUES (6, 'chocolate', 100, 150,50);''')
# # conn.commit
# # rows=cur.fetchall()
# # print(rows)
import psycopg2


hostname = "localhost"
database = "myduka_db"
owner = "postgres"
password = "Tony41943318"
port_id = 5432

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = owner,
    password = password,
    port = port_id
)
# insert_script=('''INSERT INTO public.products(
# 	id, name, buying_price, selling_price, stock_quantity)
# 	VALUES (8, 'milk', 100, 200,50);''')
cur = conn.cursor()
# cur.execute(insert_script)
# #conn.commit

# cur.execute("select products.name,sales.quantity,sales.created_at from products join sales on products.id=sales.pid;")
# for records in cur.fetchall():
#     print(records)


def check_email_password(email,password):
        query ='''SELECT id, name 
	              FROM public.users
	              WHERE email =%s AND passwords =%s;'''
        cur.execute(query,(email,password))
        result =cur.fetchone()
        if result is not None:
              id=result[0]
              name=result[1]
              return id,name
        else:
              return None
        
conn.commit()


cur.execute('''SELECT products.name,sum(sales.quantity) as ts
FROM products
JOIN sales ON sales.pid= Products.id
group by products.name;
''')
for records in cur.fetchall():
       print(records)
conn.commit()

def sale_info():
    cur= conn.cursor()
    sales_info="""SELECT products.name,SUM(sales.quantity) AS total_sales
	FROM sales
	JOIN products ON products.id=sales.pid
	GROUP BY products.name;"""
    cur.execute(sales_info)
    info=cur.fetchall()
    print(info)
    return info

def sales_date():
    cur= conn.cursor()
    saless_date="""SELECT DATE (sales.created_at) as saledate ,SUM(sales.quantity * products.selling_price) AS total_sales
	FROM sales
	JOIN products ON products.id=sales.pid
	GROUP BY saledate
	order by Saledate;"""
    cur.execute(saless_date)
    info1=cur.fetchall()
    print(info1)
    return info1

def my_sale():
      conn.cursor()
total_sale='''SELECT products.name,sales.created_at,sum(sales.quantity *products.selling_price)as my_sale
from sales
join products on products.id=sales.pid
group by products.name,sales.created_at;'''
cur.execute(total_sale)

def my_profit():
      conn.cursor()
      profit='''SELECT products.name,products.id, sum(sales.quantity*(products.selling_price-products.buying_price))as total_profit
	FROM sales
	join products on products.id=sales.pid
	group by products.name , products.id;'''
      cur.execute(profit)
