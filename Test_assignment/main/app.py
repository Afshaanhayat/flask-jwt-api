
from flask import *
from flask import Flask, redirect, request, make_response, abort
from flask_jwt_login import JWT, login_required, process_login
from os import system

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

TOKEN_NAME = 'token'

app.config["SECRET_KEY"] = "super secret"
app.config["JWT_COOKIE_NAME"] = TOKEN_NAME


jwt = JWT(app)

class User():
	def __init__(self, id, pw, name):
		self.id = id
		self.pw = pw
		self.name = name

	def __repr__(self):
		return "User(id=%s, password=%s, name=%s)" % (self.id, self.pw, self.name)

user_table = [
	{'id' : 'tay', 'pw' : '123', 'name' : 'afta'}
]

@jwt.authentication_handler
def authentication_handler(id, pw):
	for row in user_table:
		if row['id'] == id and row['pw'] == pw:
			return User(row['id'], row['pw'], row['name'])

	return None

@jwt.unauthorized_handler
def unauthorized_handler():
	abort(501)

@app.errorhandler(501)
def unauthorized(e):
	return 'Unauthorized Access', 501

@app.route("/")
def main():
	return redirect("login")

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():

	if request.method == "GET":
		return "<form method='post'>" +\
					"<input type='text' name='id'>" +\
					"<input type='password' name='pw'>" +\
					"<input type='submit'>" +\
				"</form>"


	token = process_login(request.form["id"], request.form["pw"])


	if token is not None:

		response = make_response("<a href='/protected'>You Are In!, Click here to upload an Image.<a>")
		response.set_cookie(TOKEN_NAME, token)
		return response
	return "Invalid UserId/Password!"


@app.route("/protected")
@login_required
def protected():
	return render_template("/file_upload_form.html")

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':

        if request.files:
        	image = request.files['file']
        	image.save(image.filename)
        return render_template("success.html", name = image.filename)
if __name__ == "__main__":
	app.run(debug=True)