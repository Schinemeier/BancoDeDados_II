from pymongo import MongoClient
from datetime import datetime

# Conectando ao MongoDB (supondo que o MongoDB esteja rodando localmente na porta padrão)
client = MongoClient('mongodb://localhost:27017/')
db = client['recomendacao']  # Nome do banco de dados

# Coleções no MongoDB
produtos_collection = db['produtos']
clientes_collection = db['clientes']

# Função para inserir um produto
def inserir_produto(idprod, produto, quantidade, preco):
    produto_data = {
        "idprod": idprod,
        "produto": produto,
        "quantidade": quantidade,
        "preco": preco
    }
    produtos_collection.insert_one(produto_data)
    print(f"Produto {produto} inserido com sucesso.")

# Função para inserir um cliente
def inserir_cliente(idcliente, cpf, nome, email, endereco, compras):
    cliente_data = {
        "idcliente": idcliente,
        "cpf": cpf,
        "nome": nome,
        "email": email,
        "endereco": endereco,
        "compras": compras
    }
    clientes_collection.insert_one(cliente_data)
    print(f"Cliente {nome} inserido com sucesso.")

# Função para registrar uma compra de um cliente
def registrar_compra(idcliente, idcompra, idprod, quantidade, valorpago):
    compra_data = {
        "idcompra": idcompra,
        "idprod": idprod,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "quantidade": quantidade,
        "valorpago": valorpago
    }

    # Atualiza o cliente com a nova compra
    clientes_collection.update_one(
        {"idcliente": idcliente},
        {"$push": {"compras": compra_data}}
    )
    print(f"Compra {idcompra} registrada para o cliente {idcliente}.")

# Função para exibir as compras de um cliente
def exibir_compras_cliente(idcliente):
    cliente = clientes_collection.find_one({"idcliente": idcliente})
    if cliente:
        print(f"Compras de {cliente['nome']}:")
        for compra in cliente['compras']:
            # Exibindo a estrutura da compra para depuração
            # print("Estrutura da compra:", compra)
            
            produto = produtos_collection.find_one({"idprod": compra['idprod']})
            # Verificando se a chave 'data' está presente na compra
            if 'data' in compra:
                print(f"Produto: {produto['produto']}, Quantidade: {compra['quantidade']}, Data: {compra['data']}, Valor Pago: {compra['valorpago']}")
            else:
                print(f"Produto: {produto['produto']}, Quantidade: {compra['quantidade']}, Data: Não encontrada, Valor Pago: {compra['valorpago']}")
    else:
        print("Cliente não encontrado.")

# Função para recomendar produtos para amigos de um cliente
def recomendar_produtos_amigos(idcliente):
    cliente = clientes_collection.find_one({"idcliente": idcliente})
    if cliente:
        print(f"Recomendações de produtos para os amigos de {cliente['nome']}:")
        for compra in cliente['compras']:
            produto = produtos_collection.find_one({"idprod": compra['idprod']})
            print(f"Produto: {produto['produto']}, Preço: {produto['preco']}")

# Exemplo de dados de produtos
inserir_produto(1000, "Notebook Dell", 1000, 4899.99)
inserir_produto(1001, "Smartphone Samsung", 500, 2999.99)

# Exemplo de dados de clientes e compras
cliente_endereco = {
    "rua": "Av das Nações", 
    "numero": 345, 
    "complemento": "dados do complemento", 
    "cidade": "São Paulo", 
    "uf": "SP", 
    "cep": "011111-110"
}

compra1 = {
    "idcompra": 1009, 
    "idprod": 1000, 
    "quantidade": 1, 
    "valorpago": 1002.45
}

inserir_cliente(15, "123456789", "Joao Cunha", "cunha.joao@gmail.com", cliente_endereco, [compra1])

# Registrar uma nova compra
registrar_compra(15, 1010, 1001, 1, 2999.99)

# Exibir compras de um cliente
exibir_compras_cliente(15)

# Recomendar produtos para os amigos de um cliente
recomendar_produtos_amigos(15)
