from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1999'
app.config['MYSQL_DB'] = 'Funcionarios'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)


@app.route('/funcionarios/registros', methods=['GET'])
def get_persons():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM funcionarios")
    funcionarios = cur.fetchall()
    cur.close()
    return jsonify([{'id': f[1], 'cargo': f[2], 'cargo': f[3]} for f in funcionarios])


@app.route('/funcionarios/cadastro', methods=['POST'])
def create_person():
    if request.args:
        name = request.args.get('name')
        cargo = request.args.get('cargo')
    else:
        name = request.json['name']
        cargo = request.json['cargo']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO funcionario (name, cargo) VALUES (%s, %s)", (name, cargo))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Funcionario criado com sucesso'})


@app.route('/funcionarios/deletar', methods=['DELETE'])
def delete_person():
    if request.args:
        name = request.args.get('name')
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM funcionario WHERE name = %s", (name,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Funcionario excluido com sucesso'})
    else:
        id = request.args.get('id')
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM funcionario WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Funcionario excluido com sucesso'})


if __name__ == '__main__':
    app.run(debug=True)
