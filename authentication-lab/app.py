from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDmI64XZjr4r_lOiCrfCKKxCOzDGZRnraY",
  "authDomain": "fir-project-e6676.firebaseapp.com",
  "projectId": "fir-project-e6676",
  "storageBucket": "fir-project-e6676.appspot.com",
  "messagingSenderId": "106103967808",
  "appId": "1:106103967808:web:32cf94bc6e23392f0ccfa5",
  "measurementId": "G-4KHFZMXGW1",
  "databaseURL":"https://fir-project-e6676-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user={'fullname':request.form['fullname'], 'username':request.form['username'], 'email':request.form['email'],
            bio: request.form['bio'], password:request.form['password']}
            db.child("users").child(login_session['user']['localId'].set(user))
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=='POST':
        try:
            tweet={'title':request.form['title'], 'text':request.form['text'],'uid':(db.child('users').child(login_session['user']['localId']).get().val())['username']}
            db.child("tweets").push(tweet)
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))




if __name__ == '__main__':
    app.run(debug=True)