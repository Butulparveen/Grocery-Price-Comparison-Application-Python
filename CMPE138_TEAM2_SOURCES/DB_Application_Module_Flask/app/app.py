#SJSU CMPE 138 Fall 2021 TEAM_2
from enum import IntEnum
from os import abort
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#importing the module 
import logging 

#now we will Create and configure logger 
logging.basicConfig(filename="std.log", 
					format=' %(name)s - %(levelname)s - %(message)s', 
					filemode='w') 

#Let us Create an object 
logger=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

#some messages to test
logger.debug("Testing Debug Log") 
logger.info("Testing Info Log") 
logger.warning("Testing Warning Log") 
logger.error("Testing Error Log") 
logger.critical("Testing critical Log") 




app = Flask(__name__)


app.secret_key = 'db180b'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Prequel@321'
app.config['MYSQL_DB'] = 'team2_app'

mysql = MySQL(app)



def get_max_cust_id():
    with app.app_context():
        mycursor1 = mysql.connection.cursor()
        mycursor1.execute("SELECT MAX(cust_id) FROM customer")
        max_id = mycursor1.fetchone()
    return max_id[0]
def get_next_cust_id():
    max_id = get_max_cust_id()
    return 'C'+str(int(max_id[1:])+1)


def get_max_sl_id():
    with app.app_context():
        mycursor3 = mysql.connection.cursor()
        mycursor3.execute("SELECT MAX(shopping_list_id) FROM Shopping_list")
        max_id = mycursor3.fetchone()
    return max_id[0]

def get_next_sl_id():
    max_id = get_max_sl_id()
    return 'SL'+str(int(max_id[2:])+1)

def get_item_details(): 
    with app.app_context():
        mycursor2 = mysql.connection.cursor()
        mycursor2.execute("SELECT * FROM item")
        item_details = mycursor2.fetchall()
    return item_details

def get_item_quantity(item_id,sl_id):
    with app.app_context():
        mycursor4 = mysql.connection.cursor()
        mycursor4.execute("SELECT quantity FROM Contains WHERE item_id = %s and shopping_list_id=%s",(item_id,sl_id))
        quantity = mycursor4.fetchone()
    return quantity[0]
#print(get_item_quantity('IT1001','SL1001'))

def get_max_order_id():
    with app.app_context():
        mycursor5 = mysql.connection.cursor()
        mycursor5.execute("SELECT MAX(order_id) FROM Orders")
        max_id = mycursor5.fetchone()
        if not(max_id[0]):
            return 'OR1000'
    return max_id[0]

def get_next_order_id():
    max_id = get_max_order_id()
    return 'OR'+str(int(max_id[2:])+1)
#print(get_next_order_id())

def create_order(order_id,sl_id,payment_mode):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Orders (order_id,sl_id,payment_mode) VALUES (%s,%s,%s)",(order_id,sl_id,payment_mode))
        mysql.connection.commit()
    return "created"

def create_new_order(order_id,sl_id,payment_mode):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Orders (order_id,sl_id,payment_mode) VALUES (%s,%s,%s)",(order_id,sl_id,payment_mode))
        mysql.connection.commit()
    return "created"

def checkInt(str):
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()

def update_offer(price,quantity_in_stock,item_id,store_id):
    with app.app_context():
        cursorn = mysql.connection.cursor()
        cursorn.execute("UPDATE Offers SET price = %s, quantity_in_stock = %s WHERE item_id =%s and store_id=%s",(price,quantity_in_stock,item_id,store_id))
        mysql.connection.commit()
    return "updated"


external_offering_dict = {}

@app.route('/')
def home():  
    return "hello, welcome to our website"
    
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('select  * from Customer where cust_ID=%s and cust_password=sha1(%s)', (username, password ))
        customer_details = cursor.fetchone()
        print(customer_details)
        if customer_details:
            session['loggedin'] = True
            session['id'] = customer_details['cust_ID']
            session['username'] = customer_details['cust_Name']
            session['sl_id']=""
            msg = 'Logged in successfully !'
            items = get_item_details()
           
            return redirect(url_for('home_api'))
            
        else:
            msg = 'Incorrect username / password !'
            logger.error('Login Failed for Customer'+username)
    return render_template('login.html', msg = msg)


@app.route('/m_login', methods =['GET', 'POST'])
def m_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        m_username = request.form['username']
        m_password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select  * from Authorized_person where m_id=%s and m_password=sha1(%s)', (m_username, m_password ))
        m_details = cursor.fetchone()
        #print(m_details)
        m_store_id=m_details['store_id']
        #print(m_store_id)
        inventory_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        inventory_cursor.execute('select  * from Offers where store_id=%s', (m_store_id, ))
        inventory_details = inventory_cursor.fetchall()
        #print(inventory_details)
 
        print(m_store_id)
        if m_details:
            session['loggedin'] = True
            session['m_id'] = m_details['m_id']
            session['m_store_id']=m_store_id
            msg = 'Logged in successfully !'
          
           
            return render_template('manager_home.html', msg = msg,m_details=m_details,m_store_id=m_store_id,inventory_details=inventory_details)
            #return render_template('items.html', msg = msg,items=items)
        else:
            msg = 'Incorrect username / password !'
    return render_template('manager_login.html', msg = msg)


@app.route('/logout')
def logout():
    logger.info('Logout Successful for Customer'+session['username'])
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/m_logout')
def m_logout():
    logger.info('Logout Successful for Manager'+session['m_id'])
    session.pop('loggedin', None)
    session.pop('m_id', None)
    session.pop('m_username', None)
    session.pop('m_store_id', None)
    return redirect(url_for('m_login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'cust_Name' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form and 'cust_street' in request.form and 'cust_city' in request.form and 'cust_state' in request.form and 'cust_zip' in request.form:
        print("test")
        username = request.form['cust_Name']
        password = request.form['password']
        phone_num=request.form['phone']
        email = request.form['email']
        street = request.form['cust_street']
        city = request.form['cust_city']
        state = request.form['cust_state']
        zipcode = request.form['cust_zip']
       

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customer WHERE cust_Name = % s', (username, ))
        Customer = cursor.fetchone()
        logger.info("Customer Details are as follows:\n"+Customer)
        if Customer:
            msg = 'Customer already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not phone_num or not street or not city or not state or not zip:
            msg = 'Please fill out the form !'
        else:
            new_cust_id = get_next_cust_id()
            
            cursor.execute('INSERT INTO Customer VALUES (%s,%s, sha1(%s), %s,%s, %s, %s, % s,%s)',
             (new_cust_id,username, password,phone_num,email,street,zipcode,city,state) )
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            logger.info('Registration Successful for Customer'+username)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        logger.error('Registration Failed for Customer')
    return render_template('register.html', msg = msg)


@app.route('/update_inventory', methods =['GET', 'POST'])
def update_inventory():
    if session['loggedin'] == True:
        msg = ''
        logger.info('Update Inventory Page accessed by Customer'+session['m_id'])
        if request.method == 'POST' and 'price' in request.form and 'quantity_in_stock' in request.form:
            price = request.form['price']
            quantity_in_stock = request.form['quantity_in_stock']
            item_id = request.form['item_id']
            store_id=session['m_store_id']
            res=update_offer(price,quantity_in_stock,item_id,store_id)
            print(res)
            logger.info('Update Inventory Successful for Manager'+session['m_id']+ ".")
            
            msg = item_id+' updated successfully !'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select  * from Authorized_person where m_id=%s', (session['m_id'],))
            m_details = cursor.fetchone()
          

            inventory_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            inventory_cursor.execute('select  * from Offers where store_id=%s', (session['m_store_id'], ))
            inventory_details = inventory_cursor.fetchall()
      
        return  render_template('manager_home.html', msg = msg,m_details=m_details,m_store_id=session['m_store_id'],inventory_details=inventory_details)

    else:
        return redirect(url_for('m_login'))

@app.route("/items")
def home_api():
    items = get_item_details()
    msg=''
    if session['loggedin']:
        SL_IDs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        customer_details=SL_IDs.execute('select  shopping_list_id from Shopping_list where cust_ID=%s', [session['id']] )
        for id in SL_IDs:
            print(id['shopping_list_id'])
    else:
        msg = 'You are not logged in !'
        logger.error('Item page load failed because of session log out')
        SL_IDs=''
        #abort(401)

        return redirect(url_for('login'))
    return render_template('items.html', msg = msg,items=items,SL_IDs=SL_IDs)

@app.route("/items/<item_id>")
def item_api(item_id):
    msg=''
    item_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    item_cursor.execute('select * from item where item_id=%s', (item_id,))
    item_details = item_cursor.fetchone()
    print(item_details)
    item_price_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    item_price_cursor.execute('SELECT * FROM team2_app.price_per_unit_view where item_id=%s', [item_id])
    item_price_details = item_price_cursor.fetchall()

    sl_details = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sl_details.execute('select  shopping_list_id from Shopping_list where cust_ID=%s', [session['id']] )
       
    #sl_details.execute('select * from shopping where shopping_list_id=%s', (list_id,))
    sl_details = sl_details.fetchall()
    print(sl_details)

    if len(item_details) == 0:
        abort(404)
        logger.error('Item page load failed because of invalid item id')
    return render_template('item_view.html', item_details = item_details,item_price_details = item_price_details,sl_details = sl_details,msg=msg)

@app.route("/shopinglist/<list_id>")
def shopping_list_api(list_id):
    if not(session['loggedin']):
        msg = 'You are not logged in !'
        return redirect(url_for('login'))
    if session['loggedin']:
        sl_details = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sl_details.execute('select * from contains where shopping_list_id=%s', (list_id,))
        sl_details = sl_details.fetchall()
        session['list_id']=list_id
        msg=''
        if not sl_details:
            msg= 'This Shopping list contains no items'
            logger.error('Shopping list page load failed because of invalid shopping list id')

        item_list=[]
        compare_details=[]
        
        for sl in sl_details:
            item_list.append(sl['item_id'])
        print(item_list)
        logger.info('Shopping list page load successful for Customer'+session['id'])
        for item in item_list:
            print (item)
            compare_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            compare_cursor.execute('select CONTAINS.item_id,store_id,price,quantity_in_stock from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID where  CONTAINS.item_id=%s and shopping_list_id=%s and price =(select min(price)  from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID where  CONTAINS.item_id=%s)', (item,list_id,item))
            compare_details.append( compare_cursor.fetchall())
        
        return render_template('sList_details.html', sl_details = sl_details,list_id=list_id,msg=msg,item_list=item_list,compare_details=compare_details)
    #return jsonify({'shopping_list': sl_details})

@app.route("/customer/new_sl")
def new_sl():
    if session['loggedin']:
        new_sl_id = get_next_sl_id()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Shopping_list VALUES (%s,%s)', (session['id'],new_sl_id) )
        mysql.connection.commit()
        return redirect(url_for('home_api'))
    else:
        msg = 'You are not logged in !'
        return redirect(url_for('login'))

@app.route("/insert_into_sl",methods =['GET','POST'])
def insert_item_into_SL():
    msg=''
    if session['loggedin']:
        if request.method == 'POST':
            item_id=request.form.get('item_id')
            quantity = request.form.get('quantity')
            sl_id = request.form.get('list_id_dropdown')
            quan_cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            quan_cur.execute('select quantity from Contains where item_id=%s and shopping_list_id=%s', (item_id,sl_id))
            quan_details = quan_cur.fetchone()
            quantity_in_sl=0
            if quan_details:
                quantity_in_sl = int(quan_details['quantity'])
            print(not(quantity.isnumeric()))
            print((quantity_in_sl+int(quantity))<0)
            #check if quantity is a positive integer
            if not(checkInt(quantity)):
                    msg='Quantity can only be positive integers'
                    return render_template('sList_details.html', msg = msg)
            elif (quantity_in_sl+int(quantity))<0:
                msg='Quantity cannot be negative'
                logger.error('Quantity cannot be negative')
                return render_template('sList_details.html', msg = msg)

            #if (quantity.isdigit() or (quantity_in_sl+int(quantity))<0):
            #msg = 'Quantity can only be positive integer! Quantity didnt get updated in %s for item %s', (sl_id,item_id)
                
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('select * from Contains where ITEM_ID=%s and shopping_list_id=%s', (item_id,sl_id))
                insert_update_item_flag = cursor.fetchone()
                if insert_update_item_flag:
                    cursor.execute('update Contains set quantity=quantity+%s where ITEM_ID=%s and shopping_list_id=%s', (quantity,item_id,sl_id))
                    mysql.connection.commit()
                    logger.info('Quantity updated in %s for item %s', (sl_id,item_id))
                else:
                    cursor.execute('INSERT INTO Contains VALUES (%s,%s,%s)', (sl_id,item_id,quantity) )
                    mysql.connection.commit()
                    logger.info('Quantity inserted in %s for item %s', (sl_id,item_id))
                #return redirect(url_for('item_api()'))
                return redirect(url_for('shopping_list_api',list_id=sl_id))
            #return redirect(url_for('home_api'))
        else:
            return 'test fail'
            logger.error('Insert into shopping list failed')


    else:
        msg = 'You are not logged in !'
        logger.error('insert items into SL failed because of session timeout')
        return redirect(url_for('login'))


#given shopping list id,create a route to split the shopping list into multiple orders
@app.route("/Split_shopping_list",methods =['GET','POST'])
def split_sl():
    if session['loggedin']:
        list_id = session['list_id']
        sl_details = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sl_details.execute('select * from contains where shopping_list_id=%s', (list_id,))
        sl_details = sl_details.fetchall()
        #print(sl_details)
        msg=''
        if not sl_details:
            msg= 'This Shopping list contains no items'
            logger.warning(list_id+' contains no items')

        item_list=[]
        compare_details=[]
        offering_dict_outer=[]
        
        for sl in sl_details:
            item_list.append(sl['item_id'])
        print(item_list)
        for item in item_list:
            print ("\n Details of : "+item)
            quantity_in_sl=get_item_quantity(item,list_id)
            print("quantity required = "+str(quantity_in_sl)+" for "+item)
            quantity_needed=quantity_in_sl
            compare_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            compare_cursor.execute('select * from offers  where item_id=%s order by price asc', (item,))
            offering_stores=compare_cursor.fetchall()
            offering_store_list=[]
            offering_order_list=[]
            offering_item_list=[]
            offering_quantity_list=[]
            offering_price_list=[]
            for offering_store in offering_stores:
                offering_store_list.append(offering_store['store_id'])
                offering_order_list.append("OR_dummy")
                offering_item_list.append("IT_Dummy")
                offering_quantity_list.append(0)
                offering_price_list.append(0)
           
            offering_dict_len=len(offering_store_list)
            offering_bool=[False]*offering_dict_len
            def_payment_mode="CARD"
            offering_dict={}
            for i in range(offering_dict_len):
                offering_dict[i]={}
                offering_dict[i]['store']=offering_store_list[i]
                offering_dict[i]['order']=offering_order_list[i]
                offering_dict[i]['order_flag']=offering_bool[i]
                offering_dict[i]['item']=offering_item_list[i]
                offering_dict[i]['quantity']=offering_quantity_list[i]
                offering_dict[i]['price']=offering_price_list[i]
            #print("offering dict = "+str(offering_dict))

            for offering_store in offering_stores:
                print(offering_store['store_id'])
                print(offering_store)
                store_id=offering_store['store_id']
                price=offering_store['price']
                quantity_in_stock=offering_store['quantity_in_stock']
                #print(quantity_in_stock)

                breaker=False
                while(quantity_needed!=0):
                    if(quantity_needed<quantity_in_stock):
                        
                        print(str(quantity_needed)+" of item "+item+" in store "+str(store_id))
                        for offering_dict_key in offering_dict:
                            if offering_dict[offering_dict_key]['store']==store_id:
                                offering_dict[offering_dict_key]['order_flag']=True
                                offering_dict[offering_dict_key]['quantity']=quantity_needed
                                offering_dict[offering_dict_key]['item']=item
                                offering_dict[offering_dict_key]['price']=price
                        quantity_needed=0
                        breaker=True
                        break
                   
                    else:
                        quantity_needed=quantity_needed-quantity_in_stock
                        print(str(quantity_in_stock)+" of itemm "+item+" in store "+str(store_id))
                        for offering_dict_key in offering_dict:
                            if offering_dict[offering_dict_key]['store']==store_id:
                                offering_dict[offering_dict_key]['order_flag']=True
                                offering_dict[offering_dict_key]['quantity']=quantity_in_stock
                                offering_dict[offering_dict_key]['item']=item
                                offering_dict[offering_dict_key]['price']=price

                        if(quantity_needed!=0):
                            print("moving on to next store as "+store_id+" has run out of stock for "+item+". "+str(quantity_needed)+" items are left to be ordered")
                            logger.info("moving on to next store as "+store_id+" has run out of stock for "+item+". "+str(quantity_needed)+" items are left to be ordered")
                            break
            if(quantity_needed!=0):
                        print(item+"'s "+str(quantity_needed)+" items left unordered")
                        logger.info(item+"'s "+str(quantity_needed)+" items left unordered")
                        msg=item+"'s "+str(quantity_needed)+" items left unordered"
            else:
                    print("All items ordered for "+item)
                    logger.info("All items ordered for "+item)
                   
            #print("offering dict = "+str(offering_dict))
           
            offering_dict_outer.append(offering_dict)
            for offering_dict_key in offering_dict:
                if offering_dict[offering_dict_key]['order_flag']==True:
                    print(offering_dict[offering_dict_key]['store'])
                    order_id=get_next_order_id()
                    total_cost=offering_dict[offering_dict_key]['quantity']*offering_dict[offering_dict_key]['price']
                    order_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    order_cursor.execute('INSERT INTO Orders(order_id,shopping_list_id,payment_method,total_cost) VALUES(%s,%s,%s,%s)', 
                    (order_id,list_id,def_payment_mode,total_cost) )
                    mysql.connection.commit()
                    offering_dict[offering_dict_key]['order']=order_id
        print("--------------------------------")
        print("offering dict outer ")
        logger.info("offering dictionary outer")
        #external_offering_dict=offering_dict_outer
        session['offering_dict_outer']=offering_dict_outer
        for outer_dict_key in offering_dict_outer:
            for inner_dict_key in outer_dict_key:
                if(outer_dict_key[inner_dict_key]['order_flag']==True):
                    print(outer_dict_key[inner_dict_key])
                    record_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    record_cursor.execute('Insert into Record values (%s,%s,%s)',
                    (outer_dict_key[inner_dict_key]['order'],outer_dict_key[inner_dict_key]['item'],outer_dict_key[inner_dict_key]['quantity']))
                    mysql.connection.commit()

                    process_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    process_cursor.execute('Insert into Process_Order values (%s,%s)',
                    (outer_dict_key[inner_dict_key]['order'],outer_dict_key[inner_dict_key]['store']))
                    mysql.connection.commit()

                    update_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    update_cursor.execute('Update Offers set quantity_in_stock=(quantity_in_stock-%s) where store_id=%s and item_id=%s',
                    (outer_dict_key[inner_dict_key]['quantity'],outer_dict_key[inner_dict_key]['store'],outer_dict_key[inner_dict_key]['item']))
                    mysql.connection.commit()
                    print("**********")
          
        return render_template('split_sl.html', sl_details = sl_details,list_id=list_id,item_list=item_list,compare_details=compare_details,offering_dict_outer=offering_dict_outer,msg=msg)
    else:
        msg = 'You are not logged in !'
        logger.error("split operation failed because os session timeout!")
        return redirect(url_for('login'))

@app.route('/order_details/<order_id>')
def order_details(order_id):
    if session['loggedin']:
        record_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        record_cursor.execute('SELECT * FROM Record WHERE order_id=%s',(order_id,))
        record_details = record_cursor.fetchall()


        order_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        order_cursor.execute('select * from Orders where order_id=%s', (order_id,))
        order_details = order_cursor.fetchall()

        process_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        process_cursor.execute('select * from Process_Order where order_id=%s', (order_id,))
        process_details = process_cursor.fetchall()

        

            #if external_offering_dict[details]['order']==order_id:
             #   print(external_offering_dict[details])
        return render_template('order_details.html', order_details = order_details,order_id=order_id,record_details=record_details,process_details=process_details)            
       
    else:
        msg = 'You are not logged in !'
        return redirect(url_for('login'),msg=msg)