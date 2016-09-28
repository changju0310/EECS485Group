from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *

albums = Blueprint('albums', __name__, template_folder='templates')


@albums.route('/albums', methods = ['GET', 'POST'])
def albums_route():
	test_username = request.args.get('username', 'default_value')

	db = connect_to_database()
	cur = db.cursor()
	cur.execute('SELECT * FROM Album')
	results_albums = cur.fetchall()

	return render_template('albums.html', username = test_username, Albums = results_albums)


@albums.route('/albums/edit', methods = ['GET', 'POST'])
def albums_edit_route():
	if 'default_value' != request.form.get('username', 'default_value'):
		
		test_username = request.form.get('username', 'default_value')
		db = connect_to_database()
		cur = db.cursor()
		cur.execute('SELECT * FROM Album')
		results_albums = cur.fetchall()
		
		return render_template('albumsEdit.html', username = test_username, Albums = results_albums)

	elif 'default_value' != request.form.get('DELETE', 'default_value'):
		
		test_albumid=request.form.get('DELETE', 'default_value')		
		
		db = connect_to_database()
		cur = db.cursor()
		cur.execute("SELECT * FROM Album WHERE albumid='%s'" %test_albumid)
		albumInfo = cur.fetchall()
		cur.execute("DELETE FROM Album WHERE albumid='%s'" %test_albumid)
		cur.execute('SELECT * FROM Album')
		results_albums = cur.fetchall()
		
		return render_template('albumsEdit.html', username = albumInfo[0]['username'],Albums = results_albums)

	elif 'default_value' != request.form.get('ADD', 'default_value'):
		
		test_username = request.form.get('ADD', 'default_value')
		test_title = request.form.get('title', 'default_value')
		
		db = connect_to_database()
		cur = db.cursor()
		cur.execute("INSERT INTO Album (title, username) VALUES ('%s','%s')" %(test_title,test_username))
		cur.execute('SELECT * FROM Album')
		results_albums = cur.fetchall()
		
		return render_template('albumsEdit.html', username = test_username, Albums = results_albums)

	else :
		print request.form
		return render_template('albumsEdit.html', username = 'SUCCESS SUCCESS')	



