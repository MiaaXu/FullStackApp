from werkzeug.security import check_password_hash
from flask import Flask, request
import flask_login
import mysql.connector 


# Server Development
app = Flask(__name__)

students = mysql.connector.connect(user = 'root',
                            password = '1234abcd',
                            database = 'StudentsDB')


# Set the secret key to some random bytes. Keep this really secret! 
app.secret_key = "super secret string"  

# Initialize a LoginManager object to prepare for user login authentication
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin): 
    def __init__(self, studentid, password):
        self.id = studentid
        self.password = password

# user loader callback function is required by Flask_Login; it returns either None or the user object id given an user instance.
@login_manager.user_loader 
def user_finder(id):
    cursor = students.cursor()
    cursor.execute('SELECT StudentID, Password from Students where StudentID = %s', (id,) )
    user = cursor.fetchone()
    cursor.close()
    if user is not None:
        return User(user[0], user[1])
    else:
        return None
    
# @app.get("/login")
# def login_get():
#     return """<form method=post>
#       StudentId: <input name="id"><br>
#       Password: <input name="password" type=password><br>
#       <button>Log In</button>
#     </form>"""


@app.post("/login")
def login_post():
    id = request.form.get("id")
    user = user_finder(id)
    if user is None:
        # return redirect(url_for("login_get"))
        return 'Unauthorized', 401
    elif not check_password_hash(user.password, request.form.get("password")):
        return 'Invalid passcode', 402

    flask_login.login_user(user)
    # return redirect(url_for("index"))
    return 'OK', 200

@app.route("/index")
@flask_login.login_required
def index():
    return f"You are logged in. \n Showing content that's only viewable by you."


@app.route("/logout")
def logout():
    flask_login.logout_user() 
    return "Logged out"

app.run(debug=True, host='0.0.0.0', port=5050)
