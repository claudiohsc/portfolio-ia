import copy

class ReformaCSP:
    def __init__(self, tarefas, duracoes, precedencias, prazo_maximo_dias, profissionais_disponiveis=None):
        self.tarefas = tarefas # Lista de nomes das tarefas
        self.duracoes = duracoes # Dicionário {tarefa: duracao_em_dias}
        self.precedencias = precedencias # Dicionário {tarefa: [lista_de_tarefas_precedentes]}
        self.prazo_maximo_dias = prazo_maximo_dias # Prazo final para todas as tarefas
        
        # Domínios: possíveis dias de início para cada tarefa
        self.dominios_iniciais = {}
        for tarefa in self.tarefas:
            # Se dura D dias, e começa no dia S, ocupa S, S+1, ..., S+D-1.
            # S <= prazo_maximo_dias - D
            max_inicio_possivel = prazo_maximo_dias - self.duracoes[tarefa]
            if max_inicio_possivel < 0: #  não cabe no prazo
                 self.dominios_iniciais[tarefa] = []
            else:
                self.dominios_iniciais[tarefa] = list(range(max_inicio_possivel + 1))


    def eh_consistente(self, tarefa_atual, data_inicio_atual, atribuicao):
        """
        Verifica se atribuir 'data_inicio_atual' para 'tarefa_atual' é consistente
        com as 'atribuicoes' já feitas e com o prazo.
        'atribuicao' é um dicionário {tarefa: (data_inicio, data_fim_calculada)}
        'data_fim_calculada' é o dia SEGUINTE ao último dia de trabalho.
        """
        data_fim_atual_calculada = data_inicio_atual + self.duracoes[tarefa_atual]

        # Se a tarefa termina no dia X, ela ocupa até o final do dia X-1.
        # Então, data_fim_atual_calculada (dia seguinte ao último dia) deve ser <= prazo_maximo_dias
        if data_fim_atual_calculada > self.prazo_maximo_dias:
            return False

        # Iterar sobre todas as tarefas já atribuídas para checar conflitos de precedência
        for tarefa_ja_atribuida, (inicio_ja_atribuida, fim_ja_atribuida_calculada) in atribuicao.items():
            # tarefa_atual deve começar DEPOIS ou NO MESMO DIA que tarefa_ja_atribuida terminar
            if tarefa_ja_atribuida in self.precedencias.get(tarefa_atual, []):
                if data_inicio_atual < fim_ja_atribuida_calculada:
                    return False
            
            #tarefa_ja_atribuida deve começar DEPOIS ou NO MESMO DIA que tarefa_atual terminar
            if tarefa_atual in self.precedencias.get(tarefa_ja_atribuida, []):
                if inicio_ja_atribuida < data_fim_atual_calculada:
                    return False
        return True

    def selecionar_variavel_nao_atribuida(self, atribuicao, dominios_atuais):
        """ Heurística MRV (Minimum Remaining Values). """
        nao_atribuidas = [t for t in self.tarefas if t not in atribuicao]
        if not nao_atribuidas:
            return None

        melhor_tarefa = None
        menor_tamanho_dominio = float('inf')

        for tarefa in self.tarefas: # Itera na ordem original para desempate consistente
            if tarefa in nao_atribuidas:
                tamanho_dominio = len(dominios_atuais[tarefa])
                if tamanho_dominio == 0: # Se algum domínio está vazio devido a FC, essa é uma falha
                    return tarefa # O backtrack vai falhar para ela.
                if tamanho_dominio < menor_tamanho_dominio:
                    menor_tamanho_dominio = tamanho_dominio
                    melhor_tarefa = tarefa
        
        if melhor_tarefa is None and nao_atribuidas:
            return nao_atribuidas[0]
        return melhor_tarefa


    def ordenar_valores_dominio(self, tarefa, atribuicao, dominios_atuais):
        """ Tenta os dias de início mais cedo primeiro. """
        return sorted(list(dominios_atuais[tarefa]))

    def forward_checking(self, tarefa_atribuida, data_inicio_atribuida, dominios_param, atribuicao_completa):
        """
        Forward Checking
        Retorna uma NOVA CÓPIA dos domínios atualizados, ou None se houver a inconsistência.
        dominios_param: domínios atuais antes desta atribuição ser considerada definitiva.
        atribuicao_completa: inclui a tarefa_atribuida e seu valor.
        """
        novos_dominios = copy.deepcopy(dominios_param) # cópia
        data_fim_atribuida_calculada = data_inicio_atribuida + self.duracoes[tarefa_atribuida]

        for tarefa_nao_atribuida_nome in self.tarefas:
            # processa tarefas que ainda não foram atribuídas em 'atribuicao_completa' e não sendo a própria tarefa_atribuida
            if tarefa_nao_atribuida_nome not in atribuicao_completa or tarefa_nao_atribuida_nome == tarefa_atribuida:
                 if tarefa_nao_atribuida_nome != tarefa_atribuida :
                    if tarefa_atribuida in self.precedencias.get(tarefa_nao_atribuida_nome, []):
                        # tarefa_nao_atribuida_nome deve começar APÓS ou NO MESMO DIA que tarefa_atribuida terminar
                        dominio_original_na = novos_dominios[tarefa_nao_atribuida_nome]
                        dominio_filtrado = [
                            dia for dia in dominio_original_na if dia >= data_fim_atribuida_calculada
                        ]
                        if not dominio_filtrado and dominio_original_na: 
                            return None # Inconsistência
                        novos_dominios[tarefa_nao_atribuida_nome] = dominio_filtrado
        return novos_dominios


def backtracking_search_csp(csp):
    # A primeira chamada ao backtrack usa os domínios iniciais
    return backtrack({}, csp, csp.dominios_iniciais)

def backtrack(atribuicao_atual, csp, dominios_atuais_param):
    """ Algoritmo de Backtracking para resolver o CSP da reforma. """
    if len(atribuicao_atual) == len(csp.tarefas): # Todas as tarefas foram atribuídas
        return atribuicao_atual # Solução encontrada
    
    tarefa_selecionada = csp.selecionar_variavel_nao_atribuida(atribuicao_atual, dominios_atuais_param)
    
    if tarefa_selecionada is None:
        # se acontecer, significa que não há mais vars para atribuir, mas a atribuição não está completa
        return None 
    
    #controle debug
    # print(f"Tentando tarefa: {tarefa_selecionada}, Domínio atual: {dominios_atuais_param.get(tarefa_selecionada, [])}")

    for data_inicio_valor in csp.ordenar_valores_dominio(tarefa_selecionada, atribuicao_atual, dominios_atuais_param):
        # Cria uma cópia da atribuição atual para este ramo da busca
        nova_atribuicao_ramo = atribuicao_atual.copy()

        if csp.eh_consistente(tarefa_selecionada, data_inicio_valor, nova_atribuicao_ramo):
            data_fim_calculada = data_inicio_valor + csp.duracoes[tarefa_selecionada]
            nova_atribuicao_ramo[tarefa_selecionada] = (data_inicio_valor, data_fim_calculada)
            # Forward Checking: passa os domínios atuais para serem copiados e modificados
            dominios_apos_fc = csp.forward_checking(tarefa_selecionada, data_inicio_valor, dominios_atuais_param, nova_atribuicao_ramo)

            if dominios_apos_fc is not None: # Se o Forward Checking não detectou inconsistência
                resultado_recursao = backtrack(nova_atribuicao_ramo, csp, dominios_apos_fc)
                if resultado_recursao is not None:
                    return resultado_recursao
    
    return None # siginfica  q nenhuma solução encontrada a partir deste ponto

# exemplo teste -> pode modificar aqui o meu exemplo
if __name__ == "__main__":
    print("Planejamento de Reforma de Cozinha - CSP")

    tarefas_reforma = ['Demolição', 'Encanamento', 'Elétrica', 'Alvenaria', 'Azulejos', 'Pintura', 'Marcenaria', 'Louças', 'Limpeza']
    duracoes_reforma = {
        'Demolição': 2, 'Encanamento': 3, 'Elétrica': 3, 'Alvenaria': 4,
        'Azulejos': 5, 'Pintura': 3, 'Marcenaria': 5, 'Louças': 2, 'Limpeza': 1
    }
    precedencias_reforma = {
        'Encanamento': ['Demolição'],
        'Elétrica': ['Demolição'],
        'Alvenaria': ['Demolição'],
        'Azulejos': ['Encanamento', 'Elétrica', 'Alvenaria'],
        'Pintura': ['Alvenaria', 'Azulejos'],
        'Marcenaria': ['Pintura'],
        'Louças': ['Azulejos', 'Marcenaria'],
        'Limpeza': ['Louças', 'Marcenaria', 'Pintura']
    }
    prazo_total_dias = 25 

    csp_reforma = ReformaCSP(tarefas_reforma, duracoes_reforma, precedencias_reforma, prazo_total_dias)

    print("\nDomínios iniciais (dias de início possíveis para cada tarefa):")
    for tarefa, dias in csp_reforma.dominios_iniciais.items():
        if dias:
            print(f"- {tarefa} (duração {csp_reforma.duracoes[tarefa]} dias): pode começar entre o dia {min(dias)} e {max(dias)}")
        else:
            print(f"- {tarefa} (duração {csp_reforma.duracoes[tarefa]} dias): NÃO HÁ DIAS POSSÍVEIS (verifique prazo e durações)")


    print(f"\nBuscando solução com prazo máximo de {prazo_total_dias} dias (último dia de trabalho é {prazo_total_dias-1})...")
    solucao = backtracking_search_csp(csp_reforma)

    if solucao:
        print("\n--- Cronograma da Reforma Encontrado! ---")
        cronograma_ordenado = sorted(solucao.items(), key=lambda item: item[1][0])
        for tarefa, (inicio, fim_calculado) in cronograma_ordenado:
            # último dia de trabalho é fim_calculado - 1
            print(f"Tarefa: {tarefa:<12} | Início: Dia {inicio:<2} | Fim: Dia {fim_calculado-1:<2} (Duração: {fim_calculado-inicio} dias)")
        
        # verifica final do prazo
        ultimo_dia_de_trabalho = -1
        for _, (_, fim_calc) in solucao.items():
            if fim_calc -1 > ultimo_dia_de_trabalho:
                ultimo_dia_de_trabalho = fim_calc -1
        print(f"\nReforma concluída ao final do Dia {ultimo_dia_de_trabalho}.")
        if ultimo_dia_de_trabalho < prazo_total_dias:
             print("Projeto dentro do prazo!")
        else:
             print("ATENÇÃO: Projeto excedeu o prazo (considerando que o prazo é o dia seguinte ao último dia de trabalho).")

    else:
        print("\n--- Nenhuma solução encontrada dentro do prazo e restrições. ---")