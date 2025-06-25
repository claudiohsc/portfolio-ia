class EcoAgente:
    """
    Um agente lógico simples para gerenciar a energia de um escritório.
    """
    def __init__(self):
        """
        A base de conhecimento (KB) armazena os fatos percebidos.
        As regras são definidas como métodos para manter a lógica organizada.
        """
        self.kb = set()

    def tell(self, percepcoes):
        """
        Adiciona os fatos percebidos à base de conhecimento (KB).
        Este é o processo de TELL.
        """
        self.kb.clear() # Limpa a KB para as novas percepções do momento
        for fato in percepcoes:
            if percepcoes[fato]: # Add apenas fatos que são verdadeiros
                self.kb.add(fato)

    def ask(self):
        """
        Usa a inferência para derivar novas ações e retorna as decisões.
        Este é o processo de ASK.
        """
        acoes = []

        # Regra R1: (PessoaPresente ∧ ¬LuzNaturalSuficiente) ⇒ LigarLuz
        if 'PessoaPresente' in self.kb and 'LuzNaturalSuficiente' not in self.kb:
            acoes.append('Ligar a luz artificial.')

        # Regra R2: (¬PessoaPresente ∨ LuzNaturalSuficiente) ⇒ DesligarLuz
        if 'PessoaPresente' not in self.kb or 'LuzNaturalSuficiente' in self.kb:
            acoes.append('Desligar a luz artificial.')

        # Regra R3: (PessoaPresente ∧ TemperaturaAlta ∧ HorarioExpediente) ⇒ LigarArCondicionado
        if 'PessoaPresente' in self.kb and 'TemperaturaAlta' in self.kb and 'HorarioExpediente' in self.kb:
            acoes.append('Ligar o ar-condicionado.')

        # Regra R4: (¬PessoaPresente ∨ ¬HorarioExpediente) ⇒ DesligarArCondicionado
        if 'PessoaPresente' not in self.kb or 'HorarioExpediente' not in self.kb:
            acoes.append('Desligar o ar-condicionado.')
            
        if not acoes:
            return ["Nenhuma ação necessária. Manter estado atual."]

        return acoes

def simular_cenario(nome_cenario, percepcoes):
    """Função auxiliar para executar e imprimir um cenário de simulação."""
    print(f"--- {nome_cenario} ---")
    print(f"Percepções: {percepcoes}")
    
    agente = EcoAgente()
    agente.tell(percepcoes)
    acoes_inferidas = agente.ask()
    
    print("Ações do Agente:")
    for acao in acoes_inferidas:
        print(f"- {acao}")
    print("-" * 25 + "\n")


# Simulacao

# Cenario 1: Dia de trabalho quente e com pouca luz
cenario_1 = {
    'PessoaPresente': True,
    'LuzNaturalSuficiente': False,
    'TemperaturaAlta': True,
    'HorarioExpediente': True
}
simular_cenario("Cenário 1: Dia de trabalho, quente e escuro", cenario_1)

# Cenario 2: Sala vazia durante o expediente
cenario_2 = {
    'PessoaPresente': False,
    'LuzNaturalSuficiente': True,
    'TemperaturaAlta': True,
    'HorarioExpediente': True
}
simular_cenario("Cenário 2: Sala vazia no horário de expediente", cenario_2)

# Cenario 3: Fim do expediente, mas alguém ficou na sala
cenario_3 = {
    'PessoaPresente': True,
    'LuzNaturalSuficiente': False,
    'TemperaturaAlta': True,
    'HorarioExpediente': False
}
simular_cenario("Cenário 3: Fora do expediente com pessoa na sala", cenario_3)

# Cenario 4: Dia de trabalho com clima agradável e boa luz
cenario_4 = {
    'PessoaPresente': True,
    'LuzNaturalSuficiente': True,
    'TemperaturaAlta': False,
    'HorarioExpediente': True
}
simular_cenario("Cenário 4: Condições ideais de luz e temperatura", cenario_4)