from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def testing():
    return 'test'


@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello '+ name + '!'


def factors(num):
  return [x for x in range(1, num+1) if num%x==0]


@app.route('/factors/<int:num>')
def factors_route(num):
    return "The factors of {} are {}".format(num, factors(num))



if __name__ == '__main__':
  app.run(host='0.0.0.0')



