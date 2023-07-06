from flask import *
from flask_restx  import Api, Resource, fields
from src.server.instance import server
from src.models.boletos import Boletos
from src.services.gen_boleto import GenerateBoletos
import sqlite3
import json

app, api = server.app, server.api

resource_fields_success = api.model('Model', {
    "person_name": fields.String,
    "cpf": fields.String,
    "state": fields.String,
    "city": fields.String,
    "zipcode": fields.String,
    "address": fields.String,
    "neighborhood": fields.String,
    "amount": fields.Integer,
    "expire_date": fields.String
})

resource_fields_expect = api.model('Resource', {
    "id": fields.String,
    "person_name": fields.String,
    "amount": fields.String,
    "expire_at": fields.String,
    "line": fields.String,
    "created_at": fields.String,
    "url": fields.String
})



@api.route('/boletos')
class BoletosList(Resource):

    @api.response(200, "Success", [resource_fields_expect])
    @api.response(404, "Not found")
    def get(self, ):
        c = sqlite3.connect("boletos.db")
        c.row_factory = sqlite3.Row
        data = c.execute("SELECT * FROM BOLETOS").fetchall()
        c.close()
        result = [{k: data[k] for k in data.keys()} for data in data]
        if not result:
            return {"message": "Empty list"}, 404
        else:
            return result, 200
    
    @api.expect(resource_fields_success)
    @api.response(201, "Created", resource_fields_expect)
    def post(self, ):
        try:
            boletos = Boletos(
                request.json["person_name"],
                request.json["cpf"],
                request.json["state"],
                request.json["city"],
                request.json["zipcode"],
                request.json["address"],
                request.json["neighborhood"],
                request.json["amount"],
                request.json["expire_date"]
            )
            result = GenerateBoletos.generate(boletos.person_name, boletos.cpf, boletos.state, 
                                    boletos.city, boletos.zipcode, boletos.address, 
                                    boletos.neighborhood, boletos.amount, boletos.expire_date
                                    )
            GenerateBoletos.addBoleto(result.get("id"), result.get("customer_person_name"),
                                    result.get("amount"), result.get("expire_at"), 
                                    result.get("line"), result.get("created_at"), result.get("shorten_url"))
            data = {
                "id": result.get("id"),
                "person_name": result.get("customer_person_name"),
                "amount": result.get("amount"),
                "expire_at": result.get("expire_at"),
                "line": result.get("line"),
                "created_at": result.get("created_at"),
                "url": result.get("shorten_url")
            }
            return data, 201
        except KeyError as e:
            return {"error": "Wrong key: "+str(e), "message": "Try Again!"}, 400 
    
    