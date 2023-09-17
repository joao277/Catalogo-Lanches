import mysql.connector
from flask import Flask, make_response, jsonify, request
import os


mydb = mysql.connector.connect(
    host='us-cdbr-east-06.cleardb.net',
    user='b8ee15cbf50781',
    password='ff526b3e',
    database='heroku_2b554b750211586',
)

app = Flask(__name__)

@app.route('/salgados', methods=['GET']) #Decorator
def get_salgados():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Salgados")
    salgados_disp = cursor.fetchall()

    Salgados = list() #Cria uma lista com as informações do banco de dados e coloca 'id', 'nome' e 'quantidade' na frente de cada dado.
    for salgado in salgados_disp:
        Salgados.append(
            {
                'id':salgado[0],
                'nome':salgado[1],
                'quantidade':salgado[2]
            }
        )

    return make_response(
        jsonify(
            message='Lista de Salgados',
            data=Salgados #Retorna a lista criada anteriormente.
        )
    )

@app.route('/criarsalgado', methods=['POST']) #Decorator
def create_salgado():
    salgado = request.json
    
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO Salgados (nome, quantidade) VALUES (%s, %s)",(salgado['nome'], salgado['quantidade']))
    mydb.commit() #Realiza commit do salgado criado.

    return make_response(
        jsonify(
            message='Salgado cadastrado com Sucesso!',
            data=salgado #Retorna os dados do salgado criado para visualização do usuario.
        )
    )

@app.route('/editsalgado/<id>', methods=['PUT'])
def update_salgado(id):
    cursor = mydb.cursor(dictionary=True)

    # Recupere os dados do corpo da solicitação JSON
    salgado = request.get_json()

    # Atualize o registro com base no ID fornecido
    update_query = "UPDATE Salgados SET nome = %s, quantidade = %s WHERE id = %s"
    cursor.execute(update_query, (salgado['nome'], salgado['quantidade'], id))
    mydb.commit() #Realiza commit do salgado editado.

    return make_response(
        jsonify(
            message=f'Salgado com ID {id} atualizado com sucesso',
            data=salgado #Retorna os dados do salgado editado para visualização do usuario.
        )
    )

@app.route('/deletesalgado/<id>', methods=['DELETE'])
def delete_salgado(id):
    cursor = mydb.cursor()

    # Exclua o registro com base no ID fornecido na url
    delete_query = "DELETE FROM Salgados WHERE id = %s"
    cursor.execute(delete_query, (id,))
    mydb.commit() #Realiza commit do registro excluido para o banco

    return make_response(
        jsonify(
            message=f'Salgado com ID {id} excluído com sucesso' #Confirmação de sucesso para o usuario.
        )
    )

# Obtém a porta do ambiente ou usa a porta 5000 como padrão
port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)