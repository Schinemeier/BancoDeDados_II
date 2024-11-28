# BancoDeDados_II

Um site de recomendação de compras precisa integrar duas bases de
dados. O sistema consiste em recomendar as compras para os amigos
dos clientes. A cada compra, o site solicita ao cliente a indicação de
um amigo. Os dados dos clientes e seus amigos são armazenados em
uma base de dados orientada a documentos.


## BASE 1: Orientado a documentos

Na primeira base de dados, a relacional, ficam armazenados os dados dos clientes e das suas compras.
Os documentos devem ter o seguinte formato:

* Coleção Produtos:
{idprod: 1000, produto: “descrição do produto”, quantidade: 1000, preco: 989}

* Coleção Cliente:
dados: {idcliente: 9, cpf: 123456789, nome: “Maria Dias”,
email:”mariadias@gmail.com”,
endereco: {rua: “Av das Nações”, numero: 345, 
complemento:“dados do complemento”, cidade: “São Paulo”, uf: “SP”, cep: “011111-110”},
compras: {idcompra:1009, idprod: 1000, data:”2024-10-19”,
quantidade: 1, valorpago: 1002,45}}

## BASE 2: Orientado a grafos
O banco de dados orientado a grafos deve armazenar dados dos clientes
e de seus amigos, indicando a relação de amizade entre eles.

Os objetos desse banco de dados devem ter os seguintes atributos:
cpf, nome, telefone, cidade, uf.

## Camada de integração
Implemente em uma linguagem de programação qualquer, uma API que
recupere os dados dos clientes, de suas compras e os dados de seus
amigos, retornando estes dados.