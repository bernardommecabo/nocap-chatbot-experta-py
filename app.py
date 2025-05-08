from flask import Flask, render_template, request, jsonify
from regras import SuporteTecnico  

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensagem = data["mensagem"]

    engine = SuporteTecnico()
    resposta = engine.obter_resposta(mensagem)

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
