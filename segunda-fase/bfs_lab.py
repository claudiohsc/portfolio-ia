import collections

def bfs_labirinto(labirinto, inicio, fim):
    """
    Encontra o caminho mais curto em um labirinto usando BFS.

    Args:
        labirinto; Grade representando o labirinto.
                                     '#' para parede, ' ' para caminho,
                                     'S' para início, 'E' para fim.
        inicio: Coordenadas (linha, coluna) do início.
        fim: Coordenadas (linha, coluna) do fim.
    """
    linhas, colunas = len(labirinto), len(labirinto[0])
    fila = collections.deque() # Utilizei uma forma mais otimizada de fila de tuplas (coordenadas, caminho_parcial)
    
    # Adiciona o ponto de início à fila com o caminho inicial
    fila.append((inicio, [inicio])) 
    visitados = {inicio}

    if inicio == fim:
        return [inicio]

    while fila:
        (no_r, no_c), caminho_atual = fila.popleft()

        # Movimentos possíveis: cima, baixo, esquerda, direita
        movimentos = [(0, 1, 'Direita'), (0, -1, 'Esquerda'), (1, 0, 'Baixo'), (-1, 0, 'Cima')]

        for dr, dc, nome_movimento in movimentos:
            vizinho_r, vizinho_c = no_r + dr, no_c + dc

            if 0 <= vizinho_r < linhas and 0 <= vizinho_c < colunas and \
               labirinto[vizinho_r][vizinho_c] != '#' and \
               (vizinho_r, vizinho_c) not in visitados:

                novo_caminho = list(caminho_atual)
                novo_caminho.append((vizinho_r, vizinho_c))
                
                if (vizinho_r, vizinho_c) == fim:
                    return novo_caminho # Caminho encontrado
                
                visitados.add((vizinho_r, vizinho_c))
                fila.append(((vizinho_r, vizinho_c), novo_caminho))
                
    return None # Caminho não encontrado

if __name__ == "__main__":
    labirinto_exemplo = [
        ['S', ' ', '#', ' ', ' '],
        [' ', ' ', '#', ' ', '#'],
        ['#', ' ', '#', '#', ' '],
        [' ', ' ', ' ', ' ', 'E'],
        ['#', '#', '#', ' ', ' ']
    ]
    # Encontra 'S' e 'E' dinamicamente para flexibilidade
    inicio_coords = None
    fim_coords = None
    for r_idx, linha in enumerate(labirinto_exemplo):
        for c_idx, celula in enumerate(linha):
            if celula == 'S':
                inicio_coords = (r_idx, c_idx)
            elif celula == 'E':
                fim_coords = (r_idx, c_idx)

    if inicio_coords is None or fim_coords is None:
        print("Ponto de início 'S' ou fim 'E' não encontrado no labirinto.")
    else:
        print("BFS no Labirinto")
        print("Labirinto original:")
        for linha in labirinto_exemplo:
            print("".join(linha))
        
        caminho_encontrado = bfs_labirinto(labirinto_exemplo, inicio_coords, fim_coords)
        
        if caminho_encontrado:
            print(f"\nCaminho encontrado: {caminho_encontrado}")
            
            # ver o caminho no labirinto:
            labirinto_com_caminho = [list(linha) for linha in labirinto_exemplo] # Cria a cópia
            for r_path, c_path in caminho_encontrado:
                if labirinto_com_caminho[r_path][c_path] not in ['S', 'E']:
                    labirinto_com_caminho[r_path][c_path] = '.' # Marca o caminho
            
            print("\nLabirinto com caminho ('.'):")
            for linha in labirinto_com_caminho:
                print("".join(linha))
        else:
            print("\nCaminho não encontrado.")
    print("-" * 30)