"""
DB Pool handling: https://medium.com/@thegavrikstory/manage-raw-database-connection-pool-in-flask-b11e50cbad3
"""

from contextlib import contextmanager
import sys
from flask import Flask
from flask import Response
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
import psycopg2
import yaml

class BuildingsApi(Flask):
    def __init__(self, config_path):
        super().__init__(__name__)
        self.app_config = self._load_config(config_path)
        self.db_pool = ThreadedConnectionPool(1, 20, **self.app_config['db'])
        self.route('/')(self.index)
        self.route('/buildings')(self.buildings)
        self.route('/buildings/<building_id>')(self.building_get)

    def _load_config(self, cfg_path):
        with open(cfg_path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                sys.exit(exc)

    @contextmanager
    def _get_db_connection(self):
        try:
            connection = self.db_pool.getconn()
            yield connection
        finally:
            self.db_pool.putconn(connection)

    @contextmanager
    def _get_db_cursor(self, commit=False):
        with self._get_db_connection() as connection:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                if commit:
                    connection.commit()
            finally:
                cursor.close()

    def index(self):
        content = "{'message':'Hello world!'}"
        return Response(content, mimetype='text/json')

    def buildings(self):
        with self._get_db_cursor() as cursor:
            buildings = db_buildings_all(cursor)
            return Response(str(buildings), mimetype='text/json')
        return Response("Database error", status_code=500)

    def building_get(self, building_id):
        with self._get_db_cursor() as cursor:
            building = db_buildings_get(cursor, building_id)
            return Response(str(building), mimetype='text/json')
        return Response("Database error", status_code=500)

def db_buildings_all(cursor):
    """ Gets all buildings from the database
    """
    cursor.execute("SELECT id, name, height, city, country FROM buildings")
    return cursor.fetchall()

def db_buildings_get(cursor, building_id):
    """ Gets a specific building from the database
    """
    cursor.execute("SELECT id, name, height, city, country FROM buildings WHERE id = {}".format(building_id))
    return cursor.fetchone()

def main():
    """ Main entrypoint for Building API
    """
    config_path = sys.argv[1]
    app = BuildingsApi(config_path)
    app.run()
