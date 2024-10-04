from dotenv import load_dotenv
from flask import Flask
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import os


load_dotenv()


connector = None
db = None
app = Flask(__name__)


def init_pool(connector):
    def getconn():
        connection = connector.connect(
            os.environ.get("INSTANCE_CONNECTION_NAME"),
            "pg8000",
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            db=os.environ.get("DB_NAME"),
            ip_type=IPTypes.PRIVATE
        )
        return connection

    # create connection pool
    engine = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn)
    return engine


def test_db():
    global connector, db
    if not db:
        connector = Connector()
        db = init_pool(connector)
    # build connection for db using Python Connector
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT NOW()")).fetchone()
    print("Successfully connected to Cloud SQL instance!")
    return str(result[0])


@app.route("/")
def hello_world():
    return test_db()


if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("APP_PORT", 8080)))
    print(test_db())