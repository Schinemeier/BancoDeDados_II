from flask import Flask, jsonify
from pymongo import MongoClient
from neo4j import GraphDatabase

# Configuração do Flask
app = Flask(__name__)

# Conexão com MongoDB
client_mongo = MongoClient("mongodb://localhost:27017/")
db_mongo = client_mongo["recomendacoes"]
produtos_collection = db_mongo["produtos"]
clientes_collection = db_mongo["clientes"]

# Conexão com Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "senha123"
driver_neo4j = GraphDatabase.driver(uri, auth=(username, password))

# Função para obter os dados de clientes e suas compras do MongoDB
def obter_dados_cliente(idcliente):
    cliente = clientes_collection.find_one({"idcliente": idcliente})
    compras = cliente.get("compras", [])
    produtos_comprados = []
    
    for compra in compras:
        produto = produtos_collection.find_one({"idprod": compra["idprod"]})
        produtos_comprados.append({
            "produto": produto["produto"],
            "quantidade": compra["quantidade"],
            "valorpago": compra["valorpago"]
        })
    
    return cliente, produtos_comprados

# Função para obter os amigos do cliente a partir do Neo4j
def obter_amigos_cliente(cpf_cliente):
    with driver_neo4j.session() as session:
        result = session.run("""
            MATCH (c:Cliente {cpf: $cpf})-[:AMIGO_DE]->(amigo)
            RETURN amigo.cpf, amigo.nome
        """, cpf=cpf_cliente)
        amigos = [{"cpf": record["amigo.cpf"], "nome": record["amigo.nome"]} for record in result]
    
    return amigos

# API para retornar os dados de cliente, suas compras e seus amigos
@app.route('/dados_cliente/<int:idcliente>', methods=['GET'])
def dados_cliente(idcliente):
    # Buscar dados do cliente no MongoDB
    cliente, produtos_comprados = obter_dados_cliente(idcliente)
    
    # Buscar amigos do cliente no Neo4j
    amigos = obter_amigos_cliente(cliente["cpf"])
    
    # Estruturar a resposta
    response = {
        "cliente": {
            "nome": cliente["nome"],
            "email": cliente["email"],
            "endereco": cliente["endereco"]
        },
        "compras": produtos_comprados,
        "amigos": amigos
    }
    
    return jsonify(response)

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
