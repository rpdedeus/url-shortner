# Local DEV environment setup

## Part 1 - Database Setup

Using Docker destop on Windows

Start Docker image
```
docker run --name url-shortner-postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres
```

List all docker containers
```
docker container ls --all
```

Create DB
```
docker exec -it url-shortner-postgres bash
psql -U postgres
CREATE DATABASE url_shortner;
```

Connect to DB
```
\c url_shortner
```

List schemas
```
SELECT schema_name from information_schema.schemata;
```

Create schema
```
CREATE SCHEMA main;
```

Set search path
```
SET search_path TO main;
```

Create URLS Table
```
CREATE TABLE main.urls (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  og_url varchar(500) NOT NULL,
  url_hash varchar(50) NOT NULL,
  short_url varchar(55) NOT NULL,
  creation_ts TIMESTAMP
);
```


## Part 2 - Application Setup 
Using wsl shell on Windows

Install & activate virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies
```
pip install flask
pip install psycopg2-binary
pip freeze > requirements.txt
```

or

```
pip install -r requirements.txt
```

Configure & Run Flask
```
cd app/
env flask_app=appy.py
flask run
```
