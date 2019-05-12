from flask import Flask, render_template, request, session, redirect, url_for, flash
import datetime
import platform
import subprocess
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/snds'
ALLOWED_EXTENSIONS = set(['mp3','wav'])
MAX_MB = 8

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_MB * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'azzarola'

# 2019-04-29 non funzia
@app.errorhandler(413)
def request_entity_too_large(e):
  return render_template('413.html'), 413

credentials = {
  'tonia':'Alarm',
  'azz': 'azz'
}
socketList = [
  True,
  False,
  True
]
power = 'on'
telegramDict = {
	'botName': 'toniaBot',
	'botKey':  'ldjhfkjsdhfkjsbfkhd',
	'chatKey': 'sjdhfghds'
}

soundList = []
soundCount = {}

@app.template_filter("datetimefilter")
def datetimefilter(value, format='%Y-%m-%d %02H:%02M:%02S'):
  """Convert a datetime to a differentformat."""
  return value.strftime(format)

@app.route("/sounds")
def sounds():
  global soundList
  global soundCount
  if session.get('logged_in'):
    fileListStr = subprocess.check_output(["ls", "-l", "-h", "-tr", "--time-style=long-iso", "static/snds/"])
    fileList=fileListStr.split(b'\n')
    files=[]
    for str in fileList:
      desFile = str.split()
      if len(desFile) >=  4:
        desFile.pop(0)
        desFile.pop(0)
        desFile.pop(0)
        desFile.pop(0)
        desFileAscii = []
        for str in desFile:
          desFileAscii.append(str.decode('utf-8'))
        date = desFileAscii.pop(1)
        time = desFileAscii.pop(1)
        dateTime = date + " " + time
        desFileAscii.append(dateTime)
        fileName = ""
        while len(desFileAscii) > 3:
          fileName += desFileAscii.pop(3) + " "
        fileName = fileName[:-1]  #del last space
        desFileAscii.append(fileName)
        files.append(desFileAscii)
    soundList = []
    n = 0;
    for element in files:
      n += 1
      fileName = element[1]
      soundDict={
        'index':    n,
        'fileName': fileName,
        'size':     element[0],
        'dateTime': element[2],
      }
      soundList.append(soundDict)
      if fileName not in soundCount:
        soundCount[fileName] = 1
    return render_template(
      'sounds.html',
      currentTime = datetime.datetime.now(),
      annoScolas = "18/19",
      title = "tonia alarm web configuration",
      user = session['username'],
      soundList = soundList,
      soundCount = soundCount,
      maxMb = MAX_MB
    )
  else:
    return redirect(url_for('login'))

@app.route("/", methods=['POST', 'GET'])
def login():
  message = ""
  if not session.get('logged_in'):
    session['username'] = None
    nextPage = 'login.html'
    user = ""
    if request.method == 'POST':
      user = request.form['username']
      pw  = request.form['password']
      if user in credentials:
        if credentials[user] == pw:
          session['username'] = user
          session['logged_in'] = True
          return redirect(url_for('confs'))
        else:
          message = "wrong user/Pw"
      else:
        if user != "":
          message = "wrong User/pw"
        user = ""
    else:
      message = ""
    return render_template(
      nextPage,
      user = user,
      currentTime = datetime.datetime.now(),
      annoScolas = "18/19",
      title = "tonia alarm web configuration",
      message = message
    )
  else:
    return redirect(url_for('confs'))
  
@app.route("/logout")
def logout():
  session['logged_in'] = False
  session['username'] = None
  session.clear()
  return redirect(url_for('login'))

@app.route('/session')
def sessionGet():
  sessionDict = {
    'username':session['username'],
    'logged_in': session.get('logged_in')
  }
  sessionDict['request.endpoint'] = request.endpoint
  for key, values in request.environ.items():
    sessionDict[key]=values
  sessionDict['path'] = request.path
  return render_template(
    'session.html',
    currentTime = datetime.datetime.now(),
    title = "read session vars",
    sessionDict = sessionDict,
    user = session['username']
  ) 

@app.route('/enviro')
def enviroGet():
  return render_template(
    'enviro.html',
    currentTime = datetime.datetime.now(),
    title = "read running environment vars",
    appDict = app.config,
    user = session['username']
  ) 

@app.route('/confs')
def confs():
  return render_template(
    'confs.html',
    currentTime = datetime.datetime.now(),
    socketList = socketList,
    telegramDict = telegramDict,
    power = power,
    title = "configure tonia alarm",
    user = session['username']
  ) 

@app.route('/halt')
def halt():
    shutdown_server()
    return 'python ' + platform.python_version() + ' by by ...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
    func()


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  global soundCount
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('no file part')
      return redirect(url_for('sounds'))
    # if user does not select file, browser also
    # submit an empty part without filename
    file = request.files['file']
    if file.filename == '':
      flash('no selected file')
      return redirect(url_for('sounds'))
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      soundCount[filename] = 1
      return redirect(url_for('sounds'))
  else:
    flash('no get')
    return redirect(url_for('sounds'))
  flash('denied file type')
  return redirect(url_for('sounds'))

@app.route('/delFile/<string:fileName>')
def delFile(fileName):
  global soundCount
  subprocess.call(["rm", "static/snds/" + fileName])
  soundCount.pop(fileName)
  return redirect(url_for('sounds'))

@app.route('/console')
def console():
  return ""

@app.route('/myConsole')
def myConsole():
  return render_template('myConsole.html')

@app.route('/aj/power')
def changePower():
  global power
  if power == 'on':
    power='off'
  else:
    power = 'on'
  return render_template(
    '/aj/power.html',
    power = power
  )

@app.route('/aj/socket/<string:socket>')
def changeSocket(socket):
  global socketList
  n = int(socket[-1:])
  if socketList[n] == True:
    socketList[n] = False
  else:
    socketList[n] = True
  return render_template(
    '/aj/socket.html',
    socket = socketList[n],
    n = n
  )

@app.route('/aj/changeCount/<string:fileName>/<string:newCount>')
def changeCount(fileName,newCount):
  global soundCount
  soundCount[fileName]=int(newCount)
  return render_template(
    '/aj/changeCount.html',
    newCount = newCount
  )

if __name__ == '__main__':

  # flask on default port 5000 only on localhost
  app.run(debug=True, port=2222, host='0.0.0.0')
  # flask on all interfaces
  # app.run(debug=True, host='0.0.0.0')
  # flask on other port > 1024
  # app.run(debug=True, port=5555)
