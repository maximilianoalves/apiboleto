# Boleto API

### Requirements

- [python](https://www.python.org/downloads/)

- Install Libs
    - pip install flask
    - pip install flask_restx
    - pip install requests

- Installing dependencies by pipreqs
    - pip3 install pipreqs

- Run the APIs
    - Inside of your main folder run: python -m main.py

### HTTP Collection

- GET boletos
    - ```
      curl --location 'localhost:5000/boletos/'```
- GET boletos by id
    - ```
      curl --location 'localhost:5000/boletos/588930'```
- POST add boleto
    - ```
      curl --location 'localhost:5000/boletos' \
        --header 'Content-Type: application/json' \
        --data '{
            "fullName": "Harry Potter",
            "cpf": "39024409020",
            "state": "RS",
            "city": "Sapucaia do sul",
            "zipcode": "93210220",
            "address": "Rodrigues Alves, 300",
            "neighborhood": "Diehl",
            "amount": 572.35,
            "expireDate": "10/07/2023"
        }'```
