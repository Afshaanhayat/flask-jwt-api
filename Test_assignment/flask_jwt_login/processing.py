# -*- coding:utf8 -*-
from flask import current_app, request

# use jwt module
import jwt

# get token with id and password
# return jwt token
# pass id and password parameters to authentification handler(auth_handler)
def process_login(id, pw):
	user = current_app.extensions['jwt'].auth_handler(id, pw)
	if user is None:
		return None

	token = jwt.encode(user.__dict__, \
		current_app.config["JWT_SECRET_KEY"], \
		algorithm=current_app.config["HASH_ALGORITHM"])

	return token
