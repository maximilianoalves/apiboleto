from types import NoneType
from flask import *
from flask_restx  import Api, Resource, fields, marshal_with
from src.server.instance import server
from src.models.boletos import Boletos
from src.services.gen_boleto import GenerateBoletos
import sqlite3
import json

app, api = server.app, server.api

resource_fields_success = api.model('Resource', {
    "id": fields.String,
    "person_name": fields.String,
    "amount": fields.String,
    "expire_at": fields.String,
    "line": fields.String,
    "created_at": fields.String,
    "url": fields.String
})


@api.route('/boletos/<boleto_id>', methods=['GET'])
class Boletos(Resource):
    
    @api.response(200, "Success", resource_fields_success)
    @api.response(404, "Not found")
    @api.response(500, "unrecognized token")
    def get(self, boleto_id):
        c = sqlite3.connect("boletos.db")
        try:
             query = c.execute("SELECT * FROM BOLETOS WHERE id="+ boleto_id)
             data = query.fetchone()
             data_result = {
                "id": data[0],
                "person_name": data[1],
                "amount": data[2],
                "expire_at": data[3],
                "line": data[4],
                "created_at": data[5],
                "url": data[6]
            }
             c.close()
             return data_result, 200
        except TypeError as e:
            data = {
                "error": str(e),
                "message": boleto_id+" not found."
            }
            return data, 404
        except sqlite3.OperationalError as e:
            data = {
                "error": str(e),
                "message": boleto_id+" not found."
            }
            return data, 500
        
        
        