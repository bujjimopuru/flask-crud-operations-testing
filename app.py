from flask import Flask,render_template,request,redirect,url_for,flash
import psycopg2
import psycopg2.extras
import re 

app=Flask(__name__)

app.secret_key = "cairocoders-ednalan"
 
DB_HOST = "localhost"
DB_NAME = "flaskapi"
DB_USER = "postgres"
DB_PASS = "c98xa5"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/details")
def get_details():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM registers"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template("details.html",users=list_users)

@app.route('/create',methods=['POST'])
def create():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method=='POST':
        hobby=request.form.getlist('hobbies')
        hobbies=",".join(map(str,hobby))
        firstname=request.form['firstname']
        print(firstname)
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        gender=request.form.get("gender")
        hobbies=hobbies
        country=request.form['country']
        ##
        cur.execute('SELECT * FROM registers WHERE email = %s', (email,))
        account = cur.fetchone()
        #print(account)
        # If account exists show error and validation checks
        if account:
            flash('user already exists!')
            #return redirect(url_for('home'))
            return render_template("home.html")
        ##
        elif firstname=="" or lastname=="" or email=="" or password=="" or gender=="" or  hobbies=="":
            flash("Please fill all the details")
            #return redirect(url_for('home'))
            return render_template("home.html")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
            #return redirect(url_for('home'))
            return render_template("home.html")
        elif not (len(password) >= 8 and
        re.search(r'\d+', password) and
        re.search(r'[a-z]+', password) and
        re.search(r'[A-Z]+', password) and
        re.search(r'\W+', password) and not
        re.search(r'\s+', password)):
            
            flash("Password should be combination of alphabets, special characters, digits and length of password is greater than 8")
            #return redirect(url_for('home'))
            return render_template("home.html")
        else:
            cur.execute("INSERT INTO registers (firstname, lastname, email,password,gender,hobbies,country) VALUES (%s,%s,%s,%s,%s,%s,%s)", (firstname, 
            lastname, email,password,gender,hobbies,country))
            conn.commit()
            flash('User Registered successfully')
            return redirect(url_for('get_details'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM registers WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    #print(data[0])
    return render_template('edit.html', user = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        hobby=request.form.getlist('hobbies')
        hobbies=",".join(map(str,hobby))
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        gender=request.form['gender']
        hobbies=hobbies
        country=request.form['country']         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE registers
            SET firstname = %s,
                lastname = %s,
                email = %s,
                password=%s,
                gender=%s,
                hobbies=%s,
                country=%s
            WHERE id = %s
        """, (firstname, lastname, email,password,gender,hobbies,country,id))
        flash('User Updated Successfully')
        conn.commit()
        return redirect(url_for('get_details'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM registers WHERE id = {0}'.format(id))
    conn.commit()
    flash('User Removed Successfully')
    return redirect(url_for('get_details'))
 
if __name__=='__main__':
    app.run(debug=True)