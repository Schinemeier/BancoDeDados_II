from flask import Flask, jsonify, request
from pymongo import MongoClient
from neo4j import GraphDatabase

# Configuração da API
app = Flask(__name__)

# Conexão com MongoDB (Base 1: Orientado a Documentos)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['recomendacoes']
produtos_col = mongo_db['produtos']
clientes_col = mongo_db['clientes']

# Conexão com Neo4j (Base 2: Orientado a Grafos)
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Função para recuperar dados de amigos de um cliente no Neo4j
def get_amigos(cpf):
    with neo4j_driver.session() as session:
        query = """
        MATCH (c:Cliente {cpf: $cpf})-[:AMIGO_DE]-(amigo:Cliente)
        RETURN amigo.cpf AS cpf, amigo.nome AS nome, amigo.telefone AS telefone,
               amigo.cidade AS cidade, amigo.uf AS uf
        """
        result = session.run(query, cpf=cpf)
        amigos = [record.data() for record in result]
    return amigos

# Rota para buscar dados do cliente e suas compras
@app.route('/cliente/<int:idcliente>', methods=['GET'])
def get_cliente(idcliente):
    cliente = clientes_col.find_one({"dados.idcliente": idcliente})
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    # Dados do cliente
    cliente_data = cliente['dados']
    
    # Recuperar amigos (Neo4j)
    amigos = get_amigos(cliente_data['cpf'])

    # Montar resposta
    response = {
        "cliente": {
            "idcliente": cliente_data['idcliente'],
            "cpf": cliente_data['cpf'],
            "nome": cliente_data['nome'],
            "email": cliente_data['email'],
            "endereco": cliente_data['endereco'],
            "compras": cliente_data.get('compras', [])
        },
        "amigos": amigos
    }
    return jsonify(response)

# Rota para buscar todos os clientes (incluindo seus amigos e compras)
@app.route('/clientes', methods=['GET'])
def get_todos_clientes():
    clientes = list(clientes_col.find())
    response = []

    for cliente in clientes:
        cliente_data = cliente['dados']
        amigos = get_amigos(cliente_data['cpf'])
        response.append({
            "cliente": {
                "idcliente": cliente_data['idcliente'],
                "cpf": cliente_data['cpf'],
                "nome": cliente_data['nome'],
                "email": cliente_data['email'],
                "endereco": cliente_data['endereco'],
                "compras": cliente_data.get('compras', [])
            },
            "amigos": amigos
        })
    return jsonify(response)

# Inicializar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
