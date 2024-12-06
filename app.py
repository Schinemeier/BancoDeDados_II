# File: app.py

from flask import Flask, jsonify, request
from pymongo import MongoClient
from neo4j import GraphDatabase

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['recomendacoes']
produtos_collection = mongo_db['Produtos']
clientes_collection = mongo_db['Cliente']

# Neo4J configuration
NEO4J_URI = "bolt://54.205.150.161"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "theories-readiness-modifications"
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# Function to get friends from Neo4J
def get_friends(cpf):
    query = """
    MATCH (client:Person {cpf: $cpf})-[:FRIEND]->(friend)
    RETURN friend.cpf AS cpf, friend.nome AS nome, friend.telefone AS telefone,
           friend.cidade AS cidade, friend.uf AS uf
    """
    with neo4j_driver.session() as session:
        result = session.run(query, cpf=cpf)
        return [record.data() for record in result]


# Route to fetch client details and their purchases
@app.route('/cliente/<cpf>', methods=['GET'])
def get_cliente_data(cpf):
    # Get client and purchases from MongoDB
    client_data = clientes_collection.find_one({"dados.cpf": int(cpf)}, {"_id": 0})
    if not client_data:
        return jsonify({"error": "Client not found"}), 404

    # Get friends from Neo4J
    friends = get_friends(cpf)

    # Combine data
    response = {
        "client": client_data['dados'],
        "friends": friends
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
