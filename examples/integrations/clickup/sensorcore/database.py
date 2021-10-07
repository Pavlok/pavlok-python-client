# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2

dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("sensorcore_db_host")
DB_PORT = os.environ.get("sensorcore_db_port")
DB_NAME = os.environ.get("sensorcore_db_name")
DB_USERNAME = os.environ.get("sensorcore_db_username")
DB_PASSWORD = os.environ.get("sensorcore_db_password")


def db():
    return psycopg2.connect(
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )


def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)

    try:
        r = [
            dict((cur.description[i][0], value) for i, value in enumerate(row))
            for row in cur.fetchall()
        ]
        cur.connection.close()
        return (r[0] if r else None) if one else r
    except Exception:
        cur.connection.commit()
        cur.connection.close()
        return None


