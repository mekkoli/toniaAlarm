from flask import Flask, render_template, request
import datetime
import platform

app = Flask(__name__)

@app.template_filter("datetimefilter")
def datetimefilter(value, format='%Y-%m-%d %02H:%02M:%02S'):
  """Convert a datetime to a differentformat."""
  return value.strftime(format)

@app.route("/")
def login():
  return render_template(
    'login.html',
    currentTime = datetime.datetime.now(),
    annoScolas = "18/19",
    title = "tonia alarm web configuration"
  )

@app.route("/home", methods=['POST', 'GET'])
def home():
  if request.method == 'POST':
    username = request.form['username'],
    password = request.form['password']
  else:
    username = ("none","no user")
  return render_template(
    'template.html',
    currentTime = datetime.datetime.now(),
    title = "tonia alarm web configuration",
    user = username[0]
  )

@app.route("/getAlarmStatus")
def getAlarmStatus():
  return render_template(
    'template.html',
    currentTime = datetime.datetime.now(),
    title = "tonia alarm status"
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
  #flask on default port 5000 only on localhost
  app.run(debug=True)
  
  # flask on all interfaces
  # app.run(debug=True, host='0.0.0.0')
  
  # flask on other port > 1024
  # app.run(debug=True, port=5555)
