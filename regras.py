from experta import *

class Problema(Fact):
    text = Field(str, mandatory=True)
    pass

class Diagnostico(Fact):
    categoria = Field(str, mandatory=True)
    respostaUsuario = Field(str, mandatory=True)
    tentativas = Field(str, mandatory=True)
    pass

class SuporteTecnico(KnowledgeEngine):
    def classificar_categoria(self, texto):
        categorias = {
            "video/imagem": [
                ["nao da video"], ["nada na tela"], ["tela preta"], ["sem sinal"],
                ["resolucao de tela incorreta"], ["tela distorcida"], ["imagem esticada"],
                ["resolucao errada"], ["tela fora do padrao"]
            ],

            "falha_boot": [
                ["placa mae", "problema"], ["bios"], ["nao carrega sistema"],
                ["sistema operacional", "nao inicia"], ["nao inicializa"], ["nao carrega"],
                ["windows"], ["tela azul"], ["crashou"], ["crash"], ["parou de funcionar"]
            ],

            "aquecimento/fonte": [
                ["nao liga"], ["desligou e nao liga mais"], ["sem sinal de vida"],
                ["superaquecimento"], ["esquentando"], ["fazendo barulho"], ["desligando"],
                ["barulho estranho"], ["barulhento"], ["fonte com problema"], ["fonte defeituosa"],
                ["cheiro de queimado"], ["sistema lento"]
            ],

            "firewall": [
                ["firewall"], ["bloqueando acesso"], ["firewall", "barrando"], 
                ["impedindo acesso"]
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

            "armazenamento": [""],

            "perifericos": [""],

            "audio": [""]
        }

        texto = texto.lower()
        for categoria, termos_grupo in categorias.items():
            for termos in termos_grupo:
                if all(t in texto for t in termos):
                    return categoria
        return "categoria_desconhecida"
    
    def perguntar_categoria(self, categoria):
        perguntas = {""}

    @Rule(Problema(text=MATCH.text))
    def analisar_texto(self,text):
        pergunta = text.lower()
        if "não liga" in pergunta or "nao liga" in pergunta:
            self.declare(Sintoma(tipo="nao_liga"))

        if "sem internet" in pergunta or "sem conexão" in pergunta or "sem wifi" in pergunta:
            self.declare(Sintoma(tipo="sem_internet"))


    @Rule(Sintoma(tipo="nao_liga"))
    def tratar_nao_liga(self):
        self.resposta += "Detectado: o computador não liga. Pergunta: O computador faz algum barulho (ventoinha, bip)?\n"

    @Rule(Sintoma(tipo="sem_internet"))
    def tratar_sem_internet(self):
        self.resposta += "Detectado: sem internet. Pergunta: A luz do modem está acesa?\n"
    

    def obter_resposta(self, problema):
        self.reset()
        self.resposta = ""
        self.declare(Problema(text=problema))
        self.run()
        return self.resposta
