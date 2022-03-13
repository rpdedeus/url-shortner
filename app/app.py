from flask import Flask
from flask import request
import psycopg2
import uuid
import typing
import json
import hashlib 


app = Flask(__name__)


# move to separate file
conn = psycopg2.connect(
    database="url_shortner", user="postgres", password="password", port="5432", host="127.0.0.1")


def gen_hash(str_in: str) -> str:
    return hashlib.md5(str_in.encode('utf-8')).hexdigest()


def get_og_url_by_short_url(short_url: str) -> str:
    cursor = conn.cursor()
    cursor.execute("SELECT og_url FROM main.urls WHERE short_url = %s", (short_url,))
    data = cursor.fetchone()
    return data[0] if data is not None else ""


def get_short_url_by_url_hash(url_hash: str) -> str:
    cursor = conn.cursor()
    cursor.execute("SELECT short_url FROM main.urls WHERE url_hash = %s", (url_hash,))
    data = cursor.fetchone()
    return data if data is not None else ""


def create_new_short_url(og_url: str, url_hash: str) -> str:
    domain = "https://bitly.com/"
    guid = str(uuid.uuid1())
    uri = gen_hash(guid)
    short_url = "{}{}".format(domain, uri)

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO main.urls (og_url, url_hash, short_url, creation_ts) VALUES (%s, %s, %s, now()) ",
        (og_url, url_hash, short_url)
    )
    conn.commit()

    return short_url


@app.route("/api/", methods=["GET"])
def retrieve_short_url():
    short_url = request.args.get("short_url")
    og_url = get_og_url_by_short_url(short_url)
    response_code = 200 if len(og_url) > 0 else 204

    return {"og_url": og_url}, response_code, {"ContentType":"application/json"}


@app.route("/api/", methods=["POST"])
def create_short_url():
    request_data = request.get_json()
    og_url_req = request_data.get("og_url", "")
    url_hash = gen_hash(og_url_req)
    short_url = get_short_url_by_url_hash(url_hash)

    if len(short_url) > 0:
        print("entry exists")
    else:
        print("entry does NOT exist")
        short_url = create_new_short_url(og_url_req, url_hash)

    return {"status": "ok", "short_url": short_url}, 200, {"ContentType":"application/json"}
