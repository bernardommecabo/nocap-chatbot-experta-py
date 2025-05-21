from flask import Flask, request, jsonify, render_template
from sistema_especialista import SuporteTecnico, Cliente

app = Flask(__name__)

# quando acessamos a raiz do site (/) executa a função index(), que renderiza nosso index.html
@app.route("/")
def index():
    return render_template("index.html")

# essa é a rota da API (/chat), que só permite os methods do tipo POST (envio de dados)
@app.route("/chat", methods=["POST"])
def chat():
    problema = request.json["mensagem"].lower().strip()
    # a variável engine, da biblioteca experta serve para criarmos nosso motor de regras a partir da classe suporte_tecnico importada
    engine = SuporteTecnico()
    engine.reset() # limpamos a base de dados das regras para evitar problemas
    engine.declare(Cliente(problema=problema)) # criamos um "Cliente" para servir de exemplo, será o usuário que estará digitando os problemas
    engine.run() # por fim rodamos o motor de regras

    return jsonify({"resposta": engine.resposta}) # pegamos o json criado no javascript presente no index.html para retornar ao usuário a resposta, baseada na classe sistema_especialista

if __name__ == "__main__":
    app.run(debug=True)