#======================================================================
#Can/able to add,delete,edit,view the database
#Can generate report in xlsx & pdf
#Can insert data manually, import excel file
#
#======================================================================
#---------------------------<< IMPORTANT ! >>--------------------------
#ONLY ACCEPT Excel in "CSV" format for Excel, xlsx cant be read
#======================================================================
import os
import pymysql
import xlwt
import io
import pandas as pd
import mysql.connector
from flask import Flask, Response, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

"""
import pymssql

userpass = "mssql+pymysql://root:@"
basedir = "127.0.0.1/"
dbname = "iventory"

app.config['SQLALCHEMY_DATABASE_URI'] = = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret@123'

userpass = "mysql+pymysql://root:@"
basedir = "127.0.0.1/"
dbname = "iventory"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

mysql = MySQL() # MySQL configurations

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'iventory'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'



mysql.init_app(app)

db = SQLAlchemy(app)

#==<<
# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER2 = 'static/files2'
app.config['UPLOAD_FOLDER2'] =  UPLOAD_FOLDER2

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

mydb = pymysql.connect(host="localhost",user="root",password="",database="iventory")

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")
#==>>

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
"""
#define a func to require login
for protected pages
def login_required(f):
    @wraps(f)
    def decorated_function (*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for(login))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def baseindex():
    if request.method == 'POST':
        #retrieve username& password
        username = request.form['username']
        password = request.form['password']

        #query
        conn = mysql.connection.cursor()
        conn.execute ("SELECT * FROM login WHERE username= %s AND password= %s", (username,password))

        #if user exists, can proceed
        if user:
            session['logged_in'] = True
            return redirect(url_for('home'))

        else:
            return 'Invalid Username or Password'

        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    
    #if session, then remove username, loggedin, cookie 
    session.pop('username', None)
    session.pop('loggedin', None)

    return redirect(url_for('login'))

@app.after_request
def add_header(response):
    #Prevent caching of previous page
    response.headers['Cache-Control'] = 'no-cache, no-store, must-recalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0' 
    return response

@app.route(/exp1)
@login_required
def protected1():
    return render_template('exp1.html')

    @app.route(/exp1)
@login_required
def protected1():
    return render_template('exp1.html', login=login)

"""
@app.route('/')
def baseindex():
    return render_template('homepage.html')
#end-Section


#===========================================
#<Section- Guide>---------------------------
#===========================================
@app.route("/baseindex/guide")
def guide():
    return render_template('guide.html')
#end-Section

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#===========================================
#<Section- Incoming Item>-------------------
#===========================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#viewIncoming=> 
@app.route("/baseindex/viewIncoming/")
def viewIncoming():
    data_recordincoming = db.session.query(recordincoming)
    return render_template('viewIncoming.html', data= data_recordincoming)

#viewIncoming=> Add item
@app.route("/viewStorage/addIncoming") 
def addIncoming():
    return render_template('addIncoming.html')
    #viewIncoming=> Add item process
@app.route("/viewStorage/inputIncoming", methods=['GET' , 'POST']) 
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
def editIncoming(no_incoming):
    data_recordincoming = recordincoming.query.get(no_incoming)
    return render_template('editIncoming.html', data=data_recordincoming)
    #viewIncoming=> Edit item process
@app.route("/viewIncoming/editIncomingprocess", methods=['POST' , 'GET'])
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
def deleteIncoming(no_incoming):
    data_recordincoming = recordincoming.query.get(no_incoming)
    db.session.delete(data_recordincoming)
    db.session.commit()

    flash('Delete Data Success!')

    return redirect(url_for('viewIncoming'))

#viewIncoming=> Upload CSV file/data to database
@app.route("/viewIncoming/csvIncoming") 
def csvIncoming():
    return render_template('csvIncoming.html')
    #viewIncoming=> Read & Save CSV file/data to database
@app.route("/viewIncoming/incomingexcel", methods=['POST'])
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
                print(i,row['rdate_incoming'], row['rby_incoming'], row['i_incoming'], row['desc_incoming'], row['serial_incoming'], row['qty_incoming'], row['remark_incoming'])
            except Exception:
                print(i,row['rdate_incoming'], row['rby_incoming'], row['i_incoming'], row['desc_incoming'], row['serial_incoming'], row['qty_incoming'], row['remark_incoming'])

#viewIncoming=> Create report in Excel.xls format
@app.route('/viewIncoming/export_reportIncoming')
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
#end-Section


#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#===========================================
#<Section- Tracking Item>-------------------
#===========================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#viewStorage=> 
@app.route("/baseindex/viewStorage/")
def viewStorage():
    data_recordstorage = db.session.query(recordstorage)
    return render_template('viewStorage.html', data= data_recordstorage)

#viewStorage=> Add item
@app.route("/viewStorage/addStorage") 
def addStorage():
    return render_template('addStorage.html')
    #viewStorage=> Add item process
@app.route("/viewStorage/inputStorage", methods=['GET','POST']) 
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
def editStorage(no_storage):
    data_recordStorage = recordstorage.query.get(no_storage)
    return render_template('editStorage.html', data=data_recordStorage)
    #viewStorage=> Edit item process
@app.route('/viewStorage/editStorageProcess', methods=['POST','GET']) 
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
def deleteStorage(no_storage):
    data_recordstorage = recordstorage.query.get(no_storage)
    db.session.delete(data_recordstorage)
    db.session.commit()

    flash('Delete Data Success!')

    return redirect(url_for('viewStorage'))

#viewStorage=> Upload CSV file/data to database
@app.route("/viewStorage/csvStorage") 
def csvStorage():
    return render_template('csvStorage.html')
    #viewStorage=> Read & Save CSV file/data to database
@app.route("/viewStorage/storageexcel", methods=['POST'])
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
    #add headers
    sh.write(0, 1, 'ID ITEM')
    sh.write(0, 2, 'ENVIRONMENT')
    sh.write(0, 3, 'DETAILS')
    sh.write(0, 4, 'QTY')
    sh.write(0, 5, 'REMARK')
    
    idx = 0
    for row in result:
        sh.write(idx+1, 0, row['id_storage'])
        sh.write(idx+1, 1, row['env_storage'])
        sh.write(idx+1, 2, row['detail_storage'])
        sh.write(idx+1, 3, row['quantity_storage'])
        sh.write(idx+1, 4, row['remark_storage'])
        idx += 1
    
    workbook.save(output)
    output.seek(0)

    flash('Generate Report Success!')
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Storage-Item_Report.xls"})
#end-Section


if __name__ == "__main__":
    app.run(debug=True)