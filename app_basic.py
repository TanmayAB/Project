import MySQLdb as mdb
import sys
import os
import unicodedata
from flask import Flask, render_template, request,redirect, url_for

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/",methods=["GET"])
def start():
	return render_template("index.html")

@app.route("/index",methods=["POST"])
def index():
	text = request.form['Name']
	text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
	print type(text)
	if(len(text)!=9):
                return render_template("index.html")
        flag = True
        for i in text:
                if (i >='0' and i<='9'):
                        continue
                else:
                        print "Only integers are allowed"
                        print "Retry"
                        return render_template("index.html")
	try:
                con = mdb.connect('localhost', 'root', 'root', 'CMPE273');
                cur = con.cursor()
                cur.execute("SELECT * FROM USERS where STUDENT_ID = %s"% text)
                ver = cur.fetchone()
		print ("Insert into USERS VALUES(%s,)" % text)
                if(ver == None):
			string = "NULL";
			print ("Insert into USERS VALUES(%s,%s)" % (text,string))
                        cur.execute("Insert into USERS VALUES(%s,%s)" % (text,string))
                con.commit()
		print "test"
                cur.execute("Select * from USERS")
                ver = cur.fetchall()
                for i in ver:
                        print i
        except mdb.Error, e:
                print "Error %d: %s" % (e.args[0],e.args[1])
                sys.exit(1)

        finally:
                if con:
                        con.close()
	return redirect(url_for('index1',Uid = text))


@app.route("/index1/<Uid>")
def index1(Uid):
	return render_template("upload.html",Uid=Uid)

@app.route("/index1/<Uid>/upload", methods=['POST'])
def upload(Uid):  
	print Uid
	target = os.path.join(APP_ROOT, 'images/')
   	print(target)

    	if not os.path.isdir(target):
        	os.mkdir(target)

    	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		print type(filename)
		destination = "/".join([target, filename])
		print type(destination)
		file.save(destination)
		destination = unicodedata.normalize('NFKD', destination).encode('ascii','ignore')
    	try:
                con = mdb.connect('localhost', 'root', 'root', 'CMPE273');
                cur = con.cursor()
		test = '"'
		query = "UPDATE USERS SET IMAGE_LOCATION = "+test+"%s"%destination+test + " WHERE STUDENT_ID = %s"% (Uid)
		print query
                cur.execute(query)
                ver = cur.fetchone()
		con.commit()
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
                sys.exit(1)

        finally:
                if con:
                        con.close()
    	return render_template("complete.html")

# The file location will stored across the Student Id, so while fetching the file from database, he needs to query wrt to StudentId
# and get the image and compare with the new image.
#
#

if __name__ == "__main__":
    app.run(port=5000, debug=True)
