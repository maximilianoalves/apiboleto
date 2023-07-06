import requests
import json
import sqlite3

class GenerateBoletos():
    
    def generate(person_name, cpf, state, city, zipcode, address, neighborhood, amount, expire_date):
        endpoint = "https://api-sandbox.kobana.com.br/v1/bank_billets"
        api_key = "Bearer ylnxoHmO8yr3JtRfH29ukjjzykB7cXGlDuAyFADVSEA"
        headers = {
            "accept": "application/json",
            "authorization": api_key,
            "content-type": "application/json"
        }
        data_inputed = {
            'interest_type': 0,
            'interest_days_type': 0,
            'fine_type': 0,
            'discount_type': 0,
            'charge_type': 1,
            'dispatch_type': 1,
            'document_type': '02',
            'acceptance': 'N',
            'prevent_pix': 'false',
            'instructions_mode': 1,
            'customer_person_name': person_name,
            'customer_cnpj_cpf': cpf,
            'customer_state': state,
            'customer_city_name': city,
            'customer_zipcode': zipcode,
            'customer_address': address,
            'customer_neighborhood': neighborhood,
            'amount': amount,
            'expire_at': expire_date
            }
        # date format"02/10/2023"
        r = requests.post(url=endpoint, headers=headers, json=data_inputed)
        return r.json()
    
    def addBoleto(id, person_name, amount, expire_at, line, created_at, url):
        db = sqlite3.connect("boletos.db")
        c = db.cursor()
        c.execute("INSERT INTO BOLETOS VALUES(?,?,?,?,?,?,?)",
              (id, person_name, amount, expire_at, line, created_at, url))
        db.commit()
        db.close()