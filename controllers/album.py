from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *
import hashlib
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename



def picidCreated(albumid, filename):
	m = hashlib.md5()
	m.update(str(albumid))
	m.update(filename)
	return m.hexdigest()

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['png','jpg','bmp','gif','PNG','JPG','BMP','GIF'])

def allowed_file(filename):
   	return '.' in filename and \
   		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

album = Blueprint('album', __name__, template_folder = 'templates')

@album.route('/album', methods = ['GET', 'POST'])
def album_route():
	test_albumid = int(request.args.get('albumid', 'default_value'))

	dbSearch = connect_to_database()
	curSearch = dbSearch.cursor()
	curSearch.execute('SELECT title, albumid FROM Album')
	results_search = curSearch.fetchall()

	for items in results_search:
		if items['albumid'] == test_albumid:
			test_title = items['title']

	db = connect_to_database()
	cur = db.cursor()
	cur.execute('SELECT * FROM Contain')
	results_contain = cur.fetchall()

	return render_template('album.html', album_title = test_title,albumid = test_albumid, Contain = results_contain)

@album.route('/album/edit', methods = ['GET', 'POST'])
def album_edit_route():
	#file = request.files['file']
	#print file
	if request.files:
		file = request.files['fileUpload']
		if file.filename == '':

			return render_template('pic.html', picid = 'False')

		#print file.filename
		if file and allowed_file(file.filename):
			test_albumid = request.form.get('file','default_value')

			filename = picidCreated(test_albumid, file.filename)	

			db = connect_to_database()
			cur = db.cursor()
			cur.execute("SELECT COUNT(*) FROM Contain")
			sequencenum = cur.fetchall()
			sequencenum = sequencenum[0]['COUNT(*)']
			
			cur.execute("INSERT INTO Photo (picid,format) VALUES ('%s','JPG')" %filename)
			cur.execute("INSERT INTO Contain (sequencenum, albumid, picid) VALUES ('%d','%s', '%s')" %(long(sequencenum), test_albumid, filename))

			filename = filename + '.jpg'

			file.save(os.path.join('./static/images/', filename))
			
			cur.execute('SELECT * FROM Contain')
			results_contain = cur.fetchall()
			
			cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
			results_search = cur.fetchall()
			for items in results_search:
				if items['albumid'] == long(test_albumid):
					results_title = items['title']
				
			return render_template('albumEdit.html', albumid = long(test_albumid), album_title = results_title, Contain = results_contain)
			#return render_template('pic.html', picid = 'SuccessSuccess')
		return render_template('pic.html', picid = 'False False')
	
	elif 'default_value' != request.form.get('albumid','default_value'): 
		test_albumid = request.form.get('albumid')

		db = connect_to_database()
		cur = db.cursor()
		cur.execute('SELECT * FROM Contain')
		results_contain = cur.fetchall()

		cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
		results_search = cur.fetchall()
		for items in results_search:
			if items['albumid'] == long(test_albumid):
				results_title = items['title']

		return render_template('albumEdit.html', album_title = results_title, albumid = long(test_albumid), Contain = results_contain)

	elif 'default_value' != request.form.get('EDIT', 'default_value'):

		test_albumid = request.form.get('EDIT', 'default_value')
		
		db = connect_to_database()
		cur = db.cursor()
		cur.execute('SELECT * FROM Contain')
		results_contain= cur.fetchall()

		cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
		results_search = cur.fetchall()
		for items in results_search:
			if items['albumid'] == long(test_albumid):
				results_title = items['title']
				
		return render_template('albumEdit.html', album_title = results_title, albumid = long(test_albumid), Contain = results_contain)
	
	elif 'default_value' != request.form.get('DELETE', 'default_value'):

		test_picid = request.form.get('DELETE', 'default_value')

		db = connect_to_database()
		cur = db.cursor()
		cur.execute("SELECT * FROM Contain WHERE picid='%s'" %test_picid)
		contain_info = cur.fetchall()
		
		test_albumid = contain_info[0]['albumid']

		cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
		album_info = cur.fetchall()
		test_title = album_info[0]['title']

		imagesName = test_picid + '.jpg'
		cur.execute("DELETE FROM Contain WHERE picid='%s'" %test_picid)
		os.system("cd static/images && rm '%s'" %imagesName)
		
		cur.execute('SELECT * FROM Contain')
		
		results_contain = cur.fetchall()

		return render_template('albumEdit.html', album_title = test_title, albumid = long(test_albumid), Contain = results_contain)

	else:
		return render_template('album.html', album_title = 'Album')




	