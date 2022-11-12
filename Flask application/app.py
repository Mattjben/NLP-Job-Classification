# Assignment 2 | Milestone II Web-based Data Application
# Matthew Bentham 
# S3923076

# IMPORT LIBRARIES
from flask import Flask, render_template, request, redirect, url_for,flash,session
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash 
from bs4 import BeautifulSoup
from flask_ckeditor import CKEditor
import os
from static.nlp import nlpsuggestion


# Intialisation 
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'jobs.db')
db_uri = 'sqlite:///{}'.format(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = "Assignment2.2"
app.app_context().push()
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

# DATABASES ----------------------------------------------------------------
class Jobs(db.Model):
    __tablename__ = 'Jobs'
    Webindex = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String)
    Title = db.Column(db.String)
    Company = db.Column(db.String)
    Salary = db.Column(db.Integer)
    ContractType = db.Column(db.String)
    Description = db.Column(db.String)

class Users(db.Model,UserMixin):
    __tablename__ = 'Users'
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.Integer)
    Email = db.Column(db.String)
    Password = db.Column(db.String)
    Company = db.Column(db.String)
    def is_active(self):
        return True
    def get_id(self):
        return (self.Id)


# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
        
@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# HOME PAGE ------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

# Error handler ------------------------------------------
# Invalid URL
@app.errorhandler(404)
def Page_error(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def Page_error(e):
	return render_template("500.html"), 500



# JOB SEARCH ---------------------------------------------------------------

@app.route('/search', methods=['GET','POST'])
def search():

    # Get search inputs: 
    Cat = [request.form.get('Cat1'),request.form.get('Cat2'),request.form.get('Cat3'),request.form.get('Cat4')]
    Contract = [request.form.get('Contractp'),request.form.get('Contractf'),request.form.get('Contractca'),request.form.get('Contractc')]
    contracts =['Part time','Full Time','Casual','Contract']
    cats=['Accounting_Finance',"Engineering","Healthcare_Nursing","Sales"]
    search = request.form.get('Keyword')
    Salmin = request.form.get('salmin')
    Salmax = request.form.get('salmax')
    jobs = Jobs.query.order_by(Jobs.Webindex)

    if request.method == "POST":
        # Filter database by search inputs 
        if not all(v is None for v in Contract):
            print(Contract)
            for i,c in enumerate(Contract):
                if not c:
                    jobs = jobs.filter(Jobs.ContractType != contracts[i])
        if not all(v is None for v in Cat):
            for i,c in enumerate(Cat):
                if not c:
                    print(cats[i])
                    jobs = jobs.filter(Jobs.Category != cats[i])
        if Salmax:
            jobs = jobs.filter(Jobs.Salary < Salmax)
        if Salmin:
            jobs = jobs.filter(Jobs.Salary >=Salmin)
        if search != '' and search != None:
            jobs = jobs.filter(Jobs.Title.like('%' + search + '%'))
        
    jobs = jobs.all()
    return render_template('index.html', posts=jobs)
# JOB POST ---------------------------------------------------------------
@app.route('/post/<int:Webindex>')
def post(Webindex):
    # Loads job post based on Webindex 
    post = Jobs.query.filter_by(Webindex=Webindex).one()

    return render_template('post.html', post=post)


# Create new job ---------------------------------------------------------------
@app.route('/add/<int:Id>',methods=["GET","POST"])
@login_required
def add(Id):
    User = Users.query.filter_by(Id=Id).all()
    return render_template('add.html',user=User[0])

@app.route('/addpost/<int:Id>', methods=['GET','POST'])
@login_required
def addpost(Id):
    # Loads inputted data and saves post to database
    user = Users.query.filter_by(Id=Id).all()
    title = request.form['title']
    Company = user[0].Company
    Description =  request.form.get('ckeditor')
    # Get recomended category
    Des = BeautifulSoup(Description)
    t= BeautifulSoup(title)
    Category =nlpsuggestion(Des.get_text(),t.get_text())
    Salary = request.form.get('Salary')
    ContractType = request.form.get('ContractType')
    max_id = db.session.query(func.max(Jobs.Webindex)).scalar() # adds to the maximum id 
    post = Jobs(Webindex =max_id+1,Title=title, Company=Company, Description=Description, Category=Category,Salary=Salary,ContractType=ContractType)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('Tags',Webindex=max_id+1))
@app.route('/addpost/tags/<int:Webindex>')
@login_required
def Tags(Webindex):
    job =Jobs.query.filter_by(Webindex=Webindex).all()
    return render_template('Tags.html',Job=job[0])
@app.route('/addpost/tags/edit/<int:Webindex>',methods=["GET","POST"])
@login_required
def edittags(Webindex):
    job =Jobs.query.filter_by(Webindex=Webindex).all()
    if request.method == "POST":
        job=job[0]
        # Reads submitted new values 
        job.Category = request.form['Category']
        # Saves new values to database 
        db.session.add(job)
        db.session.commit()
        flash("Tag Updated") # shows flash message to user 
        return redirect(url_for('search'))
    return render_template('Tagsedit.html',Job=job[0])

# Edit posts -------------------------------------------------------------------------------
@app.route('/post/edit/<int:Webindex>',methods=["GET","POST"])
@login_required
def editpost(Webindex):

	post = Jobs.query.filter_by(Webindex=Webindex).first()
	Id = current_user.Id

	if request.method == "POST":
        # Reads submitted new values 
		post.Title = request.form['title']
		post.Description = request.form.get('ckeditor')
		post.Salary = request.form['Salary']
        # Get recomended category
		Des = BeautifulSoup(post.Description)
		t= BeautifulSoup(post.Title)
		Category =nlpsuggestion(Des.get_text(),t.get_text())
		post.ContractType = request.form['ContractType']
		# Saves new values to database 
		db.session.add(post)
		db.session.commit()
		flash("Post Updated") # shows flash message to user 
		return redirect(url_for('Tags',Webindex=post.Webindex))
	return render_template('edit_post.html',post=post,des=post.Description)

# Delete posts -------------------------------------------------------------------------------
@app.route('/post/delete/<int:Webindex>',methods=["GET","POST"])
@login_required
def deletepost(Webindex):
	Id = current_user.Id
	post = Jobs.query.filter_by(Webindex=Webindex).first()

	try:
		db.session.delete(post)
		db.session.commit()
		flash("Blog posted deleted")
		return redirect(url_for('Userpage',Id=Id))
	except:
		flash("Problem deleting post")
		return redirect(url_for('Userpage',Id=Id))



# ADD COMPANY USER ------------------------------------------------------------

@app.route('/user/add')

def register(): # direct user to add_user method 
    return render_template("add_user.html",name=None)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    # GETs all values entered 
    Company = request.form.get('Company')
    Email = request.form.get('Email')
    username = request.form.get('Username')
    Password = request.form.get('Password')
    Password2 = request.form.get('Password2')

    user = Users.query.filter_by(Email=Email).first()
 
    if Password != Password2:# checks if confirmation password matches 
        flash("Passwords dont match!")
        return render_template("add_user.html",name=None)

    else:
        if user is None:
            # Hashes password for secruity reasons 
            hashed_pw = generate_password_hash(Password, "sha256")
            user = Users(Username=username, Company=Company, Email=Email, Password=hashed_pw)
            # Adds user to database 
            db.session.add(user)
            db.session.commit()
        
            flash("User Added Successfully!")
    
           

            return render_template("login.html")
        else: # Gets error is user is allready in the database  
            flash("User allready exists")
            return render_template("add_user.html",name=None)


# LOGIN USER:  ------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login_post():
    # Gets enetered data 
    username = request.form.get('Username')
    password = request.form.get('Password')
    # Finds user based on entered username
    user = Users.query.filter_by(Username=username).first()
    if user: 
        posts = Jobs.query.filter_by(Company=user.Company).all()
        if check_password_hash(user.Password, password): # Check if password matches database record 
            login_user(user)
            session['logged_in'] = True # Login user 
            flash("Login Succesfull!!")
            return redirect(url_for('Userpage' ,Id=user.Id,posts=posts))
        else:
            flash("Wrong Password - Try Again!")
    else: # error if user does not exists 
        flash("That User Doesn't Exist! Try Again...")


    return render_template('login.html')

# UserPage -------------------------------------------------------------------------------
@app.route('/Userpage/', methods=['GET', 'POST'])
@login_required
def Userpage(): 
    # Get User and Job values correspinding to the current logged in user 
	Id = current_user.Id
	user = Users.query.filter_by(Id=Id).first()
	posts = Jobs.query.filter_by(Company=user.Company).all()
    
	return render_template("Userpage.html",id = Id,posts=posts)
# EDIT COMPANY USER ------------------------------------------------------------
@app.route('/Userpage/edit', methods=['GET', 'POST'])
@login_required
def editUser():
    # Get user values of current logged in user 
    Id = current_user.Id
    user = Users.query.filter_by(Id=Id).first()
    if request.method == "POST":
        # Retrive entered values 
        user.Company = request.form.get('Company')
        user.Email = request.form.get('Email')
        user.Username = request.form.get('Username')
        Password = request.form.get('Password')
        Password2 = request.form.get('Password2')

        if Password != Password2: # Check if passwords match 
            flash("Passwords dont match!")
            return render_template("editprofile.html",user=user)

        else: # Edit database entry for user and redirect back to userpage 
            user.Password = generate_password_hash(Password, "sha256")
            db.session.add(user)
            db.session.commit()
            flash("User Updated")
            return redirect(url_for('Userpage',Id=Id))
	
    return render_template("editprofile.html",user=user)

# Delete User -------------------------------------------------------------------------------
@app.route('/post/delete',methods=["GET","POST"])
@login_required
def deleteuser():
    # Get user database entry 
	Id = current_user.Id
	user = Users.query.filter_by(Id=Id).first()
	
	try:
        # Logout user and delete user form database 
		logout_user()
		session['logged_in'] = False
		db.session.delete(user)
		db.session.commit()
		flash("User deleted")
		return redirect(url_for('login'))
	except:
		flash("Problem deleting user")
		return redirect(url_for('Userpage',Id=Id))




# Company profiles  -------------------------------------------------------------------------------
@app.route('/Companyprofile/<Company>')
def Profilepage(Company):
    # Get user data and all jobs posted by given company 
	user = Users.query.filter_by(Company=Company).first()
	post = Jobs.query.filter_by(Company=Company).all()

	return render_template('CompanyProfile.html', posts=post,user=user)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # Log user out and redirect to login page
	logout_user()
	session['logged_in'] = False
	flash("You Have Been Logged Out!  Thanks For Stopping By...")
	return redirect(url_for('login'))
	


if __name__ == '__main__':
    app.run(debug=True)