from flask import Flask, render_template, request, jsonify
from regras import SuporteTecnico, Problema, Diagnostico 

app = Flask(__name__)
engine = SuporteTecnico()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensagem = data.get('mensagem', '')
    resposta = data.get('resposta', '')
    categoria = data.get('categoria', '')
    tentativas = data.get('tentativas', 0)

    engine.reset()

    if mensagem:
        engine.declare(Problema(texto=mensagem))
        engine.run()
        return jsonify({
            "resposta": resposta,
            "categoria": engine.ultima_categoria,
            "tentativas": 1
        })
    elif resposta:
        engine.declare(Diagnostico(categoria=categoria, respostaUsuario=resposta, tentativas=int(tentativas)))
        engine.run()
        return jsonify({"resposta": engine.ultima_resposta,
                        "tentativas": int(tentativas) + 1 if "Tentando nova solução" in engine.ultima_resposta else 0
                        })

    return jsonify({"resposta": "Dados incompletos"})


if __name__ == "__main__":
    app.run(debug=True)
