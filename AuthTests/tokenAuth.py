from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "sua_chave_secreta"

@app.route('/login', methods=['POST'])
def login():
    # Simulação de login bem-sucedido
    username = request.json.get("username")
    
    if not username:
        return jsonify({"error": "Usuário é obrigatório"}), 400

    # Cria o token com expiração de 10 segundos
    token = jwt.encode({
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})

@app.route('/protegido')
def protegido():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token ausente"}), 401

    try:
        dados = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"mensagem": "Acesso autorizado", "usuario": dados["user"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

if __name__ == '__main__':
    app.run(debug=True)
