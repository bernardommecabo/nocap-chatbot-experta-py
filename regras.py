from experta import *

class Problema(Fact):
    texto = Field(str, mandatory=True)
    pass

class Diagnostico(Fact):
    categoria = Field(str, mandatory=True)
    respostaUsuario = Field(str, mandatory=True)
    tentativas = Field(str, default=0)
    pass

#Cria uma classe chamada SuporteTecnico que herda de KnowledgeEngine
class SuporteTecnico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.ultima_resposta = ""

    # Classifica a categoria do problema com base em palavras-chave
    def classificar_categoria(self, texto):
        categorias = {
            "video/imagem": [
                ["video", "nao exibe"],["tela", "sem imagem"],["tela", "preta"],
                ["tela", "sem sinal"],["resolucao", "incorreta"],["tela", "distorcida"],
                ["imagem", "esticada"],["resolucao", "errada"],["tela", "fora do padrao"]
            ],

            "falha_boot": [
                ["placa mae", "problema"],["bios", "erro"],["sistema", "nao carrega"],
                ["sistema operacional", "nao inicia"],["sistema", "nao inicializa"],["sistema", "nao carrega"],
                ["windows", "falha"],["sistema", "tela azul"],["sistema", "crashou"],
                ["sistema", "crash"],["sistema", "parou"]
            ],

            "aquecimento/fonte": [
                ["computador", "nao liga"],["computador", "desligou e nao liga"],["equipamento", "sem sinal de vida"],
                ["sistema", "superaquecendo"],["sistema", "esquentando"],["equipamento", "fazendo barulho"],
                ["sistema", "desligando"],["equipamento", "barulho estranho"],["equipamento", "barulhento"],
                ["fonte", "com problema"],["fonte", "defeituosa"],["fonte", "cheiro queimado"],["sistema", "lento"]
            ],

            "firewall": [
                ["firewall", "bloqueando acesso"],["acesso", "impedido pelo firewall"],
                ["firewall", "barrando conexao"],["sistema", "acesso bloqueado"]
            ],
            
            "seguranca/malware": [
                ["navegador","lento"],["navegador","travando"],["navegador","com problema"],
                ["virus"],["com malware"],["propaganda"],["pop up"],["site", "travando"],
                ["ameaca","detectada"],["ameaca","bloqueada"],["ameaca","removida"],
                ["sem protecao"],["sem antivirus"],["antivirus","desatualizado"],
                ["programa","desconhecido"],["programa","suspeito"],["programa","malicioso"],
                ["abrindo","sozinho"],["abrindo","sem querer"],["abrindo","sem autorizacao"]
            ],

            "sistema/software": [
                ["faltando","dll"],["erro","dll"],["erro","sistema"],
                ["fechou","sozinho"],["fechando","sozinho"],["travando","sozinho"],
                ["sistema","travando"],["sistema","lento"],["sistema","com problema"],
                ["sistema","com erro"],["sistema","com falha"],["sistema","com bug"],
                ["sistema","lento"],["sisema","devagar"],["baixo", "desempenho"],
                ["erro", "compatibilidade"],["erro","atualizacao"],["erro","instalacao"],
                ["conflito","software"],["conflito","programa"],["conflito","aplicativo"]
            ],

            "rede": [["sem","internet"],["sem","conexao"],["sem","wifi"],["sem","sinal"],
                     ["rede","desconhecida"],["rede","instavel"],["rede","lenta"],["conflito","ip"],
                     ["ip","duplicado"],["problema","ip"],["ip","instavel"],["erro","endereco"],
                     ["problema","modem"],["modem","desconhecido"],["roteador","nao funciona"],
                     ["luz vermelha", "modem"],["luz","modem"],["luz","roteador"],
            ],

            "armazenamento": ["hd"],

            "perifericos": [""],

            "audio": [""]
        }
        
        # Converte o texto para minúsculas para facilitar a comparação
        texto = texto.lower()
        # Itera sobre as categorias e seus respectivos grupos de termos
        # Se todos os termos de um grupo estiverem presentes no texto, retorna a categoria correspondente
        for categoria, termos_grupo in categorias.items():
            for termos in termos_grupo:
                if all(t in texto for t in termos):
                    return categoria
        return "categoria_desconhecida"
    
    # Avalia a expressão lógica com base nas palavras-chave
    def avaliar_expressao(self, condicao, palavras_chave):
        palavras_texto = " ".join(palavras_chave).lower()

        if "&&" in condicao:
            return all(termo.strip() in palavras_texto for termo in condicao.split("&&"))
        elif "||" in condicao:
            return any(termo.strip() in palavras_texto for termo in condicao.split("||"))
        else:
            return condicao.strip() in palavras_texto

    # Pergunta ao usuário sobre a categoria do problema como um metodo de segunda verificação
    # para garantir um melhor entendimento do problema e diagnóstico da maquina    
    def perguntar_categoria(self, categoria, palavras_chave):
            perguntas = {
            "inicialização": [
                ("não liga && cheiro de queimado", "O computador emite algum som ao tentar ligar?"),
                ("tela azul", "Você viu alguma mensagem de erro na tela azul?"),
                ("não dá vídeo", "A tela está totalmente preta ou com mensagem de erro?"),
                ("default", "A luz da fonte ou LED frontal acende?")
            ],
            "superaquecimento": [
                ("superaquecimento || esquentando", "O computador está muito quente ao toque?"),
                ("barulhos estranhos || barulhento", "Você escutou algum ruído incomum vindo do gabinete?"),
                ("default", "Ele desliga sozinho após algum tempo?")
            ],
            "periféricos": [
                ("mouse", "O mouse funciona em outra porta USB?"),
                ("teclado", "O teclado está respondendo em outro computador?"),
                ("default", "O driver do dispositivo está atualizado?")
            ],
            "categoria_desconhecida": [
                ("default", "Poderia descrever melhor o problema?")
            ]
            }
            
            # Perguntas padrão para cada categoria
            perguntas_categoria = perguntas.get(categoria, [("default", "Descreva melhor o seu problema.")])
            feitas = set()

            # Itera sobre as perguntas da categoria e verifica se a condição é atendida
            # Se a condição for atendida e a pergunta ainda não foi feita, imprime a pergunta
            # Se não houver perguntas feitas, imprime a pergunta padrão
            for condicao, pergunta in perguntas_categoria:
                if condicao == "default":
                    continue
                if self.avaliar_expressao(condicao, palavras_chave) and pergunta not in feitas:
                    print(f"❓ {pergunta}")
                    feitas.add(pergunta)
                if not feitas:
                    for chave, pergunta in perguntas_categoria:
                        if chave == "default":
                            print(f"❓ {pergunta}")

    # Avalia a resposta do usuário e decide o que fazer a seguir
    # Se a resposta for positiva, finaliza o atendimento e sugere iniciar outro
    # Se a resposta for negativa, tenta uma nova solução ate o limite de tentativas
    # Se o limite for atingido, recomenda procurar assistência técnica
    def avaliar_resposta_usuario(self, resposta, fila, tentativas):
        positivas = {"funcionou", "ajudou", "corretamente", "satisfeito"}
        negativas = {"não funcionou", "insatisfeito", "erro persiste", "ainda está dando erro"}

        if resposta.lower() in positivas:
            self.ultima_resposta = "✅ Problema resolvido! Deseja iniciar outro atendimento?"
            return "finalizado"
        elif resposta.lower() in negativas:
            tentativas += 1
            if tentativas < len(fila):
                self.ultima_resposta = f"🔁 Tentando nova solução: {fila[tentativas]}"
                return "continuar", tentativas
            else:
                self.ultima_resposta = "❌ Recomendamos procurar uma assistência técnica especializada. Deseja iniciar outro atendimento?"
                return "finalizado"
        else:
            self.ultima_resposta = "❓ Não entendi sua resposta. Pode repetir?"
            return "aguardando_resposta"
    
    # Regra para detectar a categoria do problema
    # e fazer perguntas adicionais para entender melhor o problema
    @Rule(Problema(texto=MATCH.texto))
    def detectar_categoria(self, texto):
        categoria = self.classificar_categoria(texto)
        self.perguntar_categoria(categoria, texto.split())
        print(f"🔍 Categoria identificada: {categoria.upper()}\n")
        self.declare(Diagnostico(categoria=categoria, respostaUsuario='', tentativas=0))
        self.ultima_categoria = categoria

    
    # Regra para diagnosticar o problema com base na categoria e resposta do usuário
    @Rule(Diagnostico(categoria=MATCH.cat, resposta_usuario=MATCH.resp, tentativas=MATCH.tent))
    def diagnosticar(self, cat, resp, tent):
        fila_diagnosticos = {
            "inicialização": ["Verifique a fonte de alimentação", "Teste com outro cabo de energia", "Reset da BIOS"],
            "superaquecimento": ["Limpeza das ventoinhas", "Troca da pasta térmica", "Verificação da fonte de energia"],
            "periféricos": ["Atualizar drivers", "Testar em outra porta", "Testar em outro PC"],
            "armazenamento": ["Verifique o cabo de dados", "Utilize um software de recuperação de arquivos", "Teste outro HD"],
            "rede": ["Reinicie o modem", "Execute o solucionador de problemas de rede", "Atualize o driver de rede"],
            "seguranca/malware": ["Execute uma verificação completa com antivírus", "Remova programas desconhecidos", "Restaure o sistema"]
        }
        fila = fila_diagnosticos.get(cat, ["Sem diagnóstico disponível."])
        resultado = self.avaliar_resposta_usuario(resp, fila, tent)
        # Se o resultado for "continuar", modifica o fato com a próxima tentativa
        # Se o resultado for "finalizado", encerra o atendimento
        if isinstance(resultado, tuple) and resultado[0] == "continuar":
            self.modify(self.facts[fact_id], tentativas=resultado[1])
        elif resultado == "finalizado":
            self.halt()

