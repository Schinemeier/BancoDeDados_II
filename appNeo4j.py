from neo4j import GraphDatabase

# Conectar ao Neo4j
# Definir a URL e credenciais do Neo4j
URI = "bolt://localhost:7687"  # URL do Bolt
USERNAME = "banco"  # Usuário padrão
PASSWORD = "banco123"  # Substitua pela sua senha

# Criar driver de conexão
try:
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    print("Conexão estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao Neo4j: {e}")
    exit()

def criar_cliente(session, cpf, nome, telefone, cidade, uf):
    session.run(
        """
        CREATE (:Cliente {cpf: $cpf, nome: $nome, telefone: $telefone, cidade: $cidade, uf: $uf})
        """,
        cpf=cpf, nome=nome, telefone=telefone, cidade=cidade, uf=uf
    )

def criar_amizade(session, cpf1, cpf2):
    session.run(
        """
        MATCH (a:Cliente {cpf: $cpf1}), (b:Cliente {cpf: $cpf2})
        CREATE (a)-[:AMIGO_DE]->(b)
        """,
        cpf1=cpf1, cpf2=cpf2
    )

# Inserir dados
with driver.session() as session:
    criar_cliente(session, "123456789", "Maria Dias", "11987654321", "São Paulo", "SP")
    criar_cliente(session, "987654321", "João Silva", "21987654321", "Rio de Janeiro", "RJ")
    criar_cliente(session, "456789123", "Ana Costa", "31987654321", "Belo Horizonte", "MG")
    criar_amizade(session, "123456789", "987654321")
    criar_amizade(session, "123456789", "456789123")
    criar_amizade(session, "987654321", "456789123")

# Fechar conexão
driver.close()
