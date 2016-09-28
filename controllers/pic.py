from flask import *
import MySQLdb
import MySQLdb.cursors
from extensions import *

pic = Blueprint('pic', __name__, template_folder='templates')


@pic.route('/pic', methods = ['GET', 'POST'])
def pic_route():
	if 'default_value' != request.args.get('picid', 'default_value'):
		test_picid = request.args.get('picid', 'default_value')

		db = connect_to_database()
		cur = db.cursor()
		cur.execute("SELECT * FROM Contain WHERE picid='%s'" %test_picid)
		results_search = cur.fetchall()

		test_albumid = results_search[0]['albumid']

		cur.execute("SELECT * FROM Contain WHERE albumid='%s'" %test_albumid)
		test_contain_selected = cur.fetchall()

		return render_template('pic.html', albumid = test_albumid, picid =test_picid, Contain = test_contain_selected)

	else:
		return render_template('pic.html', picid = 'Success Success')
