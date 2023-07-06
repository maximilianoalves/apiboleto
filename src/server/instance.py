import sqlite3
from flask import Flask
from flask_restx import Api


class Server():
    def __init__(self, ):
        db = sqlite3.connect("boletos.db")
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS BOLETOS("
              "id TEXT, name TEXT, amount TEXT, expire_at TEXT, line TEXT, created_at TEXT, url TEXT)")
        
        db.commit()
        c.connection.close()
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       version='1.0',
                       title='boletosAPI',
                       default="boletos",
                       description='API for generate and list brazillians billings',
                       doc='/docs'
                       )

    def run(self, ):
        self.app.run(
            debug=True
        )


server = Server()
