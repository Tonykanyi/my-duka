from flask import Flask, render_template ,redirect,request,flash,session
import psycopg2
from mydb import check_email_password ,sale_info,sales_date
from flask_login import LoginManager,UserMixin,login_required,login_user,current_user



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
cur = conn.cursor()

app = Flask(__name__)

app.secret_key= "TonyKanyi"

login_manager = LoginManager(app)
login_manager.login_view='login'

 
class User(UserMixin):
    def __init__(self, user_id,email,password):
        self.id = user_id
        self.email=email
        self.password=password

@login_manager.user_loader
def load_user(user_id):
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()

    if user_data:
        # Create a User object based on the database data
        user = User(user_data[0], user_data[1], user_data[2])
        return user

    return None  # Return None if the user is not found

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/products")
# @login_required
def products():
    cur.execute('select * from products')
    prods=cur.fetchall()
    return render_template("add_products.html",prods=prods)
@app.route("/add-products",methods=["post"])
def add_products():
    products_name=request.form["name"]
    buying_price=request.form["Buying_price"]
    selling_price=request.form["Selling_price"]
    stock_quantity=request.form["Stock_quantity"]
    values=(products_name,buying_price,selling_price,stock_quantity)
    
    insert_query='''INSERT INTO products(
    name, buying_price, selling_price, stock_quantity)
	VALUES (%s, %s, %s, %s);'''

    cur.execute(insert_query,values)
    conn.commit()
    flash("product is added ")
    return redirect("/products")
@app.route("/my_products")
def my_products():
    return render_template("products.html")

@app.route("/sales")
@login_required
def sales():
    cur.execute('''SELECT sales.id,products.name,sales.created_at,sum(sales.quantity *products.selling_price)as my_sale
from sales
join products on products.id=sales.pid
group by products.name,sales.created_at,sales.id;''')
    sale=cur.fetchall()
    print(sale)

    
    cur.execute('select * from products')
    prods=cur.fetchall()
    return render_template("sales.html",sale=sale,prods=prods)

@app.route("/add-sales",methods=["post"])
def add_sales():
    product_id=request.form["pid"]
    quantity=request.form["quantity"]
    my_sale=(product_id,quantity)

    insert_sale='''INSERT INTO public.sales(
	 pid, quantity, created_at)
	VALUES (%s, %s, now());'''
    cur.execute(insert_sale,my_sale,)
    conn.commit()
    flash("sale is made" , 'success')
    return redirect("/sales")
@app.route("/register", methods=["post","get"])
def register():
    if request.method=='POST':
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        phone=request.form["phone"]
        country=request.form["country"]
        gender=request.form["gender"]
        register_as=request.form["register_as"]
       
        value=(name,email,password,phone,country,gender,register_as)
        insert_users='''INSERT INTO users(
        name, email, passwords,phone_number, country, gender,register_as)
        VALUES ( %s, %s, %s,%s, %s, %s,%s);'''
        cur.execute(insert_users,value)
        conn.commit()
    return render_template('register.html')

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        email =request.form['email']
        password =request.form['password']  
        cur.execute("SELECT * FROM users WHERE email = %s AND passwords = %s", (email, password))
        user_data = cur.fetchone()
        if user_data:
            user = load_user(user_data[0])
            login_user(user)
            flash("You are successfully logged in", 'success')
            return redirect('/dashboard')
        else:
            flash("Invalid email or password", 'danger')
            return redirect('/login')

    return render_template('login.html')
 
    #     # print(f"Attempting login with email: {email}, password: {password}")     
    #     account =check_email_password(email,password)
    #     # print(f"Login result: {account}")
    #     if account:
    #         flash("You are successfully login")
    #         return redirect('/dashboard')
        
    #     else:
    #         flash("invalid password")
    #         return redirect('/register')
        
    # return render_template('login.html')


@app.route('/dashboard')
@login_required                                
def dashboard():
    
    productss=[]
    total_saless=[]
    saless=[]
    mauzo_date=[]
    cur.execute('''SELECT products.name,products.id, sum(sales.quantity*(products.selling_price-products.buying_price))as total_profit
	FROM sales
	join products on products.id=sales.pid
	group by products.name , products.id;''')
    prof=cur.fetchall()

    for j in sales_date():
        saless.append(str(j[0]))
        mauzo_date.append(str(j[1]))
    for i in sale_info():
        productss.append(str(i[0]))
        total_saless.append(i[1])
        # user_id = current_user.get_id()
        # user = load_user(user_id)
        # print(current_user.is_authenticated)

    return render_template('dashboard.html',productss=productss,total_saless=total_saless,saless=saless,mauzo_date=mauzo_date,prof=prof)


conn.commit()            

app.run(debug=True)