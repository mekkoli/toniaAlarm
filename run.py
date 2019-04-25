from flask import Flask, render_template, request, session, redirect, url_for
import datetime
import platform

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'azzarola'
credentials = {
  'tonia':'Alarm',
  'azz': 'azz'
}

@app.template_filter("datetimefilter")
def datetimefilter(value, format='%Y-%m-%d %02H:%02M:%02S'):
  """Convert a datetime to a differentformat."""
  return value.strftime(format)

@app.route("/home")
def home():
  if session.get('logged_in'):
    return render_template(
      'sounds.html',
      currentTime = datetime.datetime.now(),
      annoScolas = "18/19",
      title = "tonia alarm web configuration",
      user = session['username']
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
          return redirect(url_for('getAlarmStatus'))
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
    return redirect(url_for('getAlarmStatus'))
  
@app.route("/logout")
def logout():
  session['logged_in'] = False
  session['username'] = None
  session.clear()
  return redirect(url_for('login'))

@app.route("/getAlarmStatus")
def getAlarmStatus():
  if session.get('logged_in'):
    return render_template(
      'status.html',
      currentTime = datetime.datetime.now(),
      title = "get alarm status",
      user = session['username']
    )
  else:
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

@app.route('/halt')
def halt():
    shutdown_server()
    return 'python ' + platform.python_version() + ' by by ...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':

  # flask on default port 5000 only on localhost
  app.run(debug=True, port=2222)
  # flask on all interfaces
  # app.run(debug=True, host='0.0.0.0')
  # flask on other port > 1024
  # app.run(debug=True, port=5555)
