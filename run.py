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
    current_time=datetime.datetime.now(),
    title="tonia alarm web configuration"
  )


@app.route("/validate", methods=['POST'])
def validate():
  if request.method == 'GET':
    return 'no get method, only post'
  else:
    username = request.form['username']
    password = request.form['password']
    return username + ' '  + password


@app.route('/shutdown')
def shutdown():
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
