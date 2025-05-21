from experta import *
from regras import *

class Cliente(Fact):
    """Fato representando o cliente e seu problema"""
    pass

# classe para definição das regras que serão utilizadas na classe app
class SuporteTecnico(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.resposta = "❌ Problema não identificado. Por favor, descreva seu problema com mais detalhes."

    # para cada uma das regras, percorremos o vetor das palavras que desejamos comparar e verificamos se haverá um match com a entrada do usuário
    # (neste caso a variável x é o que o usuário digitará)
    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_SAUDACOES))))
    def saudacoes(self):
        self.resposta = "😀 Olá! Sou seu assistente de suporte técnico. Por favor, descreva seu problema para que eu possa ajudar."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_BOOT))))
    def problemas_inicializacao(self):
        self.resposta = """💻 Problema de inicialização detectado:
        1. Verifique a conexão de energia:
        - Cabo de força bem conectado
        - Tomada funcionando
        - Luzes do gabinete acesas

        2. Problemas com memória RAM:
        - Tente remover e recolocar os pentes de memória
        - Teste com um pente de cada vez

        3. Verifique o disco rígido:
        - Acesse a BIOS (geralmente apertando DEL ou F2 durante a inicialização)
        - Confira se o HD/SSD está sendo detectado"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_VIDEO))))
    def problemas_video(self):
        self.resposta = """🖥️ Problema de vídeo detectado:
        1. Verifique as conexões físicas:
        - Cabo de vídeo bem conectado (tanto na placa quanto no monitor)
        - Teste com outro cabo se possível

        2. Problemas com placa de vídeo:
        - Se for placa dedicada, verifique os conectores de energia
        - Tente remover e recolocar a placa

        3. Soluções de software:
        - Atualize os drivers da placa de vídeo
        - Reinstale o driver atual"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_FONTE))))
    def problemas_energia(self):
        self.resposta = """🔌 Problema de energia detectado:
        1. Verificação básica:
        - Teste outra tomada
        - Verifique se o cabo de força está intacto
        - Cheque se a fonte está ligada (botão na parte traseira)

        2. Teste da fonte de alimentação:
        - Desconecte todos os componentes desnecessários
        - Tente ligar com apenas o essencial conectado

        3. Possíveis problemas:
        - Fonte queimada (cheque por cheiro de queimado)
        - Superaquecimento (ventoinha da fonte girando?)"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_FIREWALL))))
    def problemas_firewall(self):
        self.resposta = """🛡️ Problema com firewall detectado:
        1. Verificação básica:
        - Temporariamente desative o firewall para testes
        - Verifique se o programa está na lista de permitidos

        2. Configurações avançadas:
        - Verifique as regras de entrada/saída
        - Confira se o antivírus não está bloqueando

        3. Soluções alternativas:
        - Adicione exceções para o programa
        - Atualize o software de segurança"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_SEGURANCA))))
    def problemas_seguranca(self):
        self.resposta = """🦠 Problema de segurança detectado:
        1. Verificação de vírus:
        - Execute uma verificação completa do sistema
        - Atualize as definições de vírus

        2. Problemas com malware:
        - Use o Windows Defender ou seu antivírus
        - Execute ferramentas como Malwarebytes

        3. Prevenção:
        - Não clique em links suspeitos
        - Mantenha seu sistema atualizado"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_SOFTWARE))))
    def problemas_software(self):
        self.resposta = """🧩 Problema de software detectado:
        1. Soluções básicas:
        - Reinicie o programa
        - Reinicie o computador

        2. Atualizações:
        - Verifique atualizações para o software
        - Atualize seu sistema operacional

        3. Reinstalação:
        - Desinstale completamente o programa
        - Baixe a versão mais recente do site oficial"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_REDE))))
    def problemas_rede(self):
        self.resposta = """📶 Problema de rede detectado:
        1. Verificação básica:
        - Reinicie o roteador/modem
        - Verifique se outros dispositivos estão conectados

        2. Soluções para Wi-Fi:
        - Mova-se mais perto do roteador
        - Tente conectar via cabo de rede

        3. Configurações:
        - Verifique se o modo avião está desligado
        - Esqueça a rede e conecte novamente
        - Atualize os drivers de rede"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_ARMAZENAMENTO))))
    def problemas_armazenamento(self):
        self.resposta = """💾 Problema de armazenamento detectado:
        1. Verificação de disco:
        - Execute CHKDSK (Prompt: chkdsk /f C:)
        - Verifique erros com ferramentas como CrystalDiskInfo

        2. Espaço insuficiente:
        - Libere espaço deletando arquivos temporários
        - Desinstale programas não utilizados

        3. Problemas físicos:
        - Verifique os cabos SATA/energia
        - Teste o disco em outro computador"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_DISPOSITIVOS))))
    def problemas_dispositivos(self):
        self.resposta = """🖱️ Problema com dispositivos detectado:
        1. Verificação básica:
        - Reconecte o dispositivo
        - Teste em outra porta USB
        - Tente em outro computador

        2. Problemas com drivers:
        - Atualize os drivers no Gerenciador de Dispositivos
        - Desinstale e deixe o Windows reinstalar

        3. Configurações:
        - Verifique as configurações de energia (USB selective suspend)
        - Teste sem hubs USB (conecte diretamente no PC)"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_AUDIO))))
    def problemas_audio(self):
        self.resposta = """🔊 Problema de áudio detectado:
        1. Verificação básica:
        - Verifique se o som não está mudo
        - Confira o dispositivo de saída selecionado

        2. Problemas com drivers:
        - Atualize drivers no Gerenciador de Dispositivos
        - Reinstale o driver de áudio

        3. Configurações:
        - Verifique o Mixer de Volume (botão direito no ícone de som)
        - Teste em diferentes programas (YouTube, Windows Sounds)"""
        self.halt()