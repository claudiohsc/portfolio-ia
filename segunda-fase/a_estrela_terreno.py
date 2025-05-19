import heapq

def heuristica_manhattan(pos_atual, pos_objetivo):
    """Calcula a distância de Manhattan entre duas posições na grade."""
    (x1, y1) = pos_atual
    (x2, y2) = pos_objetivo
    return abs(x1 - x2) + abs(y1 - y2)

def a_estrela_grade_custos(grade_custos, inicio, objetivo, pesos_terreno):
    """
    Encontra o caminho de menor custo em uma grade com custos de movimento variáveis usando A*.

    paramentros:
        grade_custos (list[list[str]]): Grade representando o terreno.
                                     Ex: 'G' para grama, 'A' para água, 'M' para montanha.
                                     'S' para início, 'E' para fim. '#' para obstáculo.
        inicio: Coordenadas (linha, coluna) do início.
        objetivo: Coordenadas (linha, coluna) do objetivo.
        pesos_terreno (dicionario):  com os custos de movimento para cada tipo de terreno.
                               Ex: {'G': 1, 'A': 5, 'M': 10, 'S':1, 'E':1}

    Retorno:
        tuple: 
               O caminho (lista de coordenadas) e o custo total, 
               ou (None, float('inf')) se não houver caminho.
    """
    linhas = len(grade_custos)
    colunas = len(grade_custos[0])
    
    # Fronteira (fila de prioridade): (f_score, g_score, coordenadas_atuais, caminho_parcial)
    fronteira = []
    heapq.heappush(fronteira, (0 + heuristica_manhattan(inicio, objetivo), 0, inicio, [inicio]))
    
    # g_scores: custo do início até uma célula conhecida
    g_scores = {inicio: 0}
    
    # Movimentos possíveis (cima, baixo, esquerda, direita)
    movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while fronteira:
        _, g_score_atual, (r_atual, c_atual), caminho_atual = heapq.heappop(fronteira)

        if (r_atual, c_atual) == objetivo:
            return caminho_atual, g_score_atual # Caminho encontrado

        for dr, dc in movimentos:
            r_vizinho, c_vizinho = r_atual + dr, c_atual + dc

            if 0 <= r_vizinho < linhas and 0 <= c_vizinho < colunas:
                tipo_terreno_vizinho = grade_custos[r_vizinho][c_vizinho]
                
                if tipo_terreno_vizinho == '#': # Obstáculo
                    continue
                
                custo_movimento_vizinho = pesos_terreno.get(tipo_terreno_vizinho, float('inf'))
                g_score_tentativo_vizinho = g_score_atual + custo_movimento_vizinho

                if g_score_tentativo_vizinho < g_scores.get((r_vizinho, c_vizinho), float('inf')):
                    g_scores[(r_vizinho, c_vizinho)] = g_score_tentativo_vizinho
                    h_score_vizinho = heuristica_manhattan((r_vizinho, c_vizinho), objetivo)
                    f_score_vizinho = g_score_tentativo_vizinho + h_score_vizinho
                    
                    novo_caminho = list(caminho_atual)
                    novo_caminho.append((r_vizinho, c_vizinho))
                    heapq.heappush(fronteira, (f_score_vizinho, g_score_tentativo_vizinho, 
                                               (r_vizinho, c_vizinho), novo_caminho))
                                               
    return None, float('inf') # Caminho não encontrado

if __name__ == "__main__":
    # 'S' = Início, 'E' = Fim, 'G' = Grama, 'A' = Água, 'M' = Montanha, '#' = Obstáculo
    grade_terreno_exemplo = [
        ['S', 'G', 'G', 'A', 'A'],
        ['#', '#', 'G', 'A', 'M'],
        ['G', 'G', 'G', '#', 'M'],
        ['G', 'A', 'A', 'M', 'E'],
        ['G', 'G', 'M', 'M', '#']
    ]
    
    custos_terreno = {
        'S': 1,  # Custo para sair do início
        'E': 1,  # Custo para entrar no fim
        'G': 1,  # Grama
        'A': 5,  # Água
        'M': 10  # Montanha
    }

    # Encontrar 'S' e 'E'
    p_inicio = None
    p_fim = None
    for r_idx, linha_grade in enumerate(grade_terreno_exemplo):
        for c_idx, celula_grade in enumerate(linha_grade):
            if celula_grade == 'S':
                p_inicio = (r_idx, c_idx)
            elif celula_grade == 'E':
                p_fim = (r_idx, c_idx)

    if p_inicio is None or p_fim is None:
        print("Ponto de início 'S' ou fim 'E' não encontrado na grade.")
    else:
        print("Exemplo 2 (Simplificado): A* em Grade com Custos de Terreno")
        print("Grade de Terreno:")
        for linha_print in grade_terreno_exemplo:
            print(" ".join(linha_print))
        print(f"Custos: {custos_terreno}")
        
        caminho_a_estrela, custo_total_a_estrela = a_estrela_grade_custos(
            grade_terreno_exemplo, p_inicio, p_fim, custos_terreno
        )
        
        if caminho_a_estrela:
            print(f"\nCaminho encontrado por A*: {caminho_a_estrela}")
            print(f"Custo total do caminho: {custo_total_a_estrela}")

            # Visualização do caminho
            grade_visualizacao = [list(linha_v) for linha_v in grade_terreno_exemplo]
            for r_v, c_v in caminho_a_estrela:
                if grade_visualizacao[r_v][c_v] not in ['S', 'E']:
                    grade_visualizacao[r_v][c_v] = '*' # Marcaçao
            print("\nGrade com caminho ('*'):")
            for linha_v_print in grade_visualizacao:
                print(" ".join(linha_v_print))
        else:
            print(f"\nCaminho de {p_inicio} para {p_fim} não encontrado por A*.")
    print("-" * 30)