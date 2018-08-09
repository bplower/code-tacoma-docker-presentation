import sys
from flask import Flask
from flask import Response
import yaml

app = Flask('buildings-api')

@app.route('/')
def index():
    content = "{'message':'Hello world!'}"
    return Response(content, mimetype='text/json')

@app.route('/buildings')
def buildings():
    content = "{'message':'all buildings'}"
    return Response(content, mimetype='text/json')

@app.route('/buildings/<building_id>')
def building_get():
    return ''
    content = "{'message':'particular building'}"
    return Response(content, mimetype='text/json')

def load_config(cfg_path):
    with open(cfg_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            sys.exit(exc)

def main():
    #conn = psycopg2.connect(database="testdb", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")
    config = load_config(sys.argv[1])
    app.run(host=config['host'], port=config['port'])
