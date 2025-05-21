import random
import string

# Parâmetros gerais
FRASE_ALVO = "algoritmo genetico teste" #pode escolher a frase nessa linha, deixe em string
CARACTERES_VALIDOS = string.ascii_letters + string.digits + " " + "!.,?" # Inclui espaço e mias alguns símbolos
TAMANHO_POPULACAO = 150
TAXA_DE_MUTACAO = 0.02  
TAXA_DE_CROSSOVER = 0.85 
NUMERO_DE_GERACOES = 3000
TAMANHO_TORNEIO_SELECAO = 3 # Número de indivíduos em cada torneio de seleção
ELITISMO = True # Se True, o melhor indivíduo da geração anterior é mantido

def gerar_individuo(tamanho_frase):
    """Cria um indivíduo (string) aleatório."""
    return ''.join(random.choice(CARACTERES_VALIDOS) for _ in range(tamanho_frase))

def calcular_aptidao(individuo, frase_alvo):
    """Calcula a aptidão de um indivíduo (quão perto está da frase alvo)."""
    pontuacao = 0
    for i in range(len(individuo)):
        if individuo[i] == frase_alvo[i]:
            pontuacao += 1
    return pontuacao

def selecao_por_torneio(populacao, aptidoes, k_torneio):
    """Seleciona o indivíduo mais apto de um subconjunto aleatório da população."""
    indices_participantes = random.sample(range(len(populacao)), k_torneio)
    melhor_participante_idx = -1
    maior_aptidao_torneio = -1

    for idx in indices_participantes:
        if aptidoes[idx] > maior_aptidao_torneio:
            maior_aptidao_torneio = aptidoes[idx]
            melhor_participante_idx = idx
            
    return populacao[melhor_participante_idx]

def crossover_de_um_ponto(pai1, pai2):
    """Realiza crossover de um ponto entre dois pais para gerar dois filhos."""
    if len(pai1) != len(pai2) or len(pai1) < 2:
        return pai1, pai2 # Não pode fazer crossover

    ponto_de_corte = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto_de_corte] + pai2[ponto_de_corte:]
    filho2 = pai2[:ponto_de_corte] + pai1[ponto_de_corte:]
    return filho1, filho2

def mutar_individuo(individuo, taxa_mutacao, tamanho_frase):
    """Aplica mutação a um indivíduo."""
    lista_caracteres_individuo = list(individuo)
    for i in range(len(lista_caracteres_individuo)):
        if random.random() < taxa_mutacao:
            lista_caracteres_individuo[i] = random.choice(CARACTERES_VALIDOS)
    return "".join(lista_caracteres_individuo)

def executar_algoritmo_genetico(frase_alvo):
    tamanho_frase = len(frase_alvo)
    
    #1 Inicializar a população com indivíduos aleatórios
    populacao_atual = [gerar_individuo(tamanho_frase) for _ in range(TAMANHO_POPULACAO)]

    melhor_individuo_global = ""
    maior_aptidao_global = -1

    print(f"Iniciando Algoritmo Genético para a frase: '{frase_alvo}'")
    print(f"Tamanho da População: {TAMANHO_POPULACAO}, Gerações: {NUMERO_DE_GERACOES}\n")

    for geracao_num in range(NUMERO_DE_GERACOES):
        # 2 Calcular a aptidão de cada indivíduo na população
        aptidoes_atuais = [calcular_aptidao(ind, frase_alvo) for ind in populacao_atual]

        # Encontrar o melhor indivíduo da geração atual
        maior_aptidao_geracao = -1
        melhor_individuo_geracao = ""
        for i in range(len(populacao_atual)):
            if aptidoes_atuais[i] > maior_aptidao_geracao:
                maior_aptidao_geracao = aptidoes_atuais[i]
                melhor_individuo_geracao = populacao_atual[i]
        
        # Atualizar o melhor global se necessário
        if maior_aptidao_geracao > maior_aptidao_global:
            maior_aptidao_global = maior_aptidao_geracao
            melhor_individuo_global = melhor_individuo_geracao

        # Critério de parada: se a frase alvo foi encontrada
        if maior_aptidao_global == tamanho_frase:
            print(f"\n--- Solução Perfeita Encontrada na Geração {geracao_num + 1}! ---")
            break
        
        # Imprimir progresso a cada X gerações
        if (geracao_num + 1) % 100 == 0 or geracao_num == 0:
            print(f"Geração {geracao_num + 1:4d}: Melhor Aptidão = {maior_aptidao_global:2d}/{tamanho_frase}, "
                  f"Melhor Indivíduo = '{melhor_individuo_global}'")

        # Criar a próxima geração
        proxima_geracao = []

        # Elitismo: se habilitado, o melhor indivíduo passa diretamente
        if ELITISMO:
            proxima_geracao.append(melhor_individuo_global) 

        # 3 Preencher o restante da nova população
        while len(proxima_geracao) < TAMANHO_POPULACAO:
            # Seleção de pais
            pai1 = selecao_por_torneio(populacao_atual, aptidoes_atuais, TAMANHO_TORNEIO_SELECAO)
            pai2 = selecao_por_torneio(populacao_atual, aptidoes_atuais, TAMANHO_TORNEIO_SELECAO)

            # Crossover
            if random.random() < TAXA_DE_CROSSOVER:
                filho1, filho2 = crossover_de_um_ponto(pai1, pai2)
            else:
                filho1, filho2 = pai1, pai2 # Pais passam diretamente se não houver crossover

            # Mutação
            filho1_mutado = mutar_individuo(filho1, TAXA_DE_MUTACAO, tamanho_frase)
            filho2_mutado = mutar_individuo(filho2, TAXA_DE_MUTACAO, tamanho_frase)
            
            proxima_geracao.append(filho1_mutado)
            if len(proxima_geracao) < TAMANHO_POPULACAO: # Adiciona o segundo filho se houver espaço
                proxima_geracao.append(filho2_mutado)
        
        populacao_atual = proxima_geracao
        
    print(f"\n--- Fim do Algoritmo Genético após {geracao_num + 1} gerações ---")
    return melhor_individuo_global, maior_aptidao_global

if __name__ == "__main__":
    print("Algoritmo Genético para 'Adivinhar' Frase")
    
    solucao_final_ag, aptidao_final_ag = executar_algoritmo_genetico(FRASE_ALVO)
    
    print(f"\nResultado Final:")
    print(f"Melhor Indivíduo Encontrado: '{solucao_final_ag}'")
    print(f"Aptidão do Melhor Indivíduo: {aptidao_final_ag}/{len(FRASE_ALVO)}")
    print("-" * 30)