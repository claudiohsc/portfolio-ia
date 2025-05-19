import random

def funcao_objetivo_parabola(x):
    """Função a ser maximizada: -(x-7)^2 + 20. Máximo em x=7, f(x)=20."""
    return -((x - 7)**2) + 20

def hill_climbing_simples(func_objetivo, x_inicial, passo, max_iteracoes, dominio_min, dominio_max):
    """
    Encontra o máximo de uma função usando Hill Climbing.

    paramentros:
        func_objetivo: A função a ser maximizada.
        x_inicial: Ponto de partida (float).
        passo: Tamanho do passo para explorar vizinhos (float).
        max_iteracoes: Número máximo de iterações.
        dominio_min: Limite inferior do domínio de x.
        dominio_max: Limite superior do domínio de x.

    Returns:
        tuple: (melhor_x_encontrado, melhor_valor_funcao_encontrado)
    """
    x_atual = x_inicial
    valor_atual = func_objetivo(x_atual)
    print(f"Iniciando Hill Climbing em x={x_atual:.4f}, f(x)={valor_atual:.4f}")

    for i in range(max_iteracoes):
        # Gera dois vizinhos: um para a esquerda e outro para a direita
        x_vizinho_esq = max(dominio_min, x_atual - passo)
        x_vizinho_dir = min(dominio_max, x_atual + passo)
        
        valor_vizinho_esq = func_objetivo(x_vizinho_esq)
        valor_vizinho_dir = func_objetivo(x_vizinho_dir)
        
        melhor_vizinho_x = x_atual
        melhor_vizinho_valor = valor_atual
        #trocas
        if valor_vizinho_esq > melhor_vizinho_valor:
            melhor_vizinho_x = x_vizinho_esq
            melhor_vizinho_valor = valor_vizinho_esq
            
        if valor_vizinho_dir > melhor_vizinho_valor: # se dir for melhor que esq (que já pode ser > atual)
            melhor_vizinho_x = x_vizinho_dir
            melhor_vizinho_valor = valor_vizinho_dir
            
        if melhor_vizinho_valor > valor_atual:
            x_atual = melhor_vizinho_x
            valor_atual = melhor_vizinho_valor
            #print(f"Iter {i+1}: Movendo para x={x_atual:.4f}, f(x)={valor_atual:.4f}")  /// descomente essa linha para ver as iterações
        else:
            # Atingiu um máximo local (ou platô, pois não há melhoria)
            # print(f"Iter {i+1}: Máximo local encontrado ou sem melhoria.")      /// descomente essa linha para ver as iterações
            break
            
    return x_atual, valor_atual

if __name__ == "__main__":
    # Parâmetros para o Hill Climbing
    x_partida = random.uniform(0, 15) # Ponto de partida aleatório no domínio [0, 15]
    tamanho_passo = 0.01
    num_iteracoes = 500
    limite_inferior_dominio = 0
    limite_superior_dominio = 15

    print("Hill Climbing para Otimizar Função Matemática")
    print(f"Maximizando f(x) = -(x-7)^2 + 20 (Máximo esperado em x=7, f(x)=20)")
    
    melhor_x_encontrado, max_valor_encontrado = hill_climbing_simples(
        funcao_objetivo_parabola, 
        x_partida, 
        tamanho_passo, 
        num_iteracoes,
        limite_inferior_dominio,
        limite_superior_dominio
    )
    
    print(f"\nApós Hill Climbing:")
    print(f"Máximo encontrado em x = {melhor_x_encontrado:.4f}")
    print(f"Valor da função no máximo encontrado f(x) = {max_valor_encontrado:.4f}")
    print("-" * 30)