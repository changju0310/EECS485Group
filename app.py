from flask import *
import MySQLdb
import MySQLdb.cursors
import controllers 
from extensions import *
from werkzeug.utils import secure_filename
import os
import hashlib
from flask import Flask, request, redirect, url_for, flash

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['png','jpg','bmp','gif'])

app = Flask (__name__)
#print results_username[0]['username']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/7dzyltg7/p1')    
def Hello():
	
	db = connect_to_database()
	cur = db.cursor()
	cur.execute('SELECT username FROM User')
	results_username = cur.fetchall()

	return render_template('index.html', test=results_username)

app.register_blueprint(controllers.albums, url_prefix='/7dzyltg7/p1')
app.register_blueprint(controllers.album, url_prefix='/7dzyltg7/p1')
app.register_blueprint(controllers.pic, url_prefix='/7dzyltg7/p1')

if __name__ == '__main__':
	app.run(host=config.env['host'], port=config.env['port'], debug=True)

