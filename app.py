#======================================================================
#Can/able to add,delete,edit,view the database
#Can generate report in xlsx & pdf
#Can insert data manually, import excel file
#
#======================================================================
#---------------------------<< IMPORTANT ! >>--------------------------
#ONLY ACCEPT Excel in "CSV" format for Excel, xlsx cant be read
#======================================================================
import datetime
from functools import wraps
import os
import pymysql
import xlwt
import io
import pandas as pd
import mysql.connector
from flask import Flask, Response, render_template, redirect, session, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

"""
#preparation for changes to MsSql
import pymssql

userpass = "mssql+pymysql://root:@"
basedir = "127.0.0.1/"
dbname = "iventory"

app.config['SQLALCHEMY_DATABASE_URI'] = = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
"""
app= Flask(__name__)
# set secret key
app.config['SECRET_KEY'] = 'secret@123'

# set database configurations
user = 'root'
password = ''
host = '127.0.0.1'
dbname = 'inventory'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set MySQL configurations
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = dbname
app.config['MYSQL_HOST'] = host
mysql = MySQL(app)

# create database instance
db = SQLAlchemy(app)

# set debugging mode
app.config['DEBUG'] = True

# set upload folders
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['UPLOAD_FOLDER2'] = 'static/files2'

# connect to database and execute query
mydb = pymysql.connect(host="localhost", user="root", password="", database="inventory")
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")


#===========================================
#<Section- Table Database>------------------
#===========================================
#table=> recordincoming
class recordincoming(db.Model):
    #no_incoming, rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming<<
    no_incoming = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rdate_incoming = db.Column(db.String(100), nullable= False)
    rby_incoming = db.Column(db.String(100), nullable= False)
    i_incoming = db.Column(db.String(500), nullable= False)
    desc_incoming = db.Column(db.String(100), nullable= False)
    serial_incoming = db.Column(db.String(100), nullable= False)
    qty_incoming = db.Column(db.String(100), nullable= False)
    remark_incoming = db.Column(db.String(500), nullable= False)

    def __init__(self, rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming):
        self.rdate_incoming= rdate_incoming    
        self.rby_incoming= rby_incoming
        self.i_incoming= i_incoming
        self.desc_incoming= desc_incoming
        self.serial_incoming= serial_incoming
        self.qty_incoming= qty_incoming
        self.remark_incoming= remark_incoming


#table=> recordstorage
class recordstorage(db.Model): 
    #no_storage, id_storage, env_storage, detail_storage, quantity_storage, remark_storage
    no_storage = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_storage = db.Column(db.String(500), nullable= False)
    env_storage = db.Column(db.String(500), nullable= False)
    detail_storage = db.Column(db.String(100), nullable= False)
    quantity_storage = db.Column(db.String(100), nullable= False)
    remark_storage = db.Column(db.String(500), nullable= False)

    def __init__(self, id_storage, env_storage, detail_storage, quantity_storage, remark_storage):
        self.id_storage= id_storage
        self.env_storage= env_storage 
        self.detail_storage= detail_storage    
        self.quantity_storage= quantity_storage
        self.remark_storage= remark_storage

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#===========================================
#<Section- Login & Logout>------------------
#===========================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#define a func to require login
def login_required(f):
    @wraps(f)
    def decorated_function (*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# function to specify report date
def get_report_date():
    # get current date
    today = datetime.date.today()
    # format date as dd-mm-yyyy
    return today.strftime('%d-%m-%Y')

@app.route('/homepage')
def homepage():
    if not 'logged_in' in session:
        return redirect(url_for('login'))
    else:
        return render_template('homepage.html')


@app.route('/', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        #retrieve username& password
        username = request.form['username']
        password = request.form['password']
        #query
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute ("SELECT * FROM users WHERE username= %s AND password= %s", (username,password))
        user = cursor.fetchone()
        cursor.close()
        #if user exists, can proceed
        if user:
            session['logged_in'] = True
            return redirect(url_for('homepage'))
        else:
            return 'Invalid Username or Password'
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    #if session, then remove username, loggedin, cookie 
    session.pop('username', None)
    session.pop('logged_in', None)
    session.clear()

    return redirect(url_for('login'))

@app.after_request
def add_header(response):
    #Prevent caching of previous page
    response.headers['Cache-Control'] = 'no-cache, no-store, must-recalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0' 
    return response

#===========================================
#<Section- Guide>---------------------------
#===========================================
@app.route("/baseindex/guide")
def guide():
    return render_template('guide.html')

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#===========================================
#<Section- Incoming Item>-------------------
#===========================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#viewIncoming=> 
@app.route("/baseindex/viewIncoming/")
@login_required
def viewIncoming():
    data_recordincoming = db.session.query(recordincoming)
    return render_template('viewIncoming.html', data= data_recordincoming)

#viewIncoming=> Add item
@app.route("/viewStorage/addIncoming")
@login_required
def addIncoming():
    return render_template('addIncoming.html')
    #viewIncoming=> Add item process
@app.route("/viewStorage/inputIncoming", methods=['GET','POST']) 
@login_required
def inputIncoming():
    if request.method == 'POST':
        rdate_incoming = request.form['rdate_incoming']
        rby_incoming = request.form['rby_incoming']
        i_incoming = request.form['i_incoming']
        desc_incoming = request.form['desc_incoming']
        serial_incoming = request.form['serial_incoming']
        qty_incoming = request.form['qty_incoming']
        remark_incoming = request.form['remark_incoming']
        #no_incoming, rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming
        input_incoming = recordincoming(rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming)

        db.session.add(input_incoming)
        db.session.commit()

        flash("Submit Data Success!")

        return redirect(url_for('viewIncoming'))

    return render_template('addIncoming.html')

#viewIncoming=> Edit item
@app.route("/viewIncoming/editIncoming/<int:no_incoming>") 
@login_required
def editIncoming(no_incoming):
    data_recordincoming = recordincoming.query.get(no_incoming)
    return render_template('editIncoming.html', data=data_recordincoming)
    #viewIncoming=> Edit item process
@app.route("/viewIncoming/editIncomingprocess", methods=['GET','POST'])
@login_required
def editIncomingprocess():
    data_recordincoming = recordincoming.query.get(request.form.get('no_incoming'))
    #no_incoming, rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming
    data_recordincoming.rdate_incoming = request.form['rdate_incoming']
    data_recordincoming.rby_incoming = request.form['rby_incoming']
    data_recordincoming.i_incoming = request.form['i_incoming']
    data_recordincoming.desc_incoming = request.form['desc_incoming']
    data_recordincoming.serial_incoming = request.form['serial_incoming']
    data_recordincoming.qty_incoming = request.form['qty_incoming']
    data_recordincoming.remark_incoming = request.form['remark_incoming']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('viewIncoming'))

#viewIncoming=> Delete item
@app.route("/viewIncoming/deleteIncoming/<int:no_incoming>") 
@login_required
def deleteIncoming(no_incoming):
    data_recordincoming = recordincoming.query.get(no_incoming)
    db.session.delete(data_recordincoming)
    db.session.commit()

    flash('Delete Data Success!')

    return redirect(url_for('viewIncoming'))

#viewIncoming=> Upload CSV file/data to database
@app.route("/viewIncoming/csvIncoming") 
@login_required
def csvIncoming():
    return render_template('csvIncoming.html')
    #viewIncoming=> Read & Save CSV file/data to database
@app.route("/viewIncoming/incomingexcel", methods=['POST'])
@login_required
def incomingexcel():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER2'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        parseincomingCSV(file_path)
        # save the file
    return redirect(url_for('viewIncoming'))

def parseincomingCSV(filePath):
    # CVS Column Names
    #no_incoming, rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming<<
    col_names = ['rdate_incoming' , 'rby_incoming' , 'i_incoming' , 'desc_incoming' , 'serial_incoming' , 'qty_incoming', 'remark_incoming']
    # Use Pandas to parse the CSV file
    icsvData = pd.read_csv(filePath,names=col_names, skiprows=1)

    # Loop through the Rows
    for i,row in icsvData.iterrows():
            sql = "INSERT INTO recordincoming (rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            value = (row['rdate_incoming'], row['rby_incoming'], row['i_incoming'], row['desc_incoming'], row['serial_incoming'], row['qty_incoming'], row['remark_incoming'])
            try:
                mycursor.execute(sql, value)
                mydb.commit()
                print(row['rdate_incoming'], row['rby_incoming'], row['i_incoming'], row['desc_incoming'], row['serial_incoming'], row['qty_incoming'], row['remark_incoming'])
            except Exception:
                print(i,row['rdate_incoming'], row['rby_incoming'], row['i_incoming'], row['desc_incoming'], row['serial_incoming'], row['qty_incoming'], row['remark_incoming'])

#viewIncoming=> Create report in Excel.xls format
@app.route('/viewIncoming/export_reportIncoming')
@login_required
def export_reportIncoming():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT no_incoming, rdate_incoming, rby_incoming, i_incoming, desc_incoming, serial_incoming, qty_incoming, remark_incoming FROM recordincoming")
    result = cursor.fetchall()
   
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Incoming-Item Report')
    #add headers
    sh.write(0, 0, 'Received Date')
    sh.write(0, 1, 'Received By')
    sh.write(0, 2, 'PO# /DO#/ AWB# (IF Receive item from store)')
    sh.write(0, 3, 'Desc')
    sh.write(0, 4, 'Item Serial Number / Part Number (IF any)')
    sh.write(0, 5, 'Qty')
    sh.write(0, 6, 'Remarks')
    
    idx = 0
    for row in result:
        sh.write(idx+1, 0, row['rdate_incoming'])
        sh.write(idx+1, 1, row['rby_incoming'])
        sh.write(idx+1, 2, row['i_incoming'])
        sh.write(idx+1, 3, row['desc_incoming'])
        sh.write(idx+1, 4, row['serial_incoming'])
        sh.write(idx+1, 5, row['qty_incoming'])
        sh.write(idx+1, 6, row['remark_incoming'])
        idx += 1
    
    workbook.save(output)
    output.seek(0)
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Incoming-item_report.xls"})


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#===========================================
#<Section- Tracking Item>-------------------
#===========================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#viewStorage=> 
@app.route("/baseindex/viewStorage/")
@login_required
def viewStorage():
    search = request.args.get('search')
    if search:
        data_recordstorage = db.session.query(recordstorage).filter_by(id_storage=search)
    else:
        data_recordstorage = db.session.query(recordstorage)
    return render_template('viewStorage.html', data=data_recordstorage, search=search)

#viewStorage=> Add item
@app.route("/viewStorage/addStorage") 
@login_required
def addStorage():
    return render_template('addStorage.html')
    #viewStorage=> Add item process
@app.route("/viewStorage/inputStorage", methods=['GET','POST']) 
@login_required
def inputStorage():
    if request.method == 'POST':
        id_storage = request.form['id_storage']
        env_storage = request.form['env_storage']
        detail_storage = request.form['detail_storage']
        quantity_storage = request.form['quantity_storage']
        remark_storage = request.form['remark_storage']
        #no_storage, id_storage, detail_storage, quantity_storage, remark_storage
        input_storage = recordstorage(id_storage, env_storage, detail_storage, quantity_storage, remark_storage)
    
        db.session.add(input_storage)
        db.session.commit()

        flash("Submit Data Success!")

        return redirect(url_for('viewStorage'))

    return render_template('addStorage.html')

#viewStorage=> Edit item
@app.route('/viewStorage/editStorage/<int:no_storage>') 
@login_required
def editStorage(no_storage):
    data_recordStorage = recordstorage.query.get(no_storage)
    return render_template('editStorage.html', data=data_recordStorage)
    #viewStorage=> Edit item process
@app.route('/viewStorage/editStorageProcess', methods=['GET','POST']) 
@login_required
def editStorageProcess():
    data_recordStorage = recordstorage.query.get(request.form.get('no_storage'))
    #no_storage, id_storage, detail_storage, quantity_storage, remark_storage
    data_recordStorage.id_storage = request.form['id_storage']
    data_recordStorage.env_storage = request.form['env_storage']
    data_recordStorage.detail_storage = request.form['detail_storage']
    data_recordStorage.quantity_storage = request.form['quantity_storage']
    data_recordStorage.remark_storage = request.form['remark_storage']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('viewStorage'))

#viewStorage=> Delete item
@app.route("/viewStorage/deleteStorage/<int:no_storage>") 
@login_required
def deleteStorage(no_storage):
    data_recordstorage = recordstorage.query.get(no_storage)
    db.session.delete(data_recordstorage)
    db.session.commit()

    flash('Delete Data Success!')

    return redirect(url_for('viewStorage'))

#viewStorage=> Upload CSV file/data to database
@app.route("/viewStorage/csvStorage") 
@login_required
def csvStorage():
    return render_template('csvStorage.html')
    #viewStorage=> Read & Save CSV file/data to database
@app.route("/viewStorage/storageexcel", methods=['POST'])
@login_required
def storageexcel():
      # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        parseCSV(file_path)
        # save the file
    return redirect(url_for('viewStorage'))

def parseCSV(filePath):
      # CVS Column Names
      #line_storage, testertype_storage, id_storage, detail_storage, quantity_storage, remark_storage
    col_names = ['id_storage' ,'env_storage','detail_storage' , 'quantity_storage' , 'remark_storage']
      # Use Pandas to parse the CSV file
      #skiprow will skip firstrow(header)
    csvData = pd.read_csv(filePath,names=col_names, skiprows=1)
      # Loop through the Rows
    for i,row in csvData.iterrows():
            sql = "INSERT INTO recordstorage (id_storage, env_storage, detail_storage, quantity_storage, remark_storage) VALUES ( %s, %s, %s, %s, %s)"
            value = (row['id_storage'], row['env_storage'], row['detail_storage'], row['quantity_storage'], row['remark_storage'])
            mycursor.execute(sql, value)
            mydb.commit()
            print(i,row['id_storage'], row['env_storage'],row['detail_storage'], row['quantity_storage'], row['remark_storage'])


#viewStorage=> Create report in Excel.xls format
@app.route('/viewStorage/export_reportStorage')
@login_required
def export_reportStorage():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    #id_storage, detail_storage, quantity_storage, remark_storage
    cursor.execute("SELECT id_storage, env_storage, detail_storage, quantity_storage, remark_storage FROM recordstorage")
    result = cursor.fetchall()
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Storage_InventoryReport')

    # define basic formatting
    style_title = xlwt.easyxf('font: bold on, color white; align: horiz center; borders: top thin, bottom thin, left thin, right thin; pattern: pattern solid, fore_color dark_blue;')
    style_data = xlwt.easyxf('align: horiz left; borders: top thin, bottom thin, left thin, right thin;')
    style_header = xlwt.easyxf('font: bold on; align: horiz center; borders: top thin, bottom thin, left thin, right thin; pattern: pattern solid, fore_color gray25;')
     
    #add title
    sh.write_merge(0, 0, 1, 5, 'InventorySystem', style_title)
    sh.write_merge(1, 1, 1, 5, 'Tracking Item- current items storage', style_title)
    sh.write_merge(2, 2, 1, 5, 'Report Date: ' + get_report_date(), style_title)

    #add headers
    sh.write(4, 1, 'ID ITEM', style_header)
    sh.write(4, 2, 'ENVIRONMENT', style_header)
    sh.write(4, 3, 'DETAILS', style_header)
    sh.write(4, 4, 'QTY', style_header)
    sh.write(4, 5, 'REMARK', style_header)

    idx = 0
    for row in result:
        sh.write(idx+5, 1, row['id_storage'], style_data)
        sh.write(idx+5, 2, row['env_storage'], style_data)
        sh.write(idx+5, 3, row['detail_storage'], style_data)
        sh.write(idx+5, 4, row['quantity_storage'], style_data)
        sh.write(idx+5, 5, row['remark_storage'], style_data)
        idx += 1
    
    workbook.save(output)
    output.seek(0)

    flash('Generate Report Success!')
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Storage-Item_Report.xls"})


if __name__ == "__main__":
    app.run(debug=True)